# iPC VRE CWL Executor

Example pipelines file that is ready to run in the VRE matching the code in the HowTo documentation.

This repo structure workflows and tools can be forked and used as the base template for new tools and workflows. It should have all of the base functionality and is set up for unit testing and with pylint to ensure code clarity.

## Requirements

* Install the dependencies used by the Wrapper.

```bash
sudo apt update
sudo apt install git
sudo apt install docker-ce
```

Remember to add your username to the `docker` group.

 ```bash
 sudo usermod -a -G docker $USER
 ```
 
* Install the Wrapper dependencies.

    - Python 3.6 or +
    - Python3.6-pip, Python3.6-dev and Python3.6-venv or +
    - mg-tool-api: https://github.com/Multiscale-Genomics/mg-tool-api.git
    - cwltool: https://github.com/common-workflow-language/cwltool.git

## Installation

Directly from GitHub:

```bash
cd ${HOME}

git clone https://github.com/inab/vre_cwl_executor.git

cd vre_cwl_executor
```

Create the Python environment

```bash
python3 -m venv ${HOME}/vre_cwl_executor/venv
source venv/bin/activate
pip install -r requirements.txt
```

## Run the Wrapper
```bash
./VRE_CWL_RUNNER --config tests/basic/config.json --in_metadata tests/basic/in_metadata.json --out_metadata out_metadata.json --log_file VRE_CWL_RUNNER.log
```

