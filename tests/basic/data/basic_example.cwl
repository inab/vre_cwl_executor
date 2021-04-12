cwlVersion: v1.0
class: Workflow

requirements:
  - class: ScatterFeatureRequirement
  - class: MultipleInputFeatureRequirement
  - class: SubworkflowFeatureRequirement

inputs:
  input_reads: File
  biospecimen_name: string
  indexed_reference_fasta: File

outputs:
  bam_files: {type: 'File[]', outputSource: samtools_split/bam_files}

steps:
  samtools_split:
    run: samtools_split.cwl
    in:
      input_bam: input_reads
      reference: indexed_reference_fasta
    out: [bam_files]
