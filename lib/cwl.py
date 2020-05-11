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
import os
import subprocess
import sys
import tarfile

from ruamel import yaml
from utils import logger

import tool.VRE_CWL


class CWL:
    """
    CWL workflow class
    """

    def __init__(self):
        """
        Init function
        """
        self.input_cwl = dict()

    def create_input_yml(self, input_metadata, arguments, filename_path):
        """
        Create a YAML file containing the information of inputs from CWL workflow

        :param input_metadata: Matching metadata for each of the files, plus any additional data.
        :type input_metadata: dict
        :param arguments: dict containing tool arguments
        :type arguments: dict
        :param filename_path: Working YAML file path directory
        :type filename_path: str
        """
        try:
            for key, value in input_metadata.items():  # add metadata inputs
                data_type = value[0]
                if data_type == "file":  # mapping
                    data_type = data_type.replace("f", "F")

                file_path = str(value[1].file_path)
                self.input_cwl.update({key: {"class": data_type, "location": file_path}})

            for key, value in arguments.items():  # add arguments
                if key not in tool.VRE_CWL.WF_RUNNER.MASKED_KEYS:
                    self.input_cwl[str(key)] = str(value)

            with open(filename_path, 'w+') as f:  # create YAML file
                yaml.dump(self.input_cwl, f, allow_unicode=True, default_flow_style=False)

        except:
            errstr = "The YAML file creation failed. See logs"
            logger.error(errstr)
            raise Exception(errstr)

    @staticmethod
    def execute_cwltool(cwl_wf_input_yml_path, cwl_wf_url, tmp_dir):
        """
        cwltool provenance execution process with the workflow specified by cwl_wf_url and YAML file path,
        created from config.json and input_metadata.json. provenance data is created.

        :param cwl_wf_input_yml_path: CWL workflow in YAML format
        :type cwl_wf_input_yml_path: str
        :param cwl_wf_url: URL for the location of the workflow
        :type cwl_wf_url: str
        :param tmp_dir: directory to save the provenance data
        :type tmp_dir: str
        """
        logger.debug("Starting CWL Workflow execution")
        process = subprocess.Popen(["cwltool", "--provenance", tmp_dir, cwl_wf_url, cwl_wf_input_yml_path],
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        return process

    @staticmethod
    def compress_provenance(filename, provenance_path):
        """
        Create TAR file of provenance data folder

        :param filename: filename
        :type filename: str
        :param provenance_path: path that contains provenance data
        :type provenance_path: str
        """
        try:
            with tarfile.open(filename, mode='w:gz', bufsize=1024 * 1024) as tar:
                tar.add(provenance_path, arcname="data", recursive=True)

            tar.close()

            if not os.path.isfile(filename):  # if tar file is not created the execution stops
                sys.exit("{} not created; See logs".format(filename))

            logger.debug("Provenance data {} created".format(filename))

        except Exception as error:
            errstr = "Unable to create provenance data {}. ERROR: {}".format(filename, error)
            logger.error(errstr)
            raise Exception(errstr)

        # with zipfile.ZipFile(filename, "w") as zip:
        #     # iterate over all the files in the directory path
        #     for folder_name, sub_folders, files in os.walk(provenance_path):
        #         for file in files:
        #             file_path = os.path.join(folder_name, file)  # create complete file path of file in files
        #             zip.write(file_path)  # add filename to zip
        # zip.close()
