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
from cwlprov.tool import *

_logger = logging.getLogger(__name__)


def validate_provenance(args=None):
    """
    CWLProv tool to validate and inspect CWLProv Research Objects
    that capture workflow runs executed in CWL implementation
    """
    with Tool(args) as tool:
        try:
            return tool.main()

        except OSError as e:
            _logger.fatal(e)
            return Status.IO_ERROR


if __name__ == '__main__':
    provenance_folder = "/Users/laurarodrigueznavas/BSC/vre_cwl_executor/tests/basic/run000/cwl_metadata"
    validate_provenance(["-d", provenance_folder, "validate"])
