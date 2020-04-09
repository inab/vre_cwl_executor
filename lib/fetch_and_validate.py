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

from cwltool.load_tool import fetch_document
from cwltool.load_tool import resolve_and_validate_document

from lib.dataset import urls


def fetch_and_validate_cwl(cwl_wf):
    """
    Retrieve and validate a CWL workflow specified by cwl_wf

    :param cwl_wf: CWL workflow
    :type cwl_wf: str
    """
    try:
        # fetch CWL workflow
        loadingContext, workflowobj, uri = fetch_document(cwl_wf)
        loadingContext.do_update = False

        # validate CWL workflow
        loadingContext, uri = resolve_and_validate_document(loadingContext, workflowobj, uri)
        processobj = loadingContext.loader.resolve_ref(uri)[0]
        print("{} is valid CWL.".format(cwl_wf))
        return loadingContext, uri, processobj  # need to pack

    except Exception as error:
        errstr = "Unable to fetch and validate the CWL workflow. ERROR: {}".format(error)
        raise Exception(errstr)


if __name__ == '__main__':
    # abspath = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
    # localpath = abspath + "/tests/basic/data/workflows/"

    # validate local cwl
    # cwl_path = localpath + "basic_example_v2.cwl"
    # print(fetch_and_validate_cwl(cwl_path))

    # validate remote cwl
    cwl_url = urls["basic_example_v2"]
    print(fetch_and_validate_cwl(cwl_url))
