cwlVersion: v1.0
class: CommandLineTool
id: samtools_cram2bam_w_index
requirements:
  - class: ShellCommandRequirement
  - class: InlineJavascriptRequirement
  - class: ResourceRequirement
    ramMin: 4000
  - class: DockerRequirement
    dockerPull: 'kfdrc/samtools:1.8-dev'
baseCommand: [samtools, view]
arguments:
  - position: 1
    shellQuote: false
    valueFrom: >-
      -b -T $(inputs.reference.path) -o $(inputs.input_cram.path) $(inputs.output_basename).bam
      && samtools index -@ 35 $(inputs.output_basename).bam $(inputs.output_basename).bai
inputs:
  input_cram: File
  output_basename: string
  reference: File
  indexed_reference_fai: File
outputs:
  output:
    type: File
    outputBinding:
      glob: output.bam
    secondaryFiles: [^.bai]