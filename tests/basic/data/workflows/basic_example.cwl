cwlVersion: v1.0
class: Workflow
id: kf_alignment_optimized_wf
requirements:
  - class: ScatterFeatureRequirement
  - class: MultipleInputFeatureRequirement
  - class: SubworkflowFeatureRequirement

inputs:
  input_reads: File
  biospecimen_name: string
  output_basename: string
  indexed_reference_fasta: File

outputs:
  test: {type: 'File[]', outputSource: samtools_split/bam_files}

steps:
  samtools_split:
    run: ../tools/samtools_split.cwl
    in:
      input_bam: input_reads
      reference: indexed_reference_fasta
    out: [bam_files]
