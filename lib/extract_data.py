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

from cwltool.load_tool import make_tool
from cwltool.workflow import default_make_tool

from lib.get_and_validate import fetch_and_validate_cwl, download_cwl


def extract_data_from_cwl(cwl_url):
    """
    Get inputs, outputs and list of tools from CWL.
    """
    tools = list()
    loadingContext, uri, processobj = fetch_and_validate_cwl(cwl_url)
    cwl_document = make_tool(uri, loadingContext)

    inputs = json.dumps(cwl_document.inputs_record_schema["fields"], indent=4)
    outputs = json.dumps(cwl_document.outputs_record_schema["fields"], indent=4)

    for item in cwl_document.metadata["steps"]:
        [tools.append(item[key]) for key in item.keys() if key == "run"]

    return inputs, outputs, tools


if __name__ == '__main__':
    basic_cwl_url = "https://raw.githubusercontent.com/inab/vre_cwl_executor/master/tests/basic/data/workflows/basic_example_v2.cwl"
    cwl_url = "https://raw.githubusercontent.com/inab/vre_cwl_executor/master/tests/trans_decoder/data/workflows/TransDecoder-v5-wf-2steps.cwl"
    cwl_demo = "https://raw.githubusercontent.com/inab/Wetlab2Variations/eosc-life/cwl-workflows/demonstrator/workflow_localfiles.cwl"

    inputs, outputs, tools = extract_data_from_cwl(cwl_demo)
    print("INPUTS:\n{0}\n OUTPUTS:\n{1}\n TOOLS:\n{2}".format(inputs, outputs, json.dumps(tools, indent=4)))

    filepath = os.path.expanduser("~") + "/workflows/"
    if not os.path.isdir(filepath):
        os.makedirs(filepath)

    for cwl in tools:
        download_cwl(cwl, filepath)
