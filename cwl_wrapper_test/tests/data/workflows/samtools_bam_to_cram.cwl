cwlVersion: v1.0
class: Workflow
id: kf-bam2cram-custom
requirements:
  - class: ScatterFeatureRequirement
  - class: MultipleInputFeatureRequirement
  - class: SubworkflowFeatureRequirement

inputs:
  input_bam: File
  output_basename: string
  indexed_reference_fasta: File

outputs:
  cram: {type: File, outputSource: samtools_cram_to_bam/output}

steps:
  samtools_cram_to_bam:
    run: ../tools/samtools_bam_to_cram.cwl
    in:
      input_bam: input_bam
      output_basename: output_basename
      reference: indexed_reference_fasta
    out: [output]