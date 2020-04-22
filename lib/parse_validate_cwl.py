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

from lib.dataset import urls
from lib.download_and_zip import download_cwl, zip_dir
from lib.extract_data import extract_data_from_cwl


def parse_and_validate_cwl(url):
    """
        - Fetch, validate and resolve
        - Extract inputs, outputs and dependencies
        - Download and zip

    :param url: remote CWL workflow
    :type url: str
    """
    try:
        # get inputs, ouputs and dependencies from CWL workflow
        inputs, outputs, tools = extract_data_from_cwl(url)
        print("INPUTS:\n{0}\n OUTPUTS:\n{1}\n DEPENDENCIES:\n{2}".format(inputs, outputs, json.dumps(tools, indent=4)))

        # download and zip dependencies from CWL workflow
        tmppath = "/tmp/data/"
        download_cwl(url, tmppath, tools)
        zip_dir(tmppath, "bundle.zip")

    except Exception as error:
        errstr = "Unable to parse and validate the CWL workflow. ERROR: {}".format(error)
        raise Exception(errstr)


if __name__ == '__main__':
    cwl_url = urls["basic_example_v2"]
    parse_and_validate_cwl(cwl_url)
