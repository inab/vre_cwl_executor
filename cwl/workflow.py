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

import glob
import os
import shutil
from collections import defaultdict
from urllib import parse

from rocrate import rocrate
from ruamel import yaml
from utils import logger


class Workflow:
    """
    Workflow class
    """

    def __init__(self):
        """
        Init function
        """
        self.type = "cwl"

        self.current_dir = os.path.abspath(os.path.dirname(__file__))
        self.parent_dir = os.path.abspath(self.current_dir + "/../")
        self.provenance_path = "execution_crate"

    def createYAMLFile(self, input_files, arguments, filename):
        """
        Method to create YAML file that describes the execution inputs of the workflow
        needed for their execution.

        :param input_files: Dictionary of input files locations.
        :type input_files: dict
        :param arguments: Dictionary of input arguments.
        :type arguments: dict
        :param filename: YAML filename
        :type filename: str
        """
        try:
            wf_exec_inputs = defaultdict(list)

            for k_in, v_in in input_files.items():
                file_type = "File"
                file_keys = ["class", "location"]

                if not os.path.isabs(v_in):  # if input file path is not an absolute path
                    v_in = os.path.join(self.parent_dir, v_in)

                if isinstance(v_in, str):
                    wf_exec_inputs.update({k_in: {file_keys[0]: file_type, file_keys[1]: v_in}})

                elif isinstance(v_in, list):
                    for file_path in v_in:
                        wf_exec_inputs[k_in].append({file_keys[0]: file_type, file_keys[1]: file_path})

            for k_arg, v_arg in arguments.items():
                if k_arg != "cwl_wf_url":
                    # if isinstance(v_arg, list): TODO specific read_goup argument
                    #     new_value = [item.replace("\t", "\\t") for item in v_arg]
                    #     # mapping special char inside argument list
                    #
                    wf_exec_inputs[k_arg] = v_arg

            if len(wf_exec_inputs) != 0:
                with open(filename, 'w+', encoding="utf-8") as yaml_file:
                    yaml.dump(dict(wf_exec_inputs), yaml_file, allow_unicode=True, default_flow_style=False)
            else:
                errstr = "Dictionary of execution inputs is empty"
                logger.error(errstr)
                raise Exception(errstr)

        except:
            errstr = "Cannot create YAML file {}. See logs.".format(filename)
            logger.error(errstr)
            raise Exception(errstr)

    @staticmethod
    def createOutputsFiles(output_files, output_metadata, outputs_execution, execution_path):
        """
        Create and validate output files generated for workflow execution

        :param output_files: Dictionary of the output files locations.
        :type output_files: dict
        :param output_metadata: # TODO
        :type output_metadata: list
        :param outputs_execution: TODO
        :type outputs_execution: dict
        :param execution_path: Working directory.
        :type execution_path: str
        """
        try:
            for metadata in output_metadata:
                out_id = metadata["name"]
                out_data_type = metadata["file"]["data_type"]
                out_keys = ["class", "path"]
                outputs = list()  # list of tuples (path, type of output)
                if out_id in outputs_execution.keys():
                    if not metadata["allow_multiple"]:  # allow multiple false
                        file_path = None
                        file_type = None
                        if isinstance(outputs_execution[out_id], list):  # list of files    # TODO check case
                            file_path = outputs_execution[next(iter(outputs_execution))][0][out_keys[1]]
                            file_type = outputs_execution[next(iter(outputs_execution))][0][out_keys[0]].lower()
                        elif isinstance(outputs_execution, dict):  # file
                            file_path = outputs_execution[out_id][out_keys[1]]
                            file_type = outputs_execution[out_id][out_keys[0]].lower()

                        outputs.append((file_path, file_type))

                    else:  # allow multiple true
                        for key_exec in outputs_execution[out_id]:
                            file_path = key_exec[out_keys[1]]
                            file_type = key_exec[out_keys[0]].lower()
                            outputs.append((file_path, file_type))

                else:  # execution provenance
                    if out_data_type == "provenance_data":
                        file_path = glob.glob(execution_path + "/*.zip")[0]
                        outputs.append((file_path, "file"))

                output_files[out_id] = outputs

        except:
            errstr = "Cannot create output files. See logs."
            logger.fatal(errstr)
            raise Exception(errstr)

    def createResearchObject(self, wf_url, input_files, execution_path, wf_yaml):
        """"
        Create RO-crate from execution provenance

        :param wf_url: Remote workflow location.
        :type wf_url: str
        :param input_files: Dictionary of input files locations.
        :type input_files: dict
        :param execution_path: Working directory
        :type execution_path: str
        :param wf_yaml: YAML filename
        :type wf_yaml: str
        """
        try:

            # Create RO-Crate
            wf_crate = rocrate.ROCrate()
            wf_file = wf_crate.add_workflow(wf_url, fetch_remote=True, main=True)

            # FIXME: What to do when workflow is in git repository different from GitHub???
            parsed_wf_url = parse.urlparse(wf_url)
            if parsed_wf_url.netloc == "raw.githubusercontent.com":
                # TODO convert raw url to normal url
                # parsed_repo_url = os.path.dirname(wf_url)
                wf_file.properties()['url'] = wf_url
                # wf_file.properties()['codeRepository'] = parsed_repo_url
                # wf_crate.isBasedOn = parsed_repo_url
            else:
                logger.error("FIXME: Unsupporterd http(s) git repository {}".format(parsed_wf_url))

            # Add inputs provenance to RO-crate
            for in_id, in_value in input_files.items():
                # FIXME: What to do when allow multiple == true ???
                in_localPath = os.path.join(self.parent_dir, in_value)
                if os.path.isfile(in_localPath):
                    properties = {
                        'name': in_id,
                        'url': in_localPath
                    }
                    wf_crate.add_file(source=in_localPath, properties=properties)
                elif os.path.isdir(in_localPath):
                    logger.error("FIXME: input directory / dataset handling in RO-Crate")
                else:
                    pass  # TODO raise Exception

            wf_crate_path = os.path.join(execution_path, self.provenance_path)
            wf_crate.writeCrate(wf_crate_path)

            # Add inputs declarations YAML file
            shutil.move(wf_yaml, self.provenance_path)

            # Compress RO-crate
            shutil.make_archive(self.provenance_path, "zip", wf_crate_path)
            shutil.rmtree(wf_crate_path)

        except:
            errstr = "Cannot create RO-Crate. See logs."
            logger.error(errstr)
            raise Exception(errstr)
