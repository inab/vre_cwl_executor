# iPC VRE Workflow Executor

[![Documentation Status](https://readthedocs.org/projects/mg-process-test/badge/?version=latest)](http://mg-process-test.readthedocs.io/en/latest/?badge=latest) [![Build Status](https://travis-ci.org/Multiscale-Genomics/mg-process-test.svg?branch=master)](https://travis-ci.org/Multiscale-Genomics/mg-process-test)

Example pipelines file that is ready to run in the VRE matching the code in the HowTo documentation.

This repo structure workflows and tools can be forked and used as the base template for new tools and workflows. It should have all of the base functionality and is set up for unit testing and with pylint to ensure code clarity.

# Requirements
- pyenv and pyenv-virtualenv
- Python <= 3.6.9
- Python Modules:
  - pylint
  - pytest
  - mg-tool-api

Installation
------------

Directly from GitHub:

```
cd ${HOME}/user

git clone https://github.com/Multiscale-Genomics/mg-process-test-dev.git

cd mg-process-test-dev
```

Create the Python environment

```
pyenv-virtualenv 3.6.9 mg-process-test-dev
pyenv activate mg-process-test-dev
pip install -e .
pip install -r requirements.txt
```
