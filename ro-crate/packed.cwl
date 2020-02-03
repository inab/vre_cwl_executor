{
    "$graph": [
        {
            "arguments": [
                {
                    "position": 0,
                    "shellQuote": false,
                    "valueFrom": "set -eo pipefail\n\nRG_NUM=`samtools view -H $(inputs.input_bam.path) | grep -c ^@RG`\nif [ $RG_NUM != 1 ]; then\n  samtools split -f '%!.bam' -@ 36 --reference $(inputs.reference.path) $(inputs.input_bam.path)\n  rm $(inputs.input_bam.path)\nfi"
                }
            ],
            "baseCommand": [
                "/bin/bash",
                "-c"
            ],
            "class": "CommandLineTool",
            "id": "#samtools_split.cwl",
            "inputs": [
                {
                    "id": "#samtools_split.cwl/input_bam",
                    "type": "File"
                },
                {
                    "id": "#samtools_split.cwl/reference",
                    "type": "File"
                }
            ],
            "outputs": [
                {
                    "id": "#samtools_split.cwl/bam_files",
                    "outputBinding": {
                        "glob": "*.bam",
                        "outputEval": "${\n  if (self.length == 0) return [inputs.input_bam]\n  else return self\n}"
                    },
                    "type": {
                        "items": "File",
                        "type": "array"
                    }
                }
            ],
            "requirements": [
                {
                    "class": "ShellCommandRequirement"
                },
                {
                    "class": "DockerRequirement",
                    "dockerPull": "kfdrc/samtools:1.8-dev"
                },
                {
                    "class": "InlineJavascriptRequirement"
                }
            ]
        },
        {
            "class": "Workflow",
            "id": "#main",
            "inputs": [
                {
                    "id": "#main/biospecimen_name",
                    "type": "string"
                },
                {
                    "id": "#main/indexed_reference_fasta",
                    "type": "File"
                },
                {
                    "id": "#main/input_reads",
                    "type": "File"
                },
                {
                    "id": "#main/output_basename",
                    "type": "string"
                }
            ],
            "outputs": [
                {
                    "id": "#main/test",
                    "outputSource": "#main/samtools_split/bam_files",
                    "type": {
                        "items": "File",
                        "type": "array"
                    }
                }
            ],
            "requirements": [
                {
                    "class": "ScatterFeatureRequirement"
                },
                {
                    "class": "MultipleInputFeatureRequirement"
                },
                {
                    "class": "SubworkflowFeatureRequirement"
                }
            ],
            "steps": [
                {
                    "id": "#main/samtools_split",
                    "in": [
                        {
                            "id": "#main/samtools_split/input_bam",
                            "source": "#main/input_reads"
                        },
                        {
                            "id": "#main/samtools_split/reference",
                            "source": "#main/indexed_reference_fasta"
                        }
                    ],
                    "out": [
                        "#main/samtools_split/bam_files"
                    ],
                    "run": "#samtools_split.cwl"
                }
            ]
        }
    ],
    "cwlVersion": "v1.0"
}