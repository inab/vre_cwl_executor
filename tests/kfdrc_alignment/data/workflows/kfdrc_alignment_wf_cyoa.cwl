cwlVersion: v1.0
class: Workflow
id: kf_alignment_cyoa_wf
doc: |-
  # KFDRC Alignment Workflow
  Workflow for the alignment or realignment of input BAMs, PE FASTQ reads, and/or SE FASTQ reads; conditionally generate gVCF and metrics.

  ![data service logo](https://github.com/d3b-center/d3b-research-workflows/raw/master/doc/kfdrc-logo-sm.png)

  This workflow is a all-in-one workflow for handling any kind of reads inputs: BAM inputs, PE reads
  and mates FASTQ inputs, SE reads FASTQ inputs,  or any combination of these. The workflow will naively attempt
  to process these depending on what you tell it you have provided. The user informs the workflow of
  which inputs to process using three boolean inputs: `run_bam_processing`, `run_pe_reads_processing`,
  and `run_se_reads_processing`. Providing `true` values for these as well their corresponding inputs
  will result in those inputs being processed.

  The second half of the workflow deals with optional gVCF creation and metrics collection.
  This workflow is capable of collecting the metrics using the following boolean flags: `run_hs_metrics`,
  `run_wgs_metrics`, and `run_agg_metrics`. To run these metrics, additional optional inputs must
  also be provided: `wxs_bait_interval_list` and `wxs_target_interval_list` for HsMetrics,
  `wgs_coverage_interval_list` for WgsMetrics. To generate the gVCF, set `run_gvcf_processing` to
  `true` and provide the following optional files: `dbsnp_vcf`, `contamination_sites_bed`,
  `contamination_sites_mu`, `contamination_sites_ud`, `wgs_calling_interval_list`, and
  `wgs_evaluation_interval_list`.

   ## Tips for running:
   1. For the fastq input file lists (PE or SE), make sure the lists are properly ordered. The items in
      the arrays are processed based on their position. These lists are dotproduct scattered. This means
      that the first file in `input_pe_reads_list` is run with the first file in `input_pe_mates_list`
      and the first string in `input_pe_rgs_list`. This also means these arrays must be the same
      length or the workflow will fail.
   1. Must have these associated indexes:
      - knownsite vcfs: Each file requires a '.tbi' index
      - reference fasta: BWA and samtools indexes ('.64.amb', '.64.ann', '.64.bwt',
          '.64.pac', '.64.sa', '.64.alt', '^.dict', '.fai')
   1. Turning off gVCF creation and metrics collection for a minimal successful run.
   1. Suggested reference inputs:
      - contamination_sites_bed: Homo_sapiens_assembly38.contam.bed
      - contamination_sites_mu: Homo_sapiens_assembly38.contam.mu
      - contamination_sites_ud: Homo_sapiens_assembly38.contam.UD
      - dbsnp_vcf: Homo_sapiens_assembly38.dbsnp138.vcf
      - indexed_reference_fasta: Homo_sapiens_assembly38.fasta
      - knownsites:
        - Homo_sapiens_assembly38.known_indels.vcf.gz
        - Mills_and_1000G_gold_standard.indels.hg38.vcf.gz
        - 1000G_phase1.snps.high_confidence.hg38.vcf.gz
        - 1000G_omni2.5.hg38.vcf.gz
      - reference_dict: Homo_sapiens_assembly38.dict


requirements:
  - class: ScatterFeatureRequirement
  - class: MultipleInputFeatureRequirement
  - class: SubworkflowFeatureRequirement

inputs:
  input_bam_list: { type: 'File[]?', doc: "List of input BAM files" }
  input_pe_reads_list: { type: 'File[]?', doc: "List of input R1 paired end fastq reads" }
  input_pe_mates_list: { type: 'File[]?', doc: "List of input R2 paired end fastq reads" }
  input_pe_rgs_list: { type: 'string[]?', doc: "List of RG strings to use in PE processing" }
  input_se_reads_list: { type: 'File[]?', doc: "List of input singlie end fastq reads" }
  input_se_rgs_list: { type: 'string[]?', doc: "List of RG strings to use in SE processing" }
  indexed_reference_fasta: { type: File, secondaryFiles: ['.64.amb', '.64.ann', '.64.bwt', '.64.pac', '.64.sa', '.64.alt', '^.dict', '.fai'], doc: "Reference fasta with BWA and samtool indexes" }
  biospecimen_name: { type: string, doc: "String name of biospcimen" }
  output_basename: { type: string, doc: "String to use as the base for output filenames" }
  reference_dict: { type: File, doc: "Dict index of the reference fasta" }
  dbsnp_vcf: { type: 'File?', doc: "dbSNP vcf file" }
  knownsites: { type: 'File[]', doc: "List of files and indexes containing known polymorphic sites used to exclude regions around known polymorphisms from analysis" }
  contamination_sites_bed: { type: 'File?', doc: ".Bed file for markers used in this analysis,format(chr\tpos-1\tpos\trefAllele\taltAllele)" }
  contamination_sites_mu: { type: 'File?', doc: ".mu matrix file of genotype matrix" }
  contamination_sites_ud: { type: 'File?', doc: ".UD matrix file from SVD result of genotype matrix" }
  wgs_calling_interval_list: { type: 'File?', doc: "WGS interval list used to aid scattering Haplotype caller" }
  wgs_coverage_interval_list: { type: 'File?', doc: "An interval list file that contains the positions to restrict the wgs metrics assessment" }
  wgs_evaluation_interval_list: { type: 'File?', doc: "Target intervals to restrict gvcf metric analysis (for VariantCallingMetrics)" }
  wxs_bait_interval_list: { type: 'File?', doc: "An interval list file that contains the locations of the WXS baits used (for HsMetrics)" }
  wxs_target_interval_list: { type: 'File?', doc: "An interval list file that contains the locations of the WXS targets (for HsMetrics)" }
  run_bam_processing: { type: boolean, doc: "BAM processing will be run. Requires: input_bam_list" }
  run_pe_reads_processing: { type: boolean, doc: "PE reads processing will be run. Requires: input_pe_reads_list, input_pe_mates_list, input_pe_rgs_list" }
  run_se_reads_processing: { type: boolean, doc: "SE reads processing will be run. Requires: input_se_reads_list, input_se_rgs_list" }
  run_hs_metrics: { type: boolean, doc: "HsMetrics will be collected. Only recommended for WXS inputs. Requires: wxs_bait_interval_list, wxs_target_interval_list" }
  run_wgs_metrics: { type: boolean, doc: "WgsMetrics will be collected. Only recommended for WGS inputs. Requires: wgs_coverage_interval_list" }
  run_agg_metrics: { type: boolean, doc: "MultipleMetrics will be collected. Warning! Very time intensive" }
  run_gvcf_processing: { type: boolean, doc: "gVCF will be generated. Requires: dbsnp_vcf, contamination_sites_bed, contamination_sites_mu, contamination_sites_ud, wgs_calling_interval_list, wgs_evaluation_interval_list" }

outputs:
  cram: {type: File, outputSource: samtools_coverttocram/output}
  gvcf: {type: 'File[]?', outputSource: generate_gvcf/gvcf}
  verifybamid_output: {type: 'File[]?', outputSource: generate_gvcf/verifybamid_output}
  bqsr_report: {type: File, outputSource: gatk_gatherbqsrreports/output}
  gvcf_calling_metrics: {type: ['null', { type: array , items: { type : array, items: File } } ], outputSource: generate_gvcf/gvcf_calling_metrics}
  aggregation_metrics: {type: ['null', { type: array , items: { type : array, items: File } } ], outputSource: picard_collectaggregationmetrics/output}
  hs_metrics: {type: 'File[]?', outputSource: picard_collecthsmetrics/output}
  wgs_metrics: {type: 'File[]?', outputSource: picard_collectwgsmetrics/output}

steps:
  gatekeeper:
    run: ../tools/gatekeeper.cwl
    in:
      run_bam_processing: run_bam_processing
      run_pe_reads_processing: run_pe_reads_processing
      run_se_reads_processing: run_se_reads_processing
      run_hs_metrics: run_hs_metrics
      run_wgs_metrics: run_wgs_metrics
      run_agg_metrics: run_agg_metrics
      run_gvcf_processing: run_gvcf_processing
    out: [scatter_bams,scatter_pe_reads,scatter_se_reads, scatter_gvcf, scatter_hs_metrics, scatter_wgs_metrics, scatter_agg_metrics]

  process_bams:
    run: ../subworkflows/kfdrc_process_bamlist.cwl
    in:
      input_bam_list: input_bam_list
      indexed_reference_fasta: indexed_reference_fasta
      sample_name: biospecimen_name
      conditional_run: gatekeeper/scatter_bams
    scatter: conditional_run
    out: [unsorted_bams] #+2 Nesting File[][][]

  process_pe_reads:
    run: ../subworkflows/kfdrc_process_pe_readslist2.cwl
    in:
      indexed_reference_fasta: indexed_reference_fasta
      input_pe_reads_list: input_pe_reads_list
      input_pe_mates_list: input_pe_mates_list
      input_pe_rgs_list: input_pe_rgs_list
      conditional_run: gatekeeper/scatter_pe_reads
    scatter: conditional_run
    out: [unsorted_bams] #+0 Nesting File[]

  process_se_reads:
    run: ../subworkflows/kfdrc_process_se_readslist2.cwl
    in:
      indexed_reference_fasta: indexed_reference_fasta
      input_se_reads_list: input_se_reads_list
      input_se_rgs_list: input_se_rgs_list
      conditional_run: gatekeeper/scatter_se_reads
    scatter: conditional_run
    out: [unsorted_bams] #+0 Nesting File[]

  sambamba_merge:
    hints:
      - class: sbg:AWSInstanceType
        value: c5.9xlarge;ebs-gp2;2048
    run: ../tools/sambamba_merge_anylist.cwl
    in:
      bams:
        source: [process_bams/unsorted_bams, process_pe_reads/unsorted_bams, process_se_reads/unsorted_bams]
        linkMerge: merge_flattened #Flattens all to File[]
      base_file_name: output_basename
    out: [merged_bam]

  sambamba_sort:
    hints:
      - class: sbg:AWSInstanceType
        value: c5.9xlarge;ebs-gp2;2048
    run: ../tools/sambamba_sort.cwl
    in:
      bam: sambamba_merge/merged_bam
      base_file_name: output_basename
    out: [sorted_bam]

  python_createsequencegroups:
    run: ../tools/python_createsequencegroups.cwl
    in:
      ref_dict: reference_dict
    out: [sequence_intervals, sequence_intervals_with_unmapped]

  gatk_baserecalibrator:
    run: ../tools/gatk_baserecalibrator.cwl
    in:
      input_bam: sambamba_sort/sorted_bam
      knownsites: knownsites
      reference: indexed_reference_fasta
      sequence_interval: python_createsequencegroups/sequence_intervals
    scatter: [sequence_interval]
    out: [output]

  gatk_gatherbqsrreports:
    run: ../tools/gatk_gatherbqsrreports.cwl
    in:
      input_brsq_reports: gatk_baserecalibrator/output
      output_basename: output_basename
    out: [output]

  gatk_applybqsr:
    run: ../tools/gatk_applybqsr.cwl
    in:
      bqsr_report: gatk_gatherbqsrreports/output
      input_bam: sambamba_sort/sorted_bam
      reference: indexed_reference_fasta
      sequence_interval: python_createsequencegroups/sequence_intervals_with_unmapped
    scatter: [sequence_interval]
    out: [recalibrated_bam]

  picard_gatherbamfiles:
    run: ../tools/picard_gatherbamfiles.cwl
    in:
      input_bam: gatk_applybqsr/recalibrated_bam
      output_bam_basename: output_basename
    out: [output]

  samtools_coverttocram:
    run: ../tools/samtools_covert_to_cram.cwl
    in:
      input_bam: picard_gatherbamfiles/output
      reference: indexed_reference_fasta
    out: [output]

  picard_collecthsmetrics:
    run: ../tools/picard_collecthsmetrics_conditional.cwl
    in:
      input_bam: picard_gatherbamfiles/output
      bait_intervals: wxs_bait_interval_list
      target_intervals: wxs_target_interval_list
      reference: indexed_reference_fasta
      conditional_run: gatekeeper/scatter_hs_metrics
    scatter: conditional_run
    out: [output]

  picard_collectwgsmetrics:
    run: ../tools/picard_collectwgsmetrics_conditional.cwl
    in:
      input_bam: picard_gatherbamfiles/output
      intervals: wgs_coverage_interval_list
      reference: indexed_reference_fasta
      conditional_run: gatekeeper/scatter_wgs_metrics
    scatter: conditional_run
    out: [output]

  picard_collectaggregationmetrics:
    run: ../tools/picard_collectaggregationmetrics_conditional.cwl
    in:
      input_bam: picard_gatherbamfiles/output
      reference: indexed_reference_fasta
      conditional_run: gatekeeper/scatter_agg_metrics
    scatter: conditional_run
    out: [output]

  generate_gvcf:
    run: ../subworkflows/kfdrc_bam_to_gvcf.cwl
    in:
      contamination_sites_bed: contamination_sites_bed
      contamination_sites_mu: contamination_sites_mu
      contamination_sites_ud: contamination_sites_ud
      input_bam: picard_gatherbamfiles/output
      indexed_reference_fasta: indexed_reference_fasta
      output_basename: output_basename
      dbsnp_vcf: dbsnp_vcf
      reference_dict: reference_dict
      wgs_calling_interval_list: wgs_calling_interval_list
      wgs_evaluation_interval_list: wgs_evaluation_interval_list
      conditional_run: gatekeeper/scatter_gvcf
    scatter: conditional_run
    out: [verifybamid_output, gvcf, gvcf_calling_metrics]


$namespaces:
  sbg: https://sevenbridges.com
hints:
  - class: 'sbg:maxNumberOfParallelInstances'
    value: 4