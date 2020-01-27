#!/usr/bin/env python3
import os
import shlex
import time
from utils import logger

cwl = "https://raw.githubusercontent.com/lrodrin/vre_cwl_executor/master/tests/basic/data/workflows/basic_example.cwl"
yml = "/home/laura/PycharmProjects/vre_cwl_executor/tests/basic/input_basic_example.yml"

import subprocess

pipes = subprocess.Popen(["cwltool", cwl, yml], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

for line in iter(pipes.stderr.readline, b''):
    print(line.rstrip().decode("utf-8"))

rc = pipes.poll()
while rc is None:
    rc = pipes.poll()
    time.sleep(0.1)

if rc is not None and rc != 0:
    logger.progress(str("HELLO"), status="ERROR")
else:
    logger.progress(str("HELLO"), status="FINISHED")