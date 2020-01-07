cwlVersion: v1.0
class: Workflow
id: test
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
  test: {type: 'File[]', outputSource: bwa_mem/aligned_bams}

steps:
  samtools_split:
    run: ../tools/samtools_split.cwl
    in:
      input_bam: input_reads
      reference: indexed_reference_fasta
    out: [bam_files]

  bwa_mem:
    run: ../workflows/kfdrc_bwamem_subwf.cwl
    in:
      input_reads: samtools_split/bam_files
      indexed_reference_fasta: indexed_reference_fasta
      sample_name: biospecimen_name
    scatter: [input_reads]
    out: [aligned_bams]

#$namespaces:
  #sbg: https://sevenbridges.com
#hints:
  #- class: 'sbg:AWSInstanceType'
    #value: c4.8xlarge;ebs-gp2;850
  #- class: 'sbg:maxNumberOfParallelInstances'
    #value: 4
