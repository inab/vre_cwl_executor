cwlVersion: v1.0
class: Workflow
label: kf_alignment_optimized_wf
requirements:
  - class: ScatterFeatureRequirement
  - class: MultipleInputFeatureRequirement
  - class: SubworkflowFeatureRequirement

inputs:
  input_reads: File
  biospecimen_name: string
  indexed_reference_fasta: File

  test:
    type: string
    s:license: https://spdx.org/licenses/Apache-2.0
    format:
        - edam:format_12345
        - edam:format_1964

outputs:
  test:
    type: 'File[]'
    outputSource: samtools_split/bam_files
    s:license: https://spdx.org/licenses/Apache-2.0

steps:
  samtools_split:
    run: ../tools/samtools_split.cwl
    in:
      input_bam: input_reads
      reference: indexed_reference_fasta
    out: [bam_files]

$namespaces:
  edam: http://edamontology.org/
  s: https://schema.org/
$schemas:
  - http://edamontology.org/EDAM_1.18.owl