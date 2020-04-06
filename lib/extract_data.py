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
from __future__ import absolute_import

import json
import os
import zipfile
import shutil

from cwltool.load_tool import make_tool
from cwltool.workflow import default_make_tool

from lib.fetch_and_validate import fetch_and_validate_cwl, download_cwl


def extract_data_from_cwl(cwlUrl):
    """
    Get inputs, outputs and list of tools from CWL.

    :param cwlUrl: URL of CWL document
    :type cwlUrl: str
    :return: inputs, outputs and list of CWL workflow dependencies
    :rtype: list, list, list
    """
    try:
        tools_list = list()
        loadingContext, uri, processobj = fetch_and_validate_cwl(cwlUrl)
        cwl_document = make_tool(uri, loadingContext)

        inputs_list = json.dumps(cwl_document.inputs_record_schema["fields"], indent=4)
        outputs_list = json.dumps(cwl_document.outputs_record_schema["fields"], indent=4)

        for item in cwl_document.metadata["steps"]:
            [tools_list.append(item[key]) for key in item.keys() if key == "run"]

        return inputs_list, outputs_list, tools_list

    except Exception as error:
        errstr = "Unable to extract inputs, outputs and the CWL workflow dependencies. ERROR: {}".format(error)
        raise Exception(errstr)


def save_cwl_data(path, files):
    """
    Download CWL workflow dependencies.

    :param path:
    :type path: str
    :param files: CWL workflow dependencies
    :type files: list
    """
    try:
        if not os.path.isdir(path):
            os.makedirs(path)

        # download CWL workflow dependencies
        for cwl in files:
            download_cwl(cwl, path)

        # create zip file of path
        with zipfile.ZipFile("bundle.zip", "w") as zipf:
            # iterate over all the files in the directory path
            for foldername, subfolders, files in os.walk(path):
                for file in files:
                    # create complete filepath of file in files
                    file_path = os.path.join(foldername, file)
                    # add filename to zip
                    zipf.write(file_path)

        # remove tmp directory
        shutil.rmtree(path)

    except Exception as error:
        errstr = "Unable to save the CWL workflow dependencies. ERROR: {}".format(error)
        raise Exception(errstr)


if __name__ == '__main__':
    basic_cwl_url = "https://raw.githubusercontent.com/inab/vre_cwl_executor/master/tests/basic/data/workflows/basic_example_v2.cwl"
    cwl_url = "https://raw.githubusercontent.com/inab/vre_cwl_executor/master/tests/trans_decoder/data/workflows/TransDecoder-v5-wf-2steps.cwl"
    cwl_demo = "https://raw.githubusercontent.com/inab/Wetlab2Variations/eosc-life/cwl-workflows/demonstrator/workflow_localfiles.cwl"

    # extract data from CWL
    inputs, outputs, tools = extract_data_from_cwl(cwl_demo)
    print("INPUTS:\n{0}\n OUTPUTS:\n{1}\n TOOLS:\n{2}".format(inputs, outputs, json.dumps(tools, indent=4)))

    # compress data into zip file
    filepath = "/tmp/workflows/"
    save_cwl_data(filepath, tools)
