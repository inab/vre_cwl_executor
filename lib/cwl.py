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
import re
import subprocess
import sys
import zipfile

from collections import defaultdict
from ruamel import yaml
from utils import logger

import tool.VRE_CWL


class CWL:
    """
    CWL workflow class
    """
    file_type = "File"

    def __init__(self):
        """
        Init function
        """
        self.input_cwl = defaultdict(list)

    def create_input_yml(self, input_files, arguments, filename_path):
        """
        Create a YAML file containing the information of inputs from CWL workflow

        :param input_files: List containing tool input files
        :type input_files: dict
        :param arguments: Dict containing tool arguments
        :type arguments: dict
        :param filename_path: Working YAML file path directory
        :type filename_path: str
        """
        try:
            for key, value in input_files.items():  # for each input file
                if isinstance(value, str):  # one input file
                    self.input_cwl.update({key: {"class": self.file_type, "location": value}})

                elif isinstance(value, list):  # more than one input file
                    for file_path in value:
                        self.input_cwl[key].append({"class": self.file_type, "location": file_path})

            for key, value in arguments.items():  # add arguments
                if key not in tool.VRE_CWL.WF_RUNNER.MASKED_KEYS:
                    self.input_cwl[str(key)] = value

            with open(filename_path, 'w+') as f:  # create YAML file
                yaml.dump(dict(self.input_cwl), f, allow_unicode=True, default_flow_style=False)

        except:
            errstr = "The YAML file creation failed. See logs"
            logger.error(errstr)
            raise Exception(errstr)

    @staticmethod
    def execute_cwltool(cwl_wf_input_yml_path, cwl_wf_url, provenance_dir, tmp_dir):
        """
        cwltool provenance execution process with the workflow specified by cwl_wf_url and YAML file path,
        created from config.json and input_metadata.json. provenance data is created.

        :param cwl_wf_input_yml_path: CWL workflow in YAML format
        :type cwl_wf_input_yml_path: str
        :param cwl_wf_url: URL for the location of the workflow
        :type cwl_wf_url: str
        :param provenance_dir: directory to save the provenance data
        :type provenance_dir: str
        :param tmp_dir: directory to save temporal files of execution
        :type tmp_dir: str
        """
        logger.debug("Starting CWL Workflow execution")

        cmd = [
            "cwltool",
            "--tmp-outdir-prefix", tmp_dir,
            "--tmpdir-prefix", tmp_dir,
            "--provenance", provenance_dir,
            cwl_wf_url,
            cwl_wf_input_yml_path
        ]

        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return process

    @staticmethod
    def compress_provenance(filename, provenance_path):
        """
        Create ZIP file of provenance data folder

        :param filename: filename
        :type filename: str
        :param provenance_path: path that contains provenance data
        :type provenance_path: str
        """
        try:
            # with tarfile.open(filename, mode='w:gz', bufsize=1024 * 1024) as tar:
            #     print(provenance_path)
            #     tar.add(provenance_path)
            #
            # tar.close()
            with zipfile.ZipFile(filename, "w", zipfile.ZIP_DEFLATED) as zip:
                abs_src = os.path.abspath(provenance_path)  # absolute path from provenance path
                for folder_name, sub_folders, files in os.walk(provenance_path):
                    rule = re.search(r"\b(data/)\b", folder_name)
                    if rule is None:  # if not contains data folder
                        for file in files:
                            abs_name = os.path.abspath(os.path.join(folder_name, file))
                            arc_name = abs_name[len(abs_src) + 1:]
                            zip.write(abs_name, arc_name)
            zip.close()

            if not os.path.isfile(filename):  # if zip file is not created the execution stops
                sys.exit("{} not created; See logs".format(filename))

            logger.debug("Provenance data {} created".format(filename))

        except Exception as error:
            errstr = "Unable to create provenance data {}. ERROR: {}".format(filename, error)
            logger.error(errstr)
            raise Exception(errstr)
