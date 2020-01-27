# iPC VRE CWL Executor

Example pipelines file that is ready to run in the VRE matching the code in the HowTo documentation.

This repo structure workflows and tools can be forked and used as the base template for new tools and workflows. It should have all of the base functionality and is set up for unit testing and with pylint to ensure code clarity.

## Requirements
- Python 3.6.9+
- Python3.6-venv
- Python Modules:
  - pylint
  - pytest
  - mg-tool-api: https://github.com/Multiscale-Genomics/mg-tool-api.git
  - cwltool: https://github.com/common-workflow-language/cwltool.git

Installation
------------

Directly from GitHub:

```
cd ${HOME}/user

git clone https://github.com/inab/vre_cwl_executor.git

cd vre_cwl_executor
```

Create the Python environment

```
python3 -m venv .
source venv/bin/activate
pip install -r requirements.txt
```
