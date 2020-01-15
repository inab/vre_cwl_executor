"""
.. See the NOTICE file distributed with this work for additional information
   regarding copyright ownership.

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""
from __future__ import print_function

import sys
import os
import configparser
import subprocess
import tempfile
import json
import fnmatch
import tarfile
import shutil
import io

import hashlib

import uuid

from utils import logger

try:
    if hasattr(sys, '_run_from_cmdl') is True:
        raise ImportError
    from pycompss.api.parameter import FILE_IN, FILE_OUT
    from pycompss.api.task import task
    from pycompss.api.api import compss_wait_on
except ImportError:
    # logger.warn("[Warning] Cannot import \"pycompss\" API packages.")
    # logger.warn("          Using mock decorators.")

    from utils.dummy_pycompss import FILE_IN, FILE_OUT  # pylint: disable=ungrouped-imports
    from utils.dummy_pycompss import task  # pylint: disable=ungrouped-imports
    from utils.dummy_pycompss import compss_wait_on  # pylint: disable=ungrouped-imports

from basic_modules.tool import Tool
from basic_modules.metadata import Metadata

import tempfile


class WF_RUNNER(Tool):
    """
    Tool for writing to a file
    """
    # DEFAULT_NXF_IMAGE = 'nextflow/nextflow'
    # DEFAULT_NXF_VERSION = '19.04.1'
    # DEFAULT_WF_BASEDIR = 'WF-checkouts'

    # DEFAULT_DOCKER_CMD = 'docker'
    # DEFAULT_GIT_CMD = 'git'

    MASKED_KEYS = {'execution', 'project', 'description', 'cwl_wf_repo_uri', 'cwl_wf_repo_tag'}

    def __init__(self, configuration=None):
        """
        Init function
        """
        logger.info("VRE CWL Workflow runner")
        Tool.__init__(self)

        # local_config = configparser.ConfigParser()
        # local_config.read(sys.argv[0] + '.ini')

        # TODO setup parameters for installing cwtool with docker
        # self.nxf_image = local_config.get('nextflow', 'docker_image') if local_config.has_option('nextflow',
        #                                                                                          'docker_image') else self.DEFAULT_NXF_IMAGE
        # self.nxf_version = local_config.get('nextflow', 'version') if local_config.has_option('nextflow',
        #                                                                                       'version') else self.DEFAULT_NXF_VERSION
        #
        # self.wf_basedir = os.path.abspath(os.path.expanduser(
        #     local_config.get('data', 'basedir') if local_config.has_option('data',
        #                                                                         'basedir') else self.DEFAULT_WF_BASEDIR))

        # Where the external commands should be located
        # self.docker_cmd = local_config.get('defaults', 'docker_cmd') if local_config.has_option('defaults',
        #                                                                                         'docker_cmd') else self.DEFAULT_DOCKER_CMD
        # self.git_cmd = local_config.get('defaults', 'git_cmd') if local_config.has_option('defaults',
        #                                                                                   'git_cmd') else self.DEFAULT_GIT_CMD

        # Now, we have to assure the CWLTOOL is already here
        # docker_tag = self.nxf_image + ':' + self.nxf_version
        # checkimage_params = [
        #     self.docker_cmd, "images", "--format", "{{.ID}}\t{{.Tag}}", docker_tag
        # ]
        #
        # with tempfile.NamedTemporaryFile() as checkimage_stdout:
        #     with tempfile.NamedTemporaryFile() as checkimage_stderr:
        #         retval = subprocess.call(checkimage_params, stdout=checkimage_stdout, stderr=checkimage_stderr)
        #
        #         if retval != 0:
        #             # Reading the output and error for the report
        #             with open(checkimage_stdout.name, "r") as c_stF:
        #                 checkimage_stdout_v = c_stF.read()
        #             with open(checkimage_stderr.name, "r") as c_stF:
        #                 checkimage_stderr_v = c_stF.read()
        #
        #             errstr = "ERROR: VRE Nextflow Runner failed while checking Nextflow image (retval {}). Tag: {}\n======\nSTDOUT\n======\n{}\n======\nSTDERR\n======\n{}".format(
        #                 retval, docker_tag, checkimage_stdout_v, checkimage_stderr_v)
        #             logger.fatal(errstr)
        #             raise Exception(errstr)
        #
        #     do_pull_image = os.path.getsize(checkimage_stdout.name) == 0
        #
        # if do_pull_image:
        #     # The image is not here yet
        #     pullimage_params = [
        #         self.docker_cmd, "pull", docker_tag
        #     ]
        #     with tempfile.NamedTemporaryFile() as pullimage_stdout:
        #         with tempfile.NamedTemporaryFile() as pullimage_stderr:
        #             retval = subprocess.call(pullimage_params, stdout=pullimage_stdout, stderr=pullimage_stderr)
        #             if retval != 0:
        #                 # Reading the output and error for the report
        #                 with open(pullimage_stdout.name, "r") as c_stF:
        #                     pullimage_stdout_v = c_stF.read()
        #                 with open(pullimage_stderr.name, "r") as c_stF:
        #                     pullimage_stderr_v = c_stF.read()
        #
        #                 # It failed!
        #                 errstr = "ERROR: VRE Nextflow Runner failed while pulling Nextflow image (retval {}). Tag: {}\n======\nSTDOUT\n======\n{}\n======\nSTDERR\n======\n{}".format(
        #                     retval, docker_tag, pullimage_stdout_v, pullimage_stderr_v)
        #                 logger.fatal(errstr)
        #                 raise Exception(errstr)

        if configuration is None:
            configuration = {}

        self.configuration.update(configuration)
        # Arrays are serialized
        for k, v in self.configuration.items():
            if isinstance(v, list):
                self.configuration[k] = ' '.join(v)

        self.populable_outputs = {}

    def doMaterializeRepo(self, git_uri, git_tag):
        repo_hashed_id = hashlib.sha1(git_uri).hexdigest()
        repo_hashed_tag_id = hashlib.sha1(git_tag).hexdigest()

        # Assure directory exists before next step
        repo_destdir = os.path.join(self.wf_basedir, repo_hashed_id)
        if not os.path.exists(repo_destdir):
            try:
                os.makedirs(repo_destdir)
            except IOError as error:
                errstr = "ERROR: Unable to create intermediate directories for repo {}. ".format(git_uri, )
                raise Exception(errstr)

        repo_tag_destdir = os.path.join(repo_destdir, repo_hashed_tag_id)
        # We are assuming that, if the directory does exist, it contains the repo
        if not os.path.exists(repo_tag_destdir):
            # Try cloing the repository without initial checkout
            gitclone_params = [
                self.git_cmd, 'clone', '-n', '--recurse-submodules', git_uri, repo_tag_destdir
            ]

            # Now, checkout the specific commit
            gitcheckout_params = [
                self.git_cmd, 'checkout', git_tag
            ]

            # Last, initialize submodules
            gitsubmodule_params = [
                self.git_cmd, 'submodule', 'update', '--init'
            ]

            with tempfile.NamedTemporaryFile() as git_stdout:
                with tempfile.NamedTemporaryFile() as git_stderr:
                    # First, bare clone
                    retval = subprocess.call(gitclone_params, stdout=git_stdout, stderr=git_stderr)
                    # Then, checkout
                    if retval == 0:
                        retval = subprocess.Popen(gitcheckout_params, stdout=git_stdout, stderr=git_stderr,
                                                  cwd=repo_tag_destdir).wait()
                    # Last, submodule preparation
                    if retval == 0:
                        retval = subprocess.Popen(gitsubmodule_params, stdout=git_stdout, stderr=git_stderr,
                                                  cwd=repo_tag_destdir).wait()

                    # Proper error handling
                    if retval != 0:
                        # Reading the output and error for the report
                        with open(git_stdout.name, "r") as c_stF:
                            git_stdout_v = c_stF.read()
                        with open(git_stderr.name, "r") as c_stF:
                            git_stderr_v = c_stF.read()

                        errstr = "ERROR: VRE Nextflow Runner could not pull '{}' (tag '{}'). Retval {}\n======\nSTDOUT\n======\n{}\n======\nSTDERR\n======\n{}".format(
                            git_uri, git_tag, retval, git_stdout_v, git_stderr_v)
                        raise Exception(errstr)

        return repo_tag_destdir

    def packDir(self, resultsDir, destTarFile):
        # This is only needed when a manifest must be generated

        # for metrics_file in os.listdir(resultsDir):
        #        abs_metrics_file = os.path.join(resultsDir, metrics_file)
        #        if fnmatch.fnmatch(metrics_file,"*.json") and os.path.isfile(abs_metrics_file):
        #                with io.open(abs_metrics_file,mode='r',encoding="utf-8") as f:
        #                        metrics = json.load(f)
        #                        metricsArray.append(metrics)
        #
        # with io.open(metrics_loc, mode='w', encoding="utf-8") as f:
        #        jdata = json.dumps(metricsArray, sort_keys=True, indent=4, separators=(',', ': '))
        #        f.write(unicode(jdata,"utf-8"))

        # And create the MuG/VRE tar file
        with tarfile.open(destTarFile, mode='w:gz', bufsize=1024 * 1024) as tar:
            tar.add(resultsDir, arcname='data', recursive=True)

    # @task(returns=bool, input_loc=FILE_IN, goldstandard_dir_loc=FILE_IN, assess_dir_loc=FILE_IN,
    #       public_ref_dir_loc=FILE_IN, results_loc=FILE_OUT, stats_loc=FILE_OUT, other_loc=FILE_OUT, isModifier=False)
    # def execute_cwl_workflow(self, input_loc, goldstandard_dir_loc, assess_dir_loc, public_ref_dir_loc, results_loc,
    #                          stats_loc, other_loc):  # pylint: disable=no-self-use

    @task(returns=bool, input_files=FILE_IN, configuration=FILE_IN, isModifier=False)
    def execute_cwl_workflow(self, input_files, configuration):  # pylint: disable=no-self-use

        # First, we need to materialize the workflow
        cwl_wf_repo_uri = self.configuration.get('cwl_wf_repo_uri')
        cwl_wf_repo_tag = self.configuration.get('cwl_wf_repo_tag')

        if (cwl_wf_repo_uri is None) or (cwl_wf_repo_tag is None):
            logger.fatal("FATAL ERROR: both 'cwl_wf_repo_uri' and 'cwl_wf_repo_tag' parameters must be defined")
            return False

        # Checking out the repo to be used
        try:
            repo_dir = self.doMaterializeRepo(cwl_wf_repo_uri, cwl_wf_repo_tag)
        except Exception as error:
            logger.fatal("While materializing repo: " + type(error).__name__ + ': ' + str(error))
            return False

        # These are the parameters, including input and output files and directories

        # Parameters which are not input or output files are in the configuration
        variable_params = [
            #    ('challenges_ids',challenges_ids),
            #    ('participant_id',participant_id)
        ]
        for conf_key in self.configuration.keys():
            if conf_key not in self.MASKED_KEYS:
                variable_params.append((conf_key, self.configuration[conf_key]))

        # variable_infile_params = [
        #     ('input', input_loc),
        #     ('goldstandard_dir', goldstandard_dir_loc),
        #     ('public_ref_dir', public_ref_dir_loc),
        #     ('assess_dir', assess_dir_loc)
        # ]
        #
        # variable_outfile_params = [
        #     ('statsdir', stats_loc),
        #     ('outdir', results_loc),
        #     ('otherdir', other_loc)
        # ]

        # The list of populable outputs
        # variable_outfile_params.extend(self.populable_outputs.items())

        # TODO
        # Generate input_example.yml/json
        # subprocess call cwtool with example.cwl input_example.yml

        retval = subprocess.run(["cwltool", "basic_example.cwl", "input_basic_example.yml"])

        if retval != 0:
            logger.fatal("ERROR: VRE NF evaluation failed. Exit value: " + str(retval))

        return retval == 0

    def run(self, input_files, input_metadata, output_files):
        """
        The main function to run the compute_metrics tool

        Parameters
        ----------
        input_files : dict
            List of input files - In this case there are no input files required
        input_metadata: dict
            Matching metadata for each of the files, plus any additional data
        output_files : dict
            List of the output files that are to be generated

        Returns
        -------
        output_files : dict
            List of files with a single entry.
        output_metadata : dict
            List of matching metadata for the returned files
        """

        # Set and check execution directory
        execution_path = os.path.abspath(self.configuration.get('execution', '.'))
        execution_parent_dir = os.path.dirname(execution_path)
        if not os.path.isdir(execution_parent_dir):
            os.makedirs(execution_parent_dir)

        # Change working dir

        print("RUN PATH: {}".format(execution_path))

        # Set file names for output files (with random name if not predefined)
        for key in output_files.keys():
            if output_files[key] is not None:
                pop_output_path = os.path.abspath(output_files[key])
            else:
                pop_output_path = os.path.join(execution_path, uuid.uuid4().hex + '.out')

            self.populable_outputs[key] = pop_output_path
            output_files[key] = pop_output_path

        # Set file names for output files (from VRE config JSON)
        # out_basename = self.configuration['out_basename']
        # out1_path = output_files.get("out1")
        # if out1_path is None:
        #     out1_path = os.path.join(execution_path, out_basename + '.out')
        # out1_path = os.path.abspath(out1_path)
        # output_files['out1'] = out1_path

        # Validate input files
        # TODO

        # Do real work: execute cwltool
        results = self.execute_cwl_workflow(input_files, self.configuration)
        results = compss_wait_on(results)

        if results is False:
            logger.fatal("VRE NF RUNNER pipeline failed. See logs")
            raise Exception("VRE NF RUNNER pipeline failed. See logs")
            return {}, {}

        # Validate output files
        # if os.path.exists(results_path):
        #     self.packDir(results_path, tar_view_path)
        #     # Redoing metrics path
        #     for metrics_file in os.listdir(results_path):
        #         if metrics_file.startswith(participant_id) and metrics_file.endswith(".json"):
        #             orig_metrics_path = os.path.join(results_path, metrics_file)
        #             shutil.copyfile(orig_metrics_path, metrics_path)
        #             break

        # Preparing the expected outputs
        # if os.path.exists(stats_path):
        #     self.packDir(stats_path, tar_nf_stats_path)

        # Initializing
        # images_file_paths = []
        # images_metadata = {
        #     'report_images': Metadata(
        #         # These ones are already known by the platform
        #         # so comment them by now
        #         data_type="report_image",
        #         file_type="IMG",
        #         file_path=images_file_paths,
        #         # Reference and golden data set paths should also be here
        #         sources=[input_metadata["input"].file_path],
        #         meta_data={
        #             "tool": "VRE_NF_RUNNER"
        #         }
        #     )
        # }
        # output_files['report_images'] = images_file_paths

        # if os.path.exists(other_path):
        #     self.packDir(other_path, tar_other_path)
        #     # Searching for image-like files
        #     for other_root, other_dirs, other_files in os.walk(other_path):
        #         for other_file in other_files:
        #             theFileType = other_file[other_file.rindex(".") + 1:].lower()
        #             if theFileType in self.IMG_FILE_TYPES:
        #                 orig_file_path = os.path.join(other_root, other_file)
        #                 new_file_path = os.path.join(execution_path, other_file)
        #                 shutil.copyfile(orig_file_path, new_file_path)
        #
        #                 # Populating
        #                 images_file_paths.append(new_file_path)

        # BEWARE: Order DOES MATTER when there is a dependency from one output on another
        # output_metadata = {
        #     "metrics": Metadata(
        #         # These ones are already known by the platform
        #         # so comment them by now
        #         data_type="assessment",
        #         file_type="JSON",
        #         file_path=metrics_path,
        #         # Reference and golden data set paths should also be here
        #         sources=[input_metadata["input"].file_path],
        #         meta_data={
        #             "tool": "VRE_NF_RUNNER"
        #         }
        #     ),
        #     "tar_view": Metadata(
        #         # These ones are already known by the platform
        #         # so comment them by now
        #         data_type="tool_statistics",
        #         file_type="TAR",
        #         file_path=tar_view_path,
        #         # Reference and golden data set paths should also be here
        #         sources=[input_metadata["input"].file_path],
        #         meta_data={
        #             "tool": "VRE_NF_RUNNER"
        #         }
        #     ),
        #     "tar_nf_stats": Metadata(
        #         # These ones are already known by the platform
        #         # so comment them by now
        #         data_type="tool_statistics",
        #         file_type="TAR",
        #         file_path=tar_nf_stats_path,
        #         # Reference and golden data set paths should also be here
        #         sources=[input_metadata["input"].file_path],
        #         meta_data={
        #             "tool": "VRE_NF_RUNNER"
        #         }
        #     ),
        #     "tar_other": Metadata(
        #         # These ones are already known by the platform
        #         # so comment them by now
        #         data_type="tool_statistics",
        #         file_type="TAR",
        #         file_path=tar_other_path,
        #         # Reference and golden data set paths should also be here
        #         sources=[input_metadata["input"].file_path],
        #         meta_data={
        #             "tool": "VRE_NF_RUNNER"
        #         }
        #     )
        # }

        # # Adding the additional interesting files
        # output_metadata.update(images_metadata)
        #
        # # And adding "fake" entries for the other output files
        # for pop_key, pop_path in self.populable_outputs.items():
        #     output_metadata[pop_key] = Metadata(
        #         file_path=pop_path,
        #         sources=[input_metadata["input"].file_path],
        #         meta_data={
        #             "tool": "VRE_NF_RUNNER"
        #         }
        #     )
        return output_files
        # return (output_files, output_metadata)
