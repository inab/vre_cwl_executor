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
import re

# change only for OSX
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

from urllib import request
from shutil import copyfileobj
from lib.download_and_zip import download_cwl
from lib.extract_data import extract_data_from_cwl

ro_path = "/Users/laurarodrigueznavas/BSC/vre_cwl_executor/ro_crate/test/basic/data/ro-crate-metadata.jsonld"
schema_path = "/Users/laurarodrigueznavas/BSC/vre_cwl_executor/ro_crate/test/basic/data/schema.jsonld"

ro_crate = json.loads(open(ro_path, encoding="utf-8").read())
schema = json.loads(open(schema_path, encoding="utf-8").read())
schema_map = dict((e["@id"], e) for e in schema["@graph"])


class Metadata:

    def __init__(self, identifier):
        self.id = identifier

    @staticmethod
    def find_entity(identifier):
        for item in ro_crate["@graph"]:
            if item.get("@id", None) == identifier:
                return item


meta = Metadata("./")
url = meta.find_entity(meta.id)["url"]
name = os.path.basename(meta.find_entity(meta.id)["mainEntity"]["@id"])
print(name)
elements = meta.find_entity(meta.id)["hasPart"]
a = re.search(r"\b(workflows)\b", url)
index = a.start()

dependencies = list()
for elem in elements:
    if "workflows" in elem["@id"] or "tools" in elem["@id"]:
        dependencies.append(url[:index] + elem["@id"])
# print(dependencies)

print("https://raw.githubusercontent.com/EBI-Metagenomics/workflow-is-cwl/master/workflows/TransDecoder-v5-wf-2steps.cwl")

import requests


url = 'https://api.github.com/repos/EBI-Metagenomics/workflow-is-cwl/contents/workflows/TransDecoder-v5-wf-2steps.cwl'
req = requests.get(url)
if req.status_code == requests.codes.ok:
    req = req.json()  # the response is a JSON
    print(req["download_url"])
else:
    print('Content was not found.')






