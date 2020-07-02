{
  "$graph": [
    {
      "class": "CommandLineTool",
      "id": "#samtools_split.cwl",
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
      ],
      "baseCommand": [
        "/bin/sh",
        "-c"
      ],
      "arguments": [
        {
          "position": 0,
          "shellQuote": false,
          "valueFrom": "set -eo pipefail\n\nRG_NUM=`samtools view -H $(inputs.input_bam.path) | grep -c ^@RG`\nif [ $RG_NUM != 1 ]; then\n  samtools split -f '%!.bam' -@ 36 --reference $(inputs.reference.path) $(inputs.input_bam.path)\n  # rm $(inputs.input_bam.path)\nfi"
        }
      ],
      "inputs": [
        {
          "type": "File",
          "id": "#samtools_split.cwl/input_bam"
        },
        {
          "type": "File",
          "id": "#samtools_split.cwl/reference"
        }
      ],
      "outputs": [
        {
          "type": {
            "type": "array",
            "items": "File"
          },
          "outputBinding": {
            "glob": "*.bam",
            "outputEval": "${\n  if (self.length == 0) return [inputs.input_bam]\n  else return self\n}"
          },
          "id": "#samtools_split.cwl/bam_files"
        }
      ]
    },
    {
      "class": "Workflow",
      "label": "kf_alignment_optimized_wf",
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
      "inputs": [
        {
          "type": "string",
          "id": "#main/biospecimen_name"
        },
        {
          "type": "File",
          "id": "#main/indexed_reference_fasta"
        },
        {
          "type": "File",
          "id": "#main/input_reads"
        }
      ],
      "outputs": [
        {
          "type": {
            "type": "array",
            "items": "File"
          },
          "outputSource": "#main/samtools_split/bam_files",
          "id": "#main/test"
        }
      ],
      "steps": [
        {
          "run": "#samtools_split.cwl",
          "in": [
            {
              "source": "#main/input_reads",
              "id": "#main/samtools_split/input_bam"
            },
            {
              "source": "#main/indexed_reference_fasta",
              "id": "#main/samtools_split/reference"
            }
          ],
          "out": [
            "#main/samtools_split/bam_files"
          ],
          "id": "#main/samtools_split"
        }
      ],
      "id": "#main"
    }
  ],
  "cwlVersion": "v1.0"
}