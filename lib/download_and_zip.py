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
from lib.dataset import urls
from lib.extract_data import extract_data_from_cwl


def zip_dir(path, zipn):
    """
    Create zip file with CWL workflow dependencies

    :param path: path that contains CWL workflow dependencies
    :type path: str
    :param zipn: zip file name
    :type zipn: str
    """
    try:
        with zipfile.ZipFile(zipn, "w") as zipf:
            # iterate over all the files in the directory path
            for foldername, subfolders, files in os.walk(path):
                for file in files:
                    # create complete filepath of file in files
                    file_path = os.path.join(foldername, file)
                    # add filename to zip
                    zipf.write(file_path)

        print("Created zip file {} of {}.".format(zipn, path))

        print("Removed temporal dir {}.".format(path))
        shutil.rmtree(path)

    except Exception as error:
        errstr = "Unable to zip the CWL workflow and their dependencies. ERROR: {}".format(error)
        raise Exception(errstr)


def download_cwl(url, path, dependencies):
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

        if not os.path.exists(path):
            os.makedirs(path)

        if url not in dependencies:  # if main CWL workflow not in dependencies to download
            dependencies.insert(0, url)  # insert cwl workflow first position in dependencies to download

        else:

            for d in dependencies:  # for each dependency to download
                validate_url(d)
                cwl_name = d.rsplit('/', 1)[-1]

                global new_path
                if "tools/" in d:  # add tools directory
                    new_path = os.path.join(path, "tools/")

                elif "workflows/" in d:  # add workflow directory
                    new_path = os.path.join(path, "workflows/")

                if not os.path.exists(new_path):
                    os.makedirs(new_path)

                with request.urlopen(d) as url_response, open(new_path + cwl_name, 'wb') as download_file:
                    shutil.copyfileobj(url_response, download_file)

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
    cwl_url = urls["TransDecoder-v5-wf-2steps"]

    # extract inputs, outputs, dependencies
    inputs, outputs, tools = extract_data_from_cwl(cwl_url)
    print("INPUTS:\n{0}\n OUTPUTS:\n{1}\n DEPENDENCIES:\n{2}".format(inputs, outputs, json.dumps(tools, indent=4)))

    # download cwl and their dependencies
    tmppath = "/tmp/data/"
    download_cwl(cwl_url, tmppath, tools)

    # zip tmppath
    zip_dir(tmppath, "bundle.zip")
