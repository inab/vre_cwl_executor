cwlVersion: v1.0
class: CommandLineTool
id: samtools_bam2cram
requirements:
  - class: ShellCommandRequirement
  - class: InlineJavascriptRequirement
  - class: ResourceRequirement
    ramMin: 4000
  - class: DockerRequirement
    dockerPull: 'kfdrc/samtools:1.8-dev'
baseCommand: [samtools, index]
arguments:
  - position: 1
    shellQuote: false
    valueFrom: >-
      $(inputs.input_bam.path) $(inputs.input_bam.path).bai
      && samtools view -C $(inputs.input_bam.path) -T $(inputs.reference.path) -o $(inputs.output_basename).cram

      # samtools faidx hg38.fa

inputs:
  input_bam: File
  output_basename: string
  reference: File
outputs:
  output:
    type: File
    outputBinding:
      glob: '*.cram'