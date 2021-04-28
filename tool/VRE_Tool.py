#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2020-2021 Barcelona Supercomputing Center (BSC), Spain
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import os
import subprocess
import time

from basic_modules.tool import Tool
from utils import logger

from cwl.workflow import Workflow


class cwlTool(Tool):
    """
    This class define CWL tool.
    """
    DEFAULT_KEYS = ['execution', 'project', 'description']  # config.json default keys
    INPUTS_FILENAME = "inputdeclarations.yaml"
    TMP_DIR = "/tmp/intermediate/"  # TODO change
    PROVENANCE_DIR = "execution_provenance/"

    def __init__(self, configuration=None):
        """
        Init function

        :param configuration: a dictionary containing parameters that define how the operation should be carried out,
        which are specific to CWL tool.
        :type configuration: dict
        """
        Tool.__init__(self)

        if configuration is None:
            configuration = {}

        self.configuration.update(configuration)

        for k, v in self.configuration.items():
            if isinstance(v, list):
                self.configuration[k] = ' '.join(v)

        # Init variables
        self.current_dir = os.path.abspath(os.path.dirname(__file__))
        self.parent_dir = os.path.abspath(self.current_dir + "/../")
        self.execution_path = self.configuration.get('execution', '.')
        if not os.path.isabs(self.execution_path):  # convert to abspath if is relpath
            self.execution_path = os.path.normpath(os.path.join(self.parent_dir, self.execution_path))

        self.arguments = dict(
            [(key, value) for key, value in self.configuration.items() if key not in self.DEFAULT_KEYS]
        )

        # Init specific variables
        self.cwl_wf = Workflow(self.parent_dir)
        self.execution_outputs = {}

    def run(self, input_files, input_metadata, output_files, output_metadata):
        """
        The main function to run the CWL tool.

        :param input_files: Dictionary of input files locations.
        :type input_files: dict
        :param input_metadata: Dictionary of files metadata.
        :type input_metadata: dict
        :param output_files: Dictionary of the output files locations. Expected to be generated.
        :type output_files: dict
        :param output_metadata: # TODO
        :type output_metadata: list
        :return: # TODO
        :rtype: dict, dict
        """
        try:
            # Set and validate execution path. If not exists the directory will be created.
            if not os.path.isdir(self.execution_path):
                os.makedirs(self.execution_path, exist_ok=True)

            # Set and validate execution parent directory. If not exists the directory will be created.
            execution_parent_dir = os.path.dirname(self.execution_path)
            if not os.path.isdir(execution_parent_dir):
                os.mkdir(execution_parent_dir)

            # Update working directory to execution path
            os.chdir(self.execution_path)

            # Tool execution
            self.toolExecution(input_files)

            if len(self.execution_outputs) != 0:
                print(self.execution_outputs)

                # # Create RO-crate
                # rocrate_path = self.execution_path + "/" + self.ROCRATE_DIR
                # if not os.path.isdir(rocrate_path):
                #     os.makedirs(rocrate_path)
                #
                # self.cwl.create_rocrate(self.cwl_wf_url, self.cwl.wf_exec_inputs, rocrate_path)
                # logger.debug("RO-Crate created")
                #
                # # Validate RO-crate # TODO validate RO-crate
                #
                # # move YAML file and RO-Crate folder to provenance data folder
                # shutil.move(self.YAML_FILENAME, self.provenance_path)
                # shutil.move(rocrate_path, self.provenance_path)
                #
                # # ZIP provenance data
                # self.cwl.compress_provenance(self.ZIP_FILENAME, self.provenance_path)
                #
                # # Remove provenance and temporal data folders
                # shutil.rmtree(self.provenance_path)
                # shutil.rmtree(self.tmp_dir)
                # # for item in Path(self.tmp_dir).iterdir():
                # #     if item.is_dir():
                # #         os.rmdir(item)
                # logger.debug("Provenance folder {} \n and temporal folder {} removed".format(self.provenance_path,
                #                                                                            self.tmp_dir))
                #
                # Modify and validate the output files from tool execution
                self.cwl_wf.createOutputsFiles(output_files, output_metadata, self.execution_outputs, self.execution_path)
                return output_files, output_metadata

            # else: TODO error handling

        except:
            errstr = "VRE CWL tool execution failed. See logs."
            logger.fatal(errstr)
            raise Exception(errstr)

    def toolExecution(self, input_files):
        """
        The main function to run the CWL tool.

        :param input_files: Dictionary of input files locations.
        :type input_files: dict
        """
        output = None
        error = None
        rc = None
        try:
            # Check cwl_wf_url argument
            cwl_wf_url = self.arguments.get("cwl_wf_url")  # TODO add tag
            if cwl_wf_url is None:
                errstr = "cwl_wf_url argument must be defined"
                logger.fatal(errstr)
                raise Exception(errstr)

            # Create YAML file
            cwl_wf_yaml_filename = os.path.join(self.execution_path, self.INPUTS_FILENAME)
            self.cwl_wf.createYAMLFile(input_files, self.arguments, cwl_wf_yaml_filename)

            # cwltool execution
            if os.path.isfile(cwl_wf_yaml_filename):
                # Create temporal directory to add intermediate execution files
                # If not exists the directory will be created
                tmp_dir = self.TMP_DIR + str(os.getpid()) + "/"
                os.makedirs(tmp_dir, exist_ok=True)

                # Create provenance directory to add provenance execution files
                # If not exists the directory will be created
                # provenance_dir = os.path.join(self.execution_path, self.PROVENANCE_DIR)
                # os.makedirs(provenance_dir, exist_ok=True)

                cmd = [
                    'cwltool',
                    '--singularity',
                    "--tmpdir-prefix", tmp_dir,
                    "--tmp-outdir-prefix", tmp_dir,
                    cwl_wf_url,
                    cwl_wf_yaml_filename
                ]

                process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

                # Sending the stdout to the log file
                for line in iter(process.stderr.readline, b''):
                    print(line.rstrip().decode("utf-8").replace("", " "))

                rc = process.poll()
                while rc is None:
                    rc = process.poll()
                    time.sleep(0.1)

                if rc is not None and rc != 0:
                    logger.progress("Something went wrong inside the cwltool execution. See logs.", status="WARNING")
                else:
                    logger.progress("The cwltool execution finished successfully.", status="FINISHED")

                # Save execution outputs from cwltool execution
                output, error = process.communicate()
                self.execution_outputs = json.loads(output)

        except:
            errstr = "The cwltool execution failed. See logs."
            logger.error(errstr)
            if rc is not None:
                logger.error("RETVAL: {}".format(rc))
            if output is not None:
                logger.error("STDOUT: " + output.decode("utf-8", errors="ignore"))
            if error is not None:
                logger.error("STDERR: " + error.decode("utf-8", errors="ignore"))
            raise Exception(errstr)
