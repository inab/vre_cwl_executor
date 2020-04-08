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
import zipfile
import shutil
import ssl
import json

# change only for OSX
ssl._create_default_https_context = ssl._create_unverified_context

from urllib import request
from shutil import copyfileobj
from lib.dataset import urls
from lib.extract_data import extract_data_from_cwl


def zip_dir(path):
    """
    Create zip file with CWL workflow dependencies

    :param path: path that contains CWL workflow dependencies
    :type path: str
    """
    try:
        zipn = "bundle.zip"
        with zipfile.ZipFile(zipn, "w") as zipf:
            # iterate over all the files in the directory path
            for foldername, subfolders, files in os.walk(path):
                for file in files:
                    # create complete filepath of file in files
                    file_path = os.path.join(foldername, file)
                    # add filename to zip
                    zipf.write(file_path)

        print("Created zip file {} of {}.".format(zipn, path))

        # remove tmp directory
        shutil.rmtree(path)

    except Exception as error:
        errstr = "Unable to save the CWL workflow dependencies. ERROR: {}".format(error)
        raise Exception(errstr)


def download_cwl(url, dependencies, path):
    """
    Download CWL workflow from URL specified by url and their dependencies

    :param url: remote CWL workflow
    :type url: str
    :param dependencies: CWL workflow dependencies
    :type dependencies: list
    :param path: temporal directory path
    :type path: str
    """
    dependencies.insert(0, cwl_url)  # insert cwl workflow first position in dependencies to download.
    try:

        if not os.path.exists(path):
            os.makedirs(path)

        for item in dependencies:
            validate_url(item)
            cwl_name = item.rsplit('/', 1)[-1]

            strts = "tools/"
            if strts in item:   # add another directory if it is needed
                new_path = os.path.join(path, strts)
                if not os.path.exists(new_path):
                    os.makedirs(new_path)

            else:
                new_path = os.path.join(path, "workflows/")
                if not os.path.exists(new_path):
                    os.makedirs(new_path)

            with request.urlopen(item) as url_response, open(new_path + cwl_name, 'wb') as download_file:
                copyfileobj(url_response, download_file)

        print("Downloaded CWL workflow dependencies in {}.".format(path))

    except Exception as error:
        errstr = "Unable to download the CWL workflow. ERROR: {}".format(error)
        raise Exception(errstr)


def validate_url(url):
    try:
        _ = request.urlopen(url)
    except Exception:
        raise AssertionError("Cannot open the provided url: {}".format(url))


if __name__ == '__main__':
    cwl_url = urls["basic_example_v2"]

    # extract inputs, outputs, dependencies
    inputs, outputs, tools = extract_data_from_cwl(cwl_url)
    print("INPUTS:\n{0}\n OUTPUTS:\n{1}\n DEPENDENCIES:\n{2}".format(inputs, outputs, json.dumps(tools, indent=4)))

    # download cwl and dependencies
    tmppath = "/tmp/data/"
    download_cwl(cwl_url, tools, tmppath)

    # zip tmppath
    zip_dir(tmppath)
