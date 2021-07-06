#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2020-2021 Barcelona Supercomputing Center (BSC), Spain
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
import sys

from utils import logger
from apps.jsonapp import JSONApp
from tool.VRE_Tool import cwlTool


class Wrapper:
    """
    Functions for wrapping the tool set up and execution.
    """

    configuration = {}
    output = {}

    def __init__(self, configuration=None):
        """
        Initialise the tool with its configuration.

        :param configuration: a dictionary containing parameters that define how the operation should be carried out,
        which are specific to CWL tool.
        :type configuration: dict
        """
        if configuration is None:
            configuration = {}

        self.configuration.update(configuration)

    def run(self, input_files, input_metadata, output_files, output_metadata):
        """
        Main run function for running CWL tool.

        :param input_files: Dictionary of input files locations.
        :type input_files: dict
        :param input_metadata: Dictionary of files metadata.
        :type input_metadata: dict
        :param output_files: Dictionary of the output files locations expected to be generated.
        :type output_files: dict
        :param output_metadata: # TODO
        :type output_metadata: list
        :return: # TODO
        :rtype: dict, dict
        """
        try:
            tt_handle = cwlTool(self.configuration)
            tt_files, tt_meta = tt_handle.run(input_files, input_metadata, output_files, output_metadata)
            return tt_files, tt_meta

        except Exception as error:
            errstr = "Tool CWL wasn't executed successfully. ERROR: {}".format(error)
            logger.error(errstr)
            raise Exception(errstr)


def main_wrapper(config_path, in_metadata_path, out_metadata_path):
    """
    Main function.

    This function launches the tool using configuration written in two json files: config.json and in_metadata.json.

    :param config_path: path to a valid VRE JSON file containing information on how the tool should be executed.
    :type config_path: str
    :param in_metadata_path: path to a valid VRE JSON file containing information on tool inputs.
    :type in_metadata_path: str
    :param out_metadata_path: path to write the JSON file containing information on tool outputs.
    :type out_metadata_path: str
    :return: If result is True, execution finished successfully. False, otherwise.
    :rtype: bool
    """
    try:
        app = JSONApp()

        result = app.launch(Wrapper, config_path, in_metadata_path, out_metadata_path)
        logger.progress("Tool successfully executed; see " + out_metadata_path)
        return result

    except Exception as error:
        errstr = "Tool wasn't successfully executed. ERROR: {}".format(error)
        logger.error(errstr)
        raise Exception(errstr)


if __name__ == "__main__":
    PARSER = argparse.ArgumentParser(description="VRE CWL Tool")
    PARSER.add_argument("--config", help="Configuration file", required=True)
    PARSER.add_argument("--in_metadata", help="Location of input metadata file", required=True)
    PARSER.add_argument("--out_metadata", help="Location of output metadata file", required=True)
    PARSER.add_argument("--log_file", help="Location of the log file", required=False)

    ARGS = PARSER.parse_args()

    CONFIG = ARGS.config
    IN_METADATA = ARGS.in_metadata
    OUT_METADATA = ARGS.out_metadata

    if ARGS.log_file:
        sys.stderr = sys.stdout = open(ARGS.log_file, "w")

    RESULTS = main_wrapper(CONFIG, IN_METADATA, OUT_METADATA)
