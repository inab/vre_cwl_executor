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

from cwltool.main import print_pack

from lib.extract_data import fetch_and_validate_cwl


def pack_cwl(cwl_wf):
    """
    Combine a workflow specified by cwl_wf made up of multiple files into single compound CWL workflow. This method
    takes all the CWL workflow files referenced by a workflow and builds a new CWL workflow with all Process objects
    (CommandLineTool and Workflow) in a list in the $graph field. Cross references (such as "run:" and "source:" fields)

    :param cwl_wf: CWL workflow
    :type cwl_wf: str
    :return: CWL serialization of cwl_wf in JSON format
    """
    try:
        # fetch and validate the CWL workflow
        loadingContext, uri, processobj = fetch_and_validate_cwl(cwl_wf)

        # CWL serialization of the CWL workflow in JSON format
        packed_cwl = json.loads(print_pack(loadingContext.loader, processobj, uri, loadingContext.metadata))

        # save CWL packed
        with open("pack.cwl", 'w') as cwl_file:
            json.dump(packed_cwl, cwl_file, indent=2)

    except Exception as error:
        errstr = "Unable to pack the CWL workflow. ERROR: {}".format(error)
        raise Exception(errstr)


if __name__ == '__main__':
    cwl_path = "/tests/basic/data/workflows/basic_example_2.cwl"
    path = os.path.abspath(os.path.join(os.getcwd(), os.pardir)) + cwl_path

    pack_cwl(path)
