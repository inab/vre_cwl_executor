# iPC VRE CWL Executor

Example pipelines file that is ready to run in the VRE matching the code in the HowTo documentation.

This repo structure workflows and tools can be forked and used as the base template for new tools and workflows. It should have all of the base functionality and is set up for unit testing and with pylint to ensure code clarity.

## Requirements
- Python 3.6.9+
- Python3-dev and Python3-venv
- Docker: https://docs.docker.com/get-docker/
- Python Modules:
  - pylint
  - pytest
  - mg-tool-api: https://github.com/Multiscale-Genomics/mg-tool-api.git
  - cwltool: https://github.com/common-workflow-language/cwltool.git

## Installation

Directly from GitHub:

```
cd ${HOME}/user

git clone https://github.com/inab/vre_cwl_executor.git

cd vre_cwl_executor
```

Create the Python environment

```
python3 -m venv ${HOME}/user/vre_cwl_executor/venv
source venv/bin/activate
pip install -r requirements.txt
```

## Configure

Add your ${USER} in `/tests/basic/config.json`:

```json 
"arguments": [
  {
      "name": "execution",
      "value": "/home/${USER}/vre_cwl_executor/tests/basic/run000"
  }
],
"output_files": [
  {
      "name": "bam_file",
      "required": true,
      "allow_multiple": false,
      "file": {
          "file_path": "/home/${USER}/vre_cwl_executor/tests/basic/run000/A.bam"
      }
   }
]
```
and `/tests/basic/in_metadata.json`:

```json 
{
    "_id": "unique_file_id_5e14abe0a37012.29503907",
    "file_path": "/home/${USER}/vre_cwl_executor/tests/basic/NA12878.bam"
},
{
    "_id": "unique_file_id_5e14abe0a37012.29503908",
    "file_path": "/home/${USER}/vre_cwl_executor/tests/basic/hg38.fa"
{
``` 
and `/test/basic/input_basic_example.yml`:

```yaml 
  input_reads: 
    class: File
    location: /home/{USER}/vre_cwl_executor/tests/basic/NA12878.bam
  biospecimen_name: "hg38"
  output_basename: "mytest"
  indexed_reference_fasta:
    class: File 
    location: /home/{USER}/vre_cwl_executor/tests/basic/hg38.fa
```
