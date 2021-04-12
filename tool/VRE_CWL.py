#!/usr/bin/env python

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
import json
import os
import shutil
import time

from basic_modules.tool import Tool
from utils import logger
from lib.cwl import CWL


# from pathlib2 import Path


class WF_RUNNER(Tool):
    """
    Tool for writing to a file
    """
    MASKED_KEYS = {'execution', 'project', 'description', 'cwl_wf_url'}  # arguments from config.json
    YAML_FILENAME = "inputs_cwl.yaml"
    ZIP_FILENAME = "cwl_metadata.zip"
    PROVENANCE_DIR = "cwl_metadata/"
    ROCRATE_DIR = "ro/"
    TMP_DIR = "/tmp/openvre/"
    debug_mode = False  # If is True, debug mode is active. False, otherwise

    def __init__(self, configuration=None):
        """
        Init function
        """
        logger.debug("VRE CWL Workflow runner")
        Tool.__init__(self)

        if configuration is None:
            configuration = {}

        self.configuration.update(configuration)
        self.cwl = CWL()  # CWL Workflow class
        self.cwl_wf_url = str()
        self.arguments = list()
        self.execution_path = None
        self.provenance_path = None
        self.tmp_dir = None
        self.outputs = dict()

    def execute_cwl_workflow(self, input_files, arguments):  # pylint: disable=no-self-use
        """
        The main function to run the remote CWL workflow

        :param input_files: List of input files - In this case there are no input files required.
        :type input_files: dict
        :param arguments: dict containing tool arguments
        :type arguments: dict
        """
        try:
            self.cwl_wf_url = self.configuration.get('cwl_wf_url')
            if self.cwl_wf_url is None:
                errstr = "cwl_wf_url parameter must be defined"
                logger.fatal(errstr)
                raise Exception(errstr)

            logger.debug("CWL workflow file: {}".format(self.cwl_wf_url))

            for params in self.configuration.keys():  # save arguments
                if params not in self.MASKED_KEYS:
                    self.arguments.append((params, self.configuration[params]))

            cwl_wf_input_yml_path = self.execution_path + "/" + self.YAML_FILENAME
            self.cwl.create_input_yml(input_files, arguments, cwl_wf_input_yml_path)
            logger.info("3) Packed information to YAML: {}".format(cwl_wf_input_yml_path))

            if not self.debug_mode:
                # Create temporal directory to add temporary execution files
                # If not exists the directory will be created
                self.tmp_dir = self.TMP_DIR + str(os.getpid()) + "/"
                if not os.path.isdir(self.tmp_dir):
                    os.umask(0)
                    os.makedirs(self.tmp_dir)

                # Create provenance directory to add metadata execution files
                # If not exists the directory will be created
                self.provenance_path = self.execution_path + "/" + self.PROVENANCE_DIR
                if not os.path.isdir(self.provenance_path):
                    os.makedirs(self.provenance_path)

                # cwltool execution
                process = CWL.execute_cwltool(cwl_wf_input_yml_path, self.cwl_wf_url, self.provenance_path,
                                              self.tmp_dir)

                # Sending the cwltool execution stdout to the log file
                for line in iter(process.stderr.readline, b''):
                    print(line.rstrip().decode("utf-8").replace("", " "))

                rc = process.poll()
                while rc is None:
                    rc = process.poll()
                    time.sleep(0.1)

                if rc is not None and rc != 0:
                    logger.progress("Something went wrong inside the CWL workflow execution. See logs",
                                    status="WARNING")

                else:
                    # output files from cwltool execution
                    output_execution = process.stdout.read().decode("utf-8")
                    logger.progress("CWL Workflow execution finished successfully", status="FINISHED")
                    return output_execution

        except:
            errstr = "CWL Workflow execution failed. See logs"
            logger.error(errstr)
            raise Exception(errstr)

    def run(self, input_files, input_metadata, output_files, output_metadata):
        """
        The main function to run the compute_metrics tool.

        :param input_files: List of input files - In this case there are no input files required.
        :type input_files: dict
        :param input_metadata: Matching metadata for each of the files, plus any additional data.
        :type input_metadata: dict
        :param output_files: List of the output files that are to be generated.
        :type output_files: dict
        :param output_metadata: List of matching metadata for the output files
        :type output_metadata: list
        :return: List of files with a single entry (output_files), List of matching metadata for the returned files
        (output_metadata).
        :rtype: dict, dict
        """
        try:
            # Set and validate execution path. If not exists the directory will be created
            execution_path = os.path.abspath(self.configuration.get('execution', '.'))
            self.execution_path = execution_path
            if not os.path.isdir(self.execution_path):
                os.makedirs(self.execution_path)

            # Set and validate execution parent path. If not exists the directory will be created
            execution_parent_dir = os.path.dirname(self.execution_path)
            if not os.path.isdir(execution_parent_dir):
                os.makedirs(execution_parent_dir)

            # Update working directory
            os.chdir(self.execution_path)
            logger.debug("Execution path: {}".format(self.execution_path))

            # cwltool execution
            outputs_execution = self.execute_cwl_workflow(input_files, self.configuration)

            if not self.debug_mode:
                outputs_execution = json.loads(outputs_execution)  # formatting the stdout to JSON format

                # Validate provenance data from cwltool execution
                # is_valid = self.cwl.validate_provenance(self.provenance_path)
                # if is_valid == 0:
                # logger.debug("Provenance data cwl_metadata validated")

                # Create RO-crate
                rocrate_path = self.execution_path + "/" + self.ROCRATE_DIR
                if not os.path.isdir(rocrate_path):
                    os.makedirs(rocrate_path)

                self.cwl.create_rocrate(self.cwl_wf_url, self.cwl.inputs_cwl, rocrate_path)
                logger.debug("RO-Crate created")

                # Validate RO-crate # TODO validate RO-crate

                # move YAML file and RO-Crate folder to provenance data folder
                shutil.move(self.YAML_FILENAME, self.provenance_path)
                shutil.move(rocrate_path, self.provenance_path)

                # ZIP provenance data
                self.cwl.compress_provenance(self.ZIP_FILENAME, self.provenance_path)

                # Remove provenance and temporal data folders
                shutil.rmtree(self.provenance_path)
                shutil.rmtree(self.tmp_dir)
                # for item in Path(self.tmp_dir).iterdir():
                #     if item.is_dir():
                #         os.rmdir(item)
                logger.debug("Provenance folder {} \n and temporal folder {} removed".format(self.provenance_path,
                                                                                           self.tmp_dir))

                # Create and validate the output files
                self.create_output_files(output_files, output_metadata, outputs_execution)
                logger.debug("Output files and output metadata created")

            return output_files, output_metadata

        except:
            errstr = "VRE CWL RUNNER pipeline failed. See logs"
            logger.fatal(errstr)
            raise Exception(errstr)

    def create_output_files(self, output_files, output_metadata, outputs_execution):
        """
        Create output files list

        :param output_files: List of the output files that are to be generated.
        :type output_files: dict
        :param output_metadata: List of matching metadata for the output files
        :type output_metadata: list
        param outputs_execution: List of the output files that are generated by cwltool execution.
        :type outputs_execution: dict
        :return: List of files with a single entry (output_files), List of matching metadata for the returned files
        (output_metadata).
        :rtype: dict, dict
        """
        try:
            for metadata in output_metadata:  # for each output file in output_metadata
                out_id = metadata["name"]
                pop_output_path = list()  # list of tuples (path, type of output)
                if out_id in outputs_execution.keys():  # output id in metadata in output id outputs_exec
                    if not metadata["allow_multiple"]:  # allow multiple false
                        print(metadata)
                        print(outputs_execution)
                        #file_path = outputs_execution[next(iter(outputs_execution))][0]["path"]
                        file_path = outputs_execution[out_id]["path"]
                        #file_type = outputs_execution[next(iter(outputs_execution))][0]["class"].lower()
                        file_type = outputs_execution[out_id]["class"].lower()
                        pop_output_path.append((file_path, file_type))

                    else:  # allow multiple true
                        for key_exec in outputs_execution[out_id]:
                            file_path = key_exec["path"]
                            file_type = key_exec["class"].lower()
                            pop_output_path.append((file_path, file_type))

                else:  # provenance data
                    if out_id == "cwl_metadata":
                        file_path = self.execution_path + "/" + self.ZIP_FILENAME
                        pop_output_path.append((file_path, "file"))

                output_files[out_id] = pop_output_path  # create output files
                self.outputs[out_id] = pop_output_path  # save output files

        except:
            errstr = "Output files not created. See logs"
            logger.fatal(errstr)
            raise Exception(errstr)
