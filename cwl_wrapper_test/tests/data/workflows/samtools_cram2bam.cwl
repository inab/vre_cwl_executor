cwlVersion: v1.0
class: Workflow
id: kf-cram2bam-custom
requirements:
  - class: ScatterFeatureRequirement
  - class: MultipleInputFeatureRequirement
  - class: SubworkflowFeatureRequirement

inputs:
  input_cram: File
  output_basename: string
  indexed_reference_fasta: File

outputs:
  output: {type: File, outputSource: samtools_cram2bam/output}

steps:
  samtools_cram2bam:
    run: ../tools/samtools_cram2bam.cwl
    in:
      input_cram: input_cram
      output_basename: output_basename
      reference: indexed_reference_fasta
    out: [output]