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
import re
import requests
import ssl

# change only for OSX
ssl._create_default_https_context = ssl._create_unverified_context

from lib.download_data import download_data

abs_path = "/Users/laurarodrigueznavas/BSC/vre_cwl_executor/"
ro_path = abs_path + "tests/trans_decoder/data/ro-crate-metadata.jsonld"
ro_crate = json.loads(open(ro_path, encoding="utf-8").read())


class Metadata:

    def __init__(self, identifier):
        self.id = identifier

    @staticmethod
    def find_entity(identifier):
        for item in ro_crate["@graph"]:
            if item.get("@id", None) == identifier:
                return item  # CWL workflow


if __name__ == '__main__':
    meta = Metadata("./")
    url = meta.find_entity(meta.id)["url"]
    elements = meta.find_entity(meta.id)["hasPart"]

    rule = re.search(r"\b(workflows/)\b", url)
    index = rule.start()
    abs_path = url[:index]
    sub_path = url[index:]

    dependencies = list()
    for elem in elements:
        if "workflows" in elem["@id"] or "tools" in elem["@id"]:
            path = abs_path + elem["@id"]
            user = path.split("/")[3]
            project = path.split("/")[4]

            url_raw = 'https://api.github.com/repos/{}/{}/contents/{}'.format(user, project, elem["@id"])
            print(url_raw)

            req = requests.get(url_raw)
            if req.status_code == requests.codes.ok:
                req = req.json()
                dependencies.append(req["download_url"])
            else:
                print('Content was not found.')

    # download cwl and their dependencies
    tmppath = "/tmp/data/"
    download_data(dependencies[0], tmppath, dependencies)


