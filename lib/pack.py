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
import ssl

from lib.fetch_and_validate import fetch_and_validate_cwl

# change only for OSX
ssl._create_default_https_context = ssl._create_unverified_context

from urllib import request
from shutil import copyfileobj
from cwltool.main import print_pack


def pack_cwl(cwl_wf):
    """
    Combine a workflow specified by cwl_wf made up of multiple files into single compound CWL workflow. This method
    takes all the CWL workflow files referenced by a workflow and builds a new CWL workflow with all Process objects
    (CommandLineTool and Workflow) in a list in the $graph field. Cross references (such as "run:" and "source:" fields)

    :param cwl_wf: CWL workflow
    :type cwl_wf: str
    :return: CWL serialization of the CWL workflow in JSON
    """
    try:
        # fetch and validate the CWL workflow
        loadingContext, uri, processobj = fetch_and_validate_cwl(cwl_wf)

        # CWL serialization of the CWL workflow in JSON
        packed_cwl = json.loads(print_pack(loadingContext.loader, processobj, uri, loadingContext.metadata))
        return json.dumps(packed_cwl, indent=4)

    except Exception as error:
        errstr = "Unable to pack the CWL workflow. ERROR: {}".format(error)
        raise Exception(errstr)


def validate_url(url):
    try:
        _ = request.urlopen(url)
    except Exception:
        raise AssertionError("Cannot open the provided url: {}".format(url))


def download_cwl(url, path):
    """
    Download CWL workflow from URL specified from cwl_url

    :param url: URL of CWL workflow
    :type url: str
    :param path: CWL workflows dir path
    :type path: str
    :return: downloaded CWL workflow path
    """
    global cwl_path
    try:
        validate_url(url)
        cwl_name = url.rsplit('/', 1)[-1]
        cwl_path = path + cwl_name
        if not os.path.isdir(cwl_path):
            with request.urlopen(url) as url_response, open(cwl_path, 'wb') as download_file:
                copyfileobj(url_response, download_file)

            return cwl_path

    except Exception as error:
        errstr = "Unable to download the CWL workflow. ERROR: {}".format(error)
        raise Exception(errstr)


if __name__ == '__main__':
    abspath = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
    filepath = abspath + "/tests/basic/data/workflows/"

    # file
    cwl_path = filepath + "basic_example.cwl"
    print(pack_cwl(cwl_path))

    # validate url
    cwl_url = "https://raw.githubusercontent.com/inab/vre_cwl_executor/master/tests/basic/data/workflows/basic_example_v2.cwl"
    print(pack_cwl(cwl_url))

    # validate file downloaded from url
    cwl_path = download_cwl(cwl_url, filepath)
    print(pack_cwl(cwl_path))
