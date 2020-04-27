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
import shutil
import subprocess
import zipfile

from ruamel import yaml
from utils import logger

import tool.VRE_CWL


class CWL:
    """
    VRE CWL workflow class.
    """
    def __init__(self):
        """
        Init function
        """
        logger.debug("VRE CWL Workflow class")
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

            with open(filename_path, 'w+') as f:
                yaml.dump(self.input_cwl, f, allow_unicode=True, default_flow_style=False)

        except:
            errstr = "The YAML file creation failed. See logs"
            logger.error(errstr)
            raise Exception(errstr)

    @staticmethod
    def execute_cwltool(cwl_wf_input_yml_path, cwl_wf_url, tmp_dir):
        """
        cwltool execution process with the workflow specified by cwl_wf_url and YAML file path cwl_wf_input_yml_path
        specified by cwl_wf_input_yml_path, created from config.json and input_metadata.json.

        :param cwl_wf_input_yml_path: CWL workflow in YAML format
        :type cwl_wf_input_yml_path: str
        :param cwl_wf_url: URL for the location of the workflow
        :type cwl_wf_url: str
        :param tmp_dir: directory to save temporally the provenance data
        :type tmp_dir: str
        """
        # TODO try and except
        logger.debug("Starting cwltool execution")
        process = subprocess.Popen(["cwltool", "--provenance", tmp_dir, cwl_wf_url, cwl_wf_input_yml_path],
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        return process

    @staticmethod
    def zip_dir(path, zipn):
        """
        Create zip file from provenance data

        :param path: path that contains provenance data
        :type path: str
        :param zipn: zip file name
        :type zipn: str
        """
        # TODO move method to utils.py
        try:
            with zipfile.ZipFile(zipn, "w") as zipf:
                # iterate over all the files in the directory path
                for foldername, subfolders, files in os.walk(path):
                    for file in files:
                        file_path = os.path.join(foldername, file)  # create complete file path of file in files
                        zipf.write(file_path)  # add filename to zip

            logger.debug("Created zip file {} of {}.".format(zipn, path))

            # remove path of provenance data
            shutil.rmtree(path)
            logger.debug("Removed temporal directory {}.".format(path))

        except Exception as error:
            errstr = "Unable to zip the path {}. ERROR: {}".format(path, error)
            logger.error(errstr)
            raise Exception(errstr)
