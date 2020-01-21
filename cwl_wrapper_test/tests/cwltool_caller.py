#!/usr/bin/env python3

cwl = "https://raw.githubusercontent.com/lrodrin/vre-process_cwl-executor/master/cwl_wrapper_test/tests/data" \
      "/workflows/basic_example.cwl"
yml = "/home/laura/PycharmProjects/vre-process_cwl-executor/cwl_wrapper_test/tests" \
      "/input_basic_example.yml"

from subprocess import Popen, PIPE, CalledProcessError

with Popen(["cwltool", cwl, yml], stdout=PIPE, bufsize=1, universal_newlines=True) as p:
    for line in p.stdout:
        print(line, end='')
#
# if p.returncode != 0:
#     raise CalledProcessError(p.returncode, p.args)