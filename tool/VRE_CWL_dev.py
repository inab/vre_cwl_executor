#!/usr/bin/env python3

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
import os
import subprocess
import sys

from basic_modules.metadata import Metadata
from utils import logger

try:
    if hasattr(sys, '_run_from_cmdl') is True:
        raise ImportError
    from pycompss.api.parameter import FILE_IN, FILE_OUT
    from pycompss.api.task import task
    from pycompss.api.api import compss_wait_on
except ImportError:
    # logger.warn("[Warning] Cannot import \"pycompss\" API packages.")
    # logger.warn("\t\tUsing mock decorators.")

    from utils.dummy_pycompss import FILE_IN, FILE_OUT  # pylint: disable=ungrouped-imports
    from utils.dummy_pycompss import task  # pylint: disable=ungrouped-imports
    from utils.dummy_pycompss import compss_wait_on  # pylint: disable=ungrouped-imports

from basic_modules.tool import Tool


def get_CWL_workflow(cwl_wf_url, cwl_wf_tag):
    """
    Get CWL Workflow from repository specified by cwl_wf_url and cwl_wf_tag.

    :param cwl_wf_url:
    :param cwl_wf_tag:
    :return:
    """
    pass


def create_inputs_object():
    """
    Create the YAML or JSON file with the formatted description of the required input values for the given CWL Workflow.

    :return: inputs_object file
    :rtype: YAML or JSON
    """
    pass


class WF_RUNNER(Tool):
    """
    Tool for writing to a file
    """
    MASKED_KEYS = {'execution', 'project', 'description', 'cwl_wf_url', 'cwl_wf_tag'}  # arguments from config.json

    def __init__(self, configuration=None):
        """
        Init function
        """
        logger.info("VRE CWL Workflow runner")
        Tool.__init__(self)

        if configuration is None:
            configuration = {}

        self.configuration.update(configuration)

        # Arrays are serialized
        for k, v in self.configuration.items():
            if isinstance(v, list):
                self.configuration[k] = ' '.join(v)

        self.populable_outputs = {}  # TODO description

    @task(returns=bool, input_files=FILE_IN, configuration=FILE_IN, isModifier=False)
    def execute_cwl_workflow(self, input_files, configuration):  # pylint: disable=no-self-use

        # First, we need to get the CWL workflow file
        cwl_wf_url = self.configuration.get('cwl_wf_url')
        cwl_wf_tag = self.configuration.get('cwl_wf_tag')
        if (cwl_wf_url is None) or (cwl_wf_tag is None):
            logger.fatal("FATAL ERROR: both 'cwl_wf_url' and 'cwl_wf_tag' parameters must be defined")
            return False

        # TODO get CWL workflow from the construction of cwl_wf_url + cwl_wf_tag config.json arguments
        get_CWL_workflow(cwl_wf_url, cwl_wf_tag)

        # TODO create the YAML/JSON file - input_basic_example.yml
        # Parameters which are not input or output files are in the configuration
        variable_params = []
        for conf_key in self.configuration.keys():
            if conf_key not in self.MASKED_KEYS:
                variable_params.append((conf_key, self.configuration[conf_key]))

        create_inputs_object()
        cwl_wf_input_yml_path = "/home/laura/PycharmProjects/vre_cwl_executor/tests/basic/input_basic_example.yml"

        # cwltool executor for CWL Workflow # TODO change to subprocess Popen
        logger.debug("cwltool executor for CWL Workflow")
        # process = subprocess.run(["cwltool", cwl_wf_url, cwl_wf_input_yml_path])

        # TESTING
        process = subprocess.Popen(["cwltool", cwl_wf_url, cwl_wf_input_yml_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        for line in iter(process.stderr.readline, b''):
            print(line.rstrip().decode("utf-8"))

        rc = process.poll()
        while rc is None:
            rc = process.poll()
            process.sleep(0.1)

        if rc is not None and rc != 0:
            logger.progress(str("HELLO"), status="ERROR")
        else:
            logger.progress(str("HELLO"), status="FINISHED")

        # TESTING

        return process.returncode == 0

    def run(self, input_files, input_metadata, output_files):
        """
        The main function to run the compute_metrics tool.

        :param input_files: List of input files - In this case there are no input files required.
        :param input_metadata: Matching metadata for each of the files, plus any additional data.
        :param output_files: List of the output files that are to be generated.
        :type input_files: dict
        :type input_metadata: dict
        :type output_files: dict
        :return: List of files with a single entry (output_files), List of matching metadata for the returned files
        (output_metadata).
        :rtype: dict, dict
        """

        # Set and check execution directory. If not exists the directory will be created.
        execution_path = os.path.abspath(self.configuration.get('execution', '.'))
        execution_parent_dir = os.path.dirname(execution_path)
        if not os.path.isdir(execution_parent_dir):
            os.makedirs(execution_parent_dir)

        # Update working directory to execution path
        os.chdir(execution_path)
        logger.debug("Execution path: {}".format(execution_path))

        # Set file names for output files (with random name if not predefined)
        for key in output_files.keys():
            if output_files[key] is not None:
                pop_output_path = os.path.abspath(output_files[key])
                self.populable_outputs[key] = pop_output_path
                output_files[key] = pop_output_path
                # TODO consider cases to future regular expressions (dir, file, multifiles, etc.)
            else:
                # TODO validate if required True/False param output_files dict config.json.
                #  case: if True raise error else raise warning
                errstr = "The output_file[{}] can not be located. Please specify its expected path.".format(key)
                logger.error(errstr)
                raise Exception(errstr)

        logger.debug("Init execution of the CWL Workflow")
        results = self.execute_cwl_workflow(input_files, self.configuration)
        results = compss_wait_on(results)  # TODO JM ???

        results = True  # TODO temporarily. forced to not stop the execution. it should be deleted
        if results is False:
            logger.fatal("VRE CWL RUNNER pipeline failed. See logs")
            raise Exception("VRE CWL RUNNER pipeline failed. See logs")

        logger.debug("Creating output metadata")
        output_metadata = dict()
        for key in output_files.keys():
            if os.path.isfile(output_files[key]):
                meta = Metadata()
                # Set file_path for output files
                meta.file_path = output_files[key]
                # Set sources for output files
                meta_sources_list = list()
                for input_name in input_metadata.keys():
                    meta_sources_list.append(input_metadata[input_name].file_path)
                meta.sources = meta_sources_list
                # Append new element in output metadata
                output_metadata.update({key: meta})

            else:
                logger.warning("Output {} not found. Path {} not exists".format(key, output_files[key]))

        logger.debug("Output metadata created")

        return output_files, output_metadata
