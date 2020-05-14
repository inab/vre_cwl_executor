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

import os
import re
import shutil
import ssl
import json

# change only for OSX
ssl._create_default_https_context = ssl._create_unverified_context

from urllib import request
from lib.extract_data import extract_data_from_cwl


def download_data(url, path, dependencies):
    """
    Download CWL workflow from URL specified by url and their dependencies

    :param url: remote CWL workflow
    :type url: str
    :param dependencies: CWL workflow dependencies
    :type dependencies: list
    :param path: temporal directory path
    :type path: str
    """
    try:

        if url not in dependencies:  # if main CWL workflow not in dependencies to download
            dependencies.insert(0, url)  # insert cwl workflow first position in dependencies to download

        for d in dependencies:  # for each dependency to download
            validate_url(d)  # validate url
            sub_path, sub_path_dir = create_path(d)  # create the structure for materialize the content
            if not os.path.exists(path + sub_path_dir):  # check the structure created
                os.makedirs(path + sub_path_dir)

            with request.urlopen(d) as url_response, open(path + sub_path, 'wb') as download_file:
                shutil.copyfileobj(url_response, download_file)  # download files

            # print(path + sub_path)
        print("Downloaded CWL workflow and their dependencies in {}.".format(path))

    except Exception as error:
        errstr = "Unable to download the CWL workflow and their dependencies. ERROR: {}".format(error)
        raise Exception(errstr)


def create_path(dependency):
    """
    Create paths to save CWL dependencies

    :param dependency: CWL dependency
    :type: dependency: str
    """
    try:
        global index
        if "tools/" in dependency:  # folder tools
            rule = re.search(r"\b(tools/)\b", dependency)
            index = rule.start()

        elif "workflows/" in dependency:  # folder workflow
            rule = re.search(r"\b(workflows/)\b", dependency)
            index = rule.start()

        sub_path = dependency[index:]
        sub_path_dir = os.path.dirname(dependency[index:])

        return sub_path, sub_path_dir

    except Exception:
        raise AssertionError("Cannot create path for the provided dependency: {}".format(dependency))


def validate_url(url):
    try:
        _ = request.urlopen(url)
    except Exception:
        raise AssertionError("Cannot open the provided url: {}".format(url))


if __name__ == '__main__':
    abs_url = "https://raw.githubusercontent.com/inab/vre_cwl_executor/master"

    cwl_example_1 = abs_url + "/tests/basic/data/workflows/basic_example_2.cwl"
    cwl_example_2 = abs_url + "/tests/trans_decoder/data/workflows/TransDecoder-v5-wf-2steps.cwl"

    # extract inputs, outputs, dependencies
    inputs, outputs, tools = extract_data_from_cwl(cwl_example_2)
    print("INPUTS:\n{0}\n OUTPUTS:\n{1}\n DEPENDENCIES:\n{2}".format(inputs, outputs, json.dumps(tools, indent=2)))

    # download cwl and their dependencies
    tmp_path = "/tmp/data/"
    download_data(cwl_example_2, tmp_path, tools)
