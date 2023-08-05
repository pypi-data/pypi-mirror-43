#! /usr/bin/env python

# Copyright (C) 2018  Charlie Hoy <charlie.hoy@ligo.org>
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 3 of the License, or (at your
# option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
# Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

import argparse
import socket
import os
import shutil
from glob import glob

import numpy as np
import h5py

import pesummary
from pesummary.utils.utils import guess_url, combine_hdf_files, logger
from pesummary.utils.utils import rename_group_or_dataset_in_hf5_file
from pesummary.utils import utils
from pesummary.one_format.data_format import one_format

import lal
import lalsimulation as lalsim

__doc__ == "Classes to handle the command line inputs"

def command_line():
    """Creates an ArgumentParser object which holds all of the information
    from the command line.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-w", "--webdir", dest="webdir",
                        help="make page and plots in DIR", metavar="DIR",
                        default=None)
    parser.add_argument("-b", "--baseurl", dest="baseurl",
                        help="make the page at this url", metavar="DIR",
                        default=None)
    parser.add_argument("-s", "--samples", dest="samples",
                        help="Posterior samples hdf5 file", nargs='+',
                        default=None)
    parser.add_argument("-a", "--approximant", dest="approximant",
                        help="waveform approximant used to generate samples",
                        nargs='+', default=None)
    parser.add_argument("--email", action="store",
                        help="send an e-mail to the given address with a link to the finished page.",
                        default=None, metavar="user@ligo.org")
    parser.add_argument("--dump", action="store_true",
                        help="dump all information onto a single html page",
                        default=False)
    parser.add_argument("-c", "--config", dest="config",
                        help="configuration file associcated with each samples file.", nargs='+',
                        default=None)
    parser.add_argument("--sensitivity", action="store_true",
                        help="generate sky sensitivities for HL, HLV",
                        default=False)
    parser.add_argument("--add_to_existing", action="store_true",
                        help="add new results to an existing html page",
                        default=False)
    parser.add_argument("-e", "--existing_webdir", dest="existing",
                        help="web directory of existing output",
                        default=None)
    parser.add_argument("-i", "--inj_file", dest="inj_file",
                        help="path to injetcion file", nargs='+',
                        default=None)
    parser.add_argument("--user", dest="user", help=argparse.SUPPRESS,
                        default="albert.einstein")
    parser.add_argument("--gracedb", dest="gracedb",
                        help="gracedb of the event", default=None)
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="print useful information for debugging purposes")
    return parser


class Input():
    """Super class to handle command line arguments

    Parameters
    ----------
    parser: argparser
        The parser containing the command line arguments

    Attributes
    ----------
    user: str
        The user who submitted the job
    add_to_existing: Bool
        Boolean to determine if you wish to add to a existing webpage
    existing: str
        Existing web directory
    webdir: str
        Directory to output all information
    baseurl: str
        The url path for the corresponding web directory
    inj_file: List
        List containing paths to the injection file
    result_files: list
        List containing paths to the results files which are being analysed
    config: list
        List containing paths to the configuration files used to generate each
        results files
    approximant: list
        List of approximants used in the analysis to generate each results files
    email: str
        The email address to notify when the job has completed
    sensitivity: Bool
        Boolean to determine if you wish to plot the sky sensitivity for
        different detector networks
    gracedb: str
        The gracedb of the event that produced the results files
    dump: Bool
        Boolean to determine if you wish to produce a dumped html page layout
    detectors: list
        List containing the detectors used to generate each results file
    labels: str
        A label for this summary page
    """
    def __init__(self, opts):
        logger.info("Command line arguments: %s" %(opts))
        self.user = opts.user
        self.existing = opts.existing
        self.webdir = opts.webdir
        self.baseurl = opts.baseurl
        self.inj_file = opts.inj_file
        self.result_files = opts.samples
        self.config = opts.config
        self.approximant = opts.approximant
        self.email = opts.email
        self.add_to_existing = opts.add_to_existing
        self.sensitivity = opts.sensitivity
        self.gracedb = opts.gracedb
        self.dump = opts.dump
        self.check_approximant_in_results_file()
        self.make_directories()
        self.copy_files()
        self.detectors = None
        self.labels = None
        self.check_label_in_results_file()

    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, user):
        try:
            self._user = os.environ["USER"]
            logger.debug("The following user submitted the job %s" %(self._user))
        except Exception as e:
            logger.info("Failed to grab user information because %s. "
                        "Default will be used" %(e))
            self._user = user

    @property
    def host(self):
        return socket.getfqdn()

    @property
    def existing(self):
        return self._existing

    @existing.setter
    def existing(self, existing):
        if not existing:
            self._existing = None
        else:
            self._existing = existing

    @property
    def webdir(self):
        return self._webdir

    @webdir.setter
    def webdir(self, webdir):
        if not webdir and not self.existing:
            raise Exception("Please provide a web directory to store the "
                            "webpages. If this is an existing directory "
                            "pass this path under the --existing_dir "
                            "argument. If this is a new directory then "
                            "pass this under the --webdir argument")
        elif not webdir and self.existing:
            if not os.path.isdir(self.existing):
                raise Exception("The directory %s does not "
                                "exist" %(self.existing))
            entries = glob(self.existing+"/*")
            if "%s/home.html" %(self.existing) not in entries:
                raise Exception("Please give the base directory of an existing "
                                "output")
            self._webdir = self.existing
        if webdir:
            if not os.path.isdir(webdir):
                logger.debug("Given web directory does not exist. "
                             "Creating it now")
                utils.make_dir(webdir)
            self._webdir = webdir

    @property
    def baseurl(self):
        return self._baseurl

    @baseurl.setter
    def baseurl(self, baseurl):
        self._baseurl = baseurl
        if not baseurl:
            self._baseurl = guess_url(self.webdir, socket.getfqdn(), self.user) 
            logger.debug("No url is provided. The url %s will be "
                         "used" %(self._baseurl))

    @property
    def inj_file(self):
        return self._inj_file

    @inj_file.setter
    def inj_file(self, inj_file):
        if inj_file:
            self._inj_file = inj_file
        else:
            self._inj_file = None
        self._inj_file = inj_file


    @property
    def result_files(self):
        return self._samples

    @result_files.setter
    def result_files(self, samples):
        sample_list = [] 
        if not samples:
            raise Exception("Please provide a results file")
        if self.inj_file and len(samples) != len(self.inj_file):
            raise Exception("The number of results files does not match the "
                            "number of injection files")
        if not self.inj_file:
            self.inj_file = [None]*len(samples)
        for num, i in enumerate(samples):
            if not os.path.isfile(i):
                raise Exception("File %s does not exist" %(i))
            std_form = self.convert_to_standard_format(i, self.inj_file[num])
            sample_list.append(std_form)
        self._samples = sample_list

    @property
    def config(self):
        return self._config

    @config.setter
    def config(self, config):
        if config and len(self.result_files) != len(config):
            raise Exception("Ensure that the number of results files match "
                            "the number of configuration files")
        self._config = config

    @property
    def approximant(self):
        return self._approximant

    @approximant.setter
    def approximant(self, approximant):
        if not approximant:
            logger.debug("No approximant is given. Trying to extract from "
                         "results file")
            approximant_list = []
            for i in self.result_files:
                f = h5py.File(i, "r")
                approx = list(f["label"].keys())[0]
                f.close()
                if approx == "none":
                    raise Exception("Failed to extract the approximant "
                                    "from the file: %s. Please pass the "
                                    "approximant with the flag "
                                    "--approximant" %(i.split("_temp")[0]))
                approximant_list.append(approx)
        else:
            approximant_list = approximant
        if len(approximant_list) != len(self.result_files):
            raise Exception("The number of results files does not match the "
                            "number of approximants")
        self._approximant = approximant_list

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, email):
        if email:
            self._email = email
        else:
            self._email = None

    @property
    def add_to_existing(self):
        return self._add_to_existing

    @add_to_existing.setter
    def add_to_existing(self, add_to_existing):
        self._add_to_existing = False
        if add_to_existing and not self.existing:
            raise Exception("Please provide a current html page that you "
                            "wish to add content to")
        if not add_to_existing and self.existing:
            logger.debug("Existing html page has been given without specifying "
                         "--add_to_existing flag. This is probably and error "
                         "and so manually adding --add_to_existing flag")
            self._add_to_existing = True
        if add_to_existing and self.existing:
            if self.config:
                for i in glob(self.existing+"/config/*"):
                    self.config.append(i)
            self._add_to_existing = True

    @property
    def gracedb(self):
        return self._gracedb

    @gracedb.setter
    def gracedb(self, gracedb):
        if gracedb:
            self._gracedb = gracedb
        else:
            self._gracedb = None

    @property
    def dump(self):
        return self._dump

    @dump.setter
    def dump(self, dump):
        if dump:
            self._dump = True
        else:
            self._dump = False

    @property
    def detectors(self):
        return self._detectors

    @detectors.setter
    def detectors(self, detectors):
        detector_list = []
        if not detectors:
            for num, i in enumerate(self.result_files):
                f = h5py.File(i)
                params = [j for j in f["label/%s/parameter_names" %(self.approximant[num])]]
                f.close()
                individual_detectors = []
                for j in params:
                    if b"optimal_snr" in j:
                        individual_detectors.append(j.split(b"_optimal_snr")[0])
                individual_detectors = [i.decode("utf-8") for i in individual_detectors]
                if individual_detectors:
                    detector_list.append("_".join(individual_detectors))
        else:
            detector_list = detectors
        logger.debug("The detector network is %s" %(detector_list))
        self._detectors = detector_list

    @property
    def labels(self):
        return self._labels

    @labels.setter
    def labels(self, labels):
        label_list = []
        for num, i in enumerate(self.result_files):
            if self.gracedb and self.detectors and type(self.detectors[num]) == list:
                for i in self.detectors[num]:
                    label_list.append("_".join([self.gracedb, i]))
            elif self.gracedb and self.detectors and type(self.detectors[num]) == str:
                label_list.append("_".join([self.gracedb, self.detectors[num]]))
            elif self.gracedb:
                label_list.append(self.gracedb)
            elif self.detectors and type(self.detectors[num]) == list:
                for i in self.detectors[num]:
                    label_list.append("_".join(self.detectors[num]))
            elif self.detectors and type(self.detectors[num]) == str:
                label_list.append(self.detectors[num])
            else:
                for i in range(len(self.approximant)):
                    label_list.append("%s" %(i))
        proposed_names = ["%s_%s" %(i,j) for i,j in zip(label_list, self.approximant)]
        duplicates=dict(set((x,proposed_names.count(x)) for x in \
            filter(lambda rec : proposed_names.count(rec)>1,proposed_names)))
        for i in duplicates.keys():
            for j in range(duplicates[i]):
                ind = proposed_names.index(i)
                proposed_names[ind] += "_%s" %(j)
                label_list[ind] += "_%s" %(j)
        if self.add_to_existing:
            f = h5py.File(self.existing+"/samples/posterior_samples.h5")
            labels = list(f.keys())
            current_labels = ["%s_%s" %(i, j) for i in labels \
                for j in list(f[i].keys())]
            logger.info("%s" %(current_labels))
            for num, i in enumerate(proposed_names):
                if i in current_labels:
                    label_list[ind] += "_%s" %(num)
        logger.debug("The label is %s" %(label_list))
        self._labels = label_list

    def check_approximant_in_results_file(self):
        """Check that the approximant that is stored in the results file
        corresponds to the given approximant. If not then this will be changed.
        """
        for num, i in enumerate(self.result_files):
            f = h5py.File(i, "r")
            keys = list(f["label"].keys())
            f.close()
            if "none" in keys:
                rename_group_or_dataset_in_hf5_file(i,
                    group = ["label/none", "label/%s" %(self.approximant[num])])

    def check_label_in_results_file(self):
        """Check that the label that is stored in the results file corresponds
        to the given label. If not then this will be changed.
        """
        for num, i in enumerate(self.result_files):
            rename_group_or_dataset_in_hf5_file(i,
                group = ["label", self.labels[num]])

    def make_directories(self):
        """Make the directorys in the web directory to store all information.
        """
        dirs = ["samples", "plots", "js", "html", "css", "plots/corner",
                "config"]
        for i in dirs:
            utils.make_dir(self.webdir + "/%s" %(i))

    def copy_files(self):
        """Copy the relevant files to the web directory.
        """
        logger.info("Copying the files to %s" %(self.webdir))
        path = pesummary.__file__[:-12]
        scripts = glob(path+"/js/*.js")
        for i in scripts:
            shutil.copyfile(i, self.webdir+"/js/%s" %(i.split("/")[-1]))
        scripts = glob(path+"/css/*.css")
        for i in scripts:
            shutil.copyfile(i, self.webdir+"/css/%s" %(i.split("/")[-1]))
        if self.config:
            for num, i in enumerate(self.config):
                if self.webdir not in i:
                    shutil.copyfile(i, self.webdir+"/config/"+\
                                    self.approximant[num]+"_"+i.split("/")[-1])

    def convert_to_standard_format(self, results_file, injection_file=None):
        """Convert a results file to standard form.

        Parameters
        ----------
        results_file: str
            Path to the results file that you wish to convert to standard
            form
        injection_file: str, optional
            Path to the injection file that was used in the analysis to
            produce the results_file
        """
        logger.debug("Converting %s to standard format" %(results_file))
        f = one_format(results_file, injection_file)
        f.generate_all_posterior_samples()
        return f.save()


class PostProcessing():
    """Class to extract parameters from the results files

    Parameters
    ----------
    inputs: argparser
        The parser containing the command line arguments
    colors: list, optional
        colors that you would like to use to display each results file in the
        webpage

    Attributes
    ----------
    parameters: list
        list of parameters that have posterior distributions for each results
        file
    injection_data: list
        list of dictionaries that contain the injection parameters and their
        injected value for each results file
    samples: list
        list of posterior samples for each parameter for each results file
    maxL_samples: list
        list of dictionaries that contain each parameter and their corresponding
        maximum likelihood value for each results file
    same_parameters: list
        List of parameters that all results files have sampled over

    """
    def __init__(self, inputs, colors="default"):
        self.inputs = inputs
        self.webdir = inputs.webdir
        self.baseurl = inputs.baseurl
        self.result_files = inputs.result_files
        self.approximant = inputs.approximant
        self.detectors = inputs.detectors
        self.dump = inputs.dump
        self.email = inputs.email
        self.user = inputs.user
        self.host = inputs.host
        self.config = inputs.config
        self.existing = inputs.existing
        self.gracedb = inputs.gracedb
        self.add_to_existing = inputs.add_to_existing
        self.labels = inputs.labels
        self.sensitivity = inputs.sensitivity
        self.colors = colors

        self.parameters = []
        self.injection_data = []
        self.samples = []
        self.maxL_samples = []
        self.same_parameters = []

    @property
    def coherence_test(self):
        duplicates=dict(set((x,self.approximant.count(x)) for x in \
            filter(lambda rec : self.approximant.count(rec)>1,self.approximant)))
        if len(duplicates.keys()) > 0:
            return True
        return False

    @property
    def colors(self):
        return self._colors

    @colors.setter
    def colors(self, colors):
        if colors == "default":
            self._colors = ["#a6b3d0", "#baa997", "#FF6347", "#FFA500",
                            "#003366"]
        else:
            if not len(self.result_files) <= colors:
                raise Exception("Please give the same number of colors as "
                                "results files")
            self._colors = colors

    @property
    def parameters(self):
        return self._parameters

    @parameters.setter
    def parameters(self, parameters):
        parameter_list = []
        for num, results_files in enumerate(self.result_files):
            f = h5py.File(results_files, "r")
            p = [i for i in f["%s/%s/parameter_names" %(
                self.labels[num], self.approximant[num])]]
            parameter_list.append([i.decode("utf-8") for i in p])
            f.close()
        self._parameters = parameter_list

    @property
    def injection_data(self):
        return self._injection_data

    @injection_data.setter
    def injection_data(self, injection_data):
        injection_list = []
        for num, results_files in enumerate(self.result_files):
            f = h5py.File(results_files, "r")
            inj_p = [i for i in f["%s/%s/injection_parameters" %(
                self.labels[num], self.approximant[num])]]
            inj_p = [i.decode("utf-8") for i in inj_p]
            inj_data = [i for i in f["%s/%s/injection_data" %(
                self.labels[num], self.approximant[num])]]
            injection_list.append({i:j for i,j in zip(inj_p, inj_data)})
        self._injection_data = injection_list

    @property
    def samples(self):
        return self._samples

    @samples.setter
    def samples(self, samples):
        sample_list = []
        for num, results_files in enumerate(self.result_files):
            f = h5py.File(results_files, "r")
            s = [i for i in f["%s/%s/samples" %(
                self.labels[num], self.approximant[num])]]
            sample_list.append(s)
        self._samples = sample_list

    @property
    def maxL_samples(self):
        return self._maxL_samples

    @maxL_samples.setter
    def maxL_samples(self, maxL_samples):
        key_data = self._key_data()
        maxL_list = []
        for num, i in enumerate(self.parameters):
            dictionary = {j: key_data[num][j]["maxL"] for j in i}
            dictionary["approximant"] = self.approximant[num]
            maxL_list.append(dictionary)
        self._maxL_samples = maxL_list

    @property
    def same_parameters(self):
        return self._same_parameters

    @same_parameters.setter
    def same_parameters(self, same_parameters):
        params = list(set.intersection(*[set(l) for l in self.parameters]))
        self._same_parameters = params
            
    def _key_data(self):
        """Grab the mean, median, maximum likelihood value and the standard
        deviation of each posteiror distribution for each results file.
        """
        key_data_list = []
        for num, i in enumerate(self.samples):
            data = {}
            likelihood_ind = self.parameters[num].index("log_likelihood")
            logL = [j[likelihood_ind] for j in i]
            for ind, j in enumerate(self.parameters[num]):
                index = self.parameters[num].index("%s" %(j))
                subset = [k[index] for k in i]
                data[j] = {"mean": np.mean(subset),
                           "median": np.median(subset),
                           "maxL": subset[logL.index(np.max(logL))],
                           "std": np.std(subset)}
            key_data_list.append(data)
        return key_data_list
