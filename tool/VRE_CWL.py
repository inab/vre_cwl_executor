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
import sys
import tarfile
import time

from basic_modules.tool import Tool
from utils import logger
from lib.cwl import CWL


class WF_RUNNER(Tool):
    """
    Tool for writing to a file
    """
    MASKED_KEYS = {'execution', 'project', 'description', 'cwl_wf_url'}  # arguments from config.json
    YAML_FILENAME = "inputs_cwl.yml"
    # ZIP_METADATA_FILENAME = "cwl_metadata.zip"
    TAR_FILENAME = "cwl_metadata.tar.gz"
    TMP_DIR = "/tmp/cwl_metadata/"

    def __init__(self, configuration=None):
        """
        Init function
        """
        logger.debug("VRE CWL Workflow runner")
        Tool.__init__(self)

        if configuration is None:
            configuration = {}

        self.configuration.update(configuration)

        # Arrays are serialized
        for k, v in self.configuration.items():
            if isinstance(v, list):
                self.configuration[k] = ' '.join(v)

        self.cwl = CWL()  # CWL workflow class
        self.arguments = list()
        self.execution_path = str()
        self.populable_outputs = dict()

    def execute_cwl_workflow(self, input_metadata, arguments, working_directory):  # pylint: disable=no-self-use
        """
        The main function to run the remote CWL workflow

        :param input_metadata: Matching metadata for each of the files, plus any additional data.
        :type input_metadata: dict
        :param arguments: dict containing tool arguments
        :type arguments: dict
        :param working_directory: Execution working path directory
        :type working_directory: str
        """
        try:
            cwl_wf_url = self.configuration.get('cwl_wf_url')  # TODO add tag
            if cwl_wf_url is None:
                errstr = "cwl_wf_url parameter must be defined"
                logger.fatal(errstr)
                raise Exception(errstr)

            logger.debug("CWL workflow file: {}". format(cwl_wf_url))

            for params in self.configuration.keys():  # save arguments
                if params not in self.MASKED_KEYS:
                    self.arguments.append((params, self.configuration[params]))

            cwl_wf_input_yml_path = working_directory + "/" + self.YAML_FILENAME
            self.cwl.create_input_yml(input_metadata, arguments, cwl_wf_input_yml_path)
            logger.info("3) Packed information to YAML: {}".format(cwl_wf_input_yml_path))

            # Create temporal directory to add provenance data. If not exists the directory will be created
            if not os.path.isdir(self.TMP_DIR):
                os.makedirs(self.TMP_DIR)

            # cwltool execution
            process = CWL.execute_cwltool(cwl_wf_input_yml_path, cwl_wf_url, self.TMP_DIR)

            # Sending the cwltool execution stdout to the log file
            for line in iter(process.stderr.readline, b''):
                print(line.rstrip().decode("utf-8").replace("", " "))

            rc = process.poll()
            while rc is None:
                rc = process.poll()
                time.sleep(0.1)

            if rc is not None and rc != 0:
                logger.progress("Something went wrong inside the cwltool execution. See logs", status="WARNING")

            else:
                # output files from cwltool execution
                output_files = process.stdout.read().decode("utf-8")
                logger.progress("CWL Workflow execution finished successfully", status="FINISHED")
                return output_files

        except:
            errstr = "The cwltool execution failed. See logs"
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
            self.execution_path = execution_path  # save execution path
            if not os.path.isdir(execution_path):
                os.makedirs(execution_path)

            # Set and validate execution parent path. If not exists the directory will be created
            execution_parent_dir = os.path.dirname(execution_path)
            if not os.path.isdir(execution_parent_dir):
                os.makedirs(execution_parent_dir)

            # Update working directory
            os.chdir(execution_path)
            logger.debug("Execution path: {}".format(execution_path))

            # cwltool execution
            logger.debug("Initialise CWL Workflow execution")
            outputs_execution = self.execute_cwl_workflow(input_metadata, self.configuration, execution_path)
            outputs_execution = json.loads(outputs_execution)  # formatting the stdout

            # Compress provenance data
            if os.path.isdir(self.TMP_DIR):
                # self.cwl.zip_dir(self.TMP_DIR, self.ZIP_METADATA_FILENAME)
                # move YAML to cwl_metadata
                shutil.move(self.YAML_FILENAME, self.TMP_DIR)

                with tarfile.open(self.TAR_FILENAME, "w:gz") as tar:
                    tar.add(self.TMP_DIR, arcname=os.path.basename(self.TMP_DIR))

                if not os.path.isfile(self.TAR_FILENAME):
                    sys.exit("{} not created; See logs".format(self.TAR_FILENAME))

                logger.debug("Provenance data: {}".format(self.TAR_FILENAME))

                # Remove path of provenance data
                shutil.rmtree(self.TMP_DIR)

            else:
                logger.debug("{} not created")
                # TODO change to logger fatal ?

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
        # TODO much control
        try:
            for metadata in output_metadata:  # for each output file in output_metadata
                out_id = metadata["name"]
                pop_output_path = list()  # list of tuples (path, type of output)
                if out_id in outputs_execution.keys():  # output id in metadata in output id outputs_exec
                    if not metadata["allow_multiple"]:  # allow multiple false
                        # pop_output_path.append(os.path.abspath(outputs_exec[key]))
                        file_path = outputs_execution[next(iter(outputs_execution))][0]["path"]
                        file_type = outputs_execution[next(iter(outputs_execution))][0]["class"].lower()
                        pop_output_path.append((file_path, file_type))

                    else:  # allow multiple true
                        for key_exec in outputs_execution[out_id]:
                            file_path = key_exec["path"]
                            file_type = key_exec["class"].lower()
                            pop_output_path.append((file_path, file_type))

                else:  # provenance data
                    if out_id == "cwl_metadata":
                        file_path = self.execution_path + "/" + self.TAR_FILENAME
                        file_type = "file"  # TODO always a file ?
                        pop_output_path.append((file_path, file_type))

                output_files[out_id] = pop_output_path  # create output files
                self.populable_outputs[out_id] = pop_output_path  # save output files

        except:
            errstr = "Output files not created. See logs"
            logger.fatal(errstr)
            raise Exception(errstr)
