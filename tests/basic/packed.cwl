{
    "cwlVersion": "v1.0", 
    "$graph": [
        {
            "class": "CommandLineTool", 
            "requirements": [
                {
                    "class": "InlineJavascriptRequirement"
                }, 
                {
                    "class": "DockerRequirement", 
                    "dockerPull": "quay.io/biocontainers/bwa:0.7.17--h84994c4_5"
                }, 
                {
                    "class": "InitialWorkDirRequirement", 
                    "listing": [
                        {
                            "entry": "$(inputs.reference_genome)"
                        }
                    ]
                }, 
                {
                    "class": "ResourceRequirement", 
                    "outdirMin": 10500, 
                    "tmpdirMin": 10500
                }
            ], 
            "hints": [
                {
                    "class": "ResourceRequirement", 
                    "ramMin": 4000, 
                    "coresMin": 1
                }
            ], 
            "baseCommand": [
                "bwa", 
                "index"
            ], 
            "inputs": [
                {
                    "type": [
                        "null", 
                        "string"
                    ], 
                    "inputBinding": {
                        "prefix": "-a"
                    }, 
                    "doc": "BWT construction algorithm: bwtsw or is (Default: auto)\n", 
                    "id": "#bwa-index.cwl/algorithm"
                }, 
                {
                    "type": [
                        "null", 
                        "int"
                    ], 
                    "inputBinding": {
                        "position": 2, 
                        "prefix": "-b"
                    }, 
                    "id": "#bwa-index.cwl/block_size"
                }, 
                {
                    "type": "File", 
                    "inputBinding": {
                        "position": 4
                    }, 
                    "id": "#bwa-index.cwl/reference_genome"
                }
            ], 
            "outputs": [
                {
                    "type": "File", 
                    "outputBinding": {
                        "glob": "*.fa"
                    }, 
                    "secondaryFiles": [
                        ".amb", 
                        ".ann", 
                        ".bwt", 
                        ".pac", 
                        ".sa"
                    ], 
                    "id": "#bwa-index.cwl/output"
                }
            ], 
            "id": "#bwa-index.cwl"
        }, 
        {
            "class": "CommandLineTool", 
            "baseCommand": [
                "bwa", 
                "mem", 
                "-M", 
                "-p"
            ], 
            "requirements": [
                {
                    "class": "InlineJavascriptRequirement"
                }, 
                {
                    "class": "MultipleInputFeatureRequirement"
                }, 
                {
                    "class": "DockerRequirement", 
                    "dockerPull": "quay.io/biocontainers/bwa:0.7.17--h84994c4_5"
                }, 
                {
                    "class": "ResourceRequirement", 
                    "outdirMin": 10500, 
                    "tmpdirMin": 10700
                }
            ], 
            "hints": [
                {
                    "class": "ResourceRequirement", 
                    "coresMin": 4, 
                    "ramMin": 4000
                }
            ], 
            "inputs": [
                {
                    "id": "#bwa-mem.cwl/trimmed_fastq", 
                    "type": "File", 
                    "inputBinding": {
                        "position": 4
                    }
                }, 
                {
                    "id": "#bwa-mem.cwl/reference_genome", 
                    "type": "File", 
                    "inputBinding": {
                        "position": 3
                    }, 
                    "secondaryFiles": [
                        ".amb", 
                        ".ann", 
                        ".bwt", 
                        ".pac", 
                        ".sa"
                    ]
                }, 
                {
                    "id": "#bwa-mem.cwl/sample_name", 
                    "type": "string"
                }, 
                {
                    "id": "#bwa-mem.cwl/threads", 
                    "type": [
                        "null", 
                        "string"
                    ], 
                    "default": "2", 
                    "inputBinding": {
                        "position": 1, 
                        "prefix": "-t"
                    }, 
                    "doc": "-t INT        number of threads [1]"
                }, 
                {
                    "id": "#bwa-mem.cwl/read_group", 
                    "type": "string", 
                    "default": "@RG\\\\tID:H947YADXX\\\\tSM:NA12878\\\\tPL:ILLUMINA", 
                    "inputBinding": {
                        "position": 2, 
                        "prefix": "-R"
                    }
                }
            ], 
            "stdout": "$(inputs.sample_name).sam", 
            "arguments": [
                {
                    "position": 2, 
                    "prefix": "-M"
                }, 
                {
                    "position": 2, 
                    "prefix": "-p"
                }
            ], 
            "outputs": [
                {
                    "id": "#bwa-mem.cwl/aligned_sam", 
                    "type": "File", 
                    "outputBinding": {
                        "glob": "*.sam"
                    }
                }
            ], 
            "id": "#bwa-mem.cwl"
        }, 
        {
            "class": "CommandLineTool", 
            "baseCommand": [
                "curl"
            ], 
            "doc": "transfer file from a remote FTP/HTTP server to the TES", 
            "requirements": [
                {
                    "class": "DockerRequirement", 
                    "dockerPull": "jlaitinen/lftpalpine"
                }, 
                {
                    "class": "ResourceRequirement", 
                    "tmpdirMin": 2500, 
                    "outdirMin": 2500
                }
            ], 
            "hints": [
                {
                    "class": "ResourceRequirement", 
                    "coresMin": 2, 
                    "ramMin": 2000
                }
            ], 
            "inputs": [
                {
                    "type": "File", 
                    "inputBinding": {
                        "prefix": "-K", 
                        "separate": true, 
                        "position": 1
                    }, 
                    "id": "#curl.cwl/curl_config_file"
                }
            ], 
            "outputs": [
                {
                    "type": {
                        "type": "array", 
                        "items": "File"
                    }, 
                    "outputBinding": {
                        "glob": "*.gz"
                    }, 
                    "id": "#curl.cwl/in_files"
                }
            ], 
            "id": "#curl.cwl"
        }, 
        {
            "class": "CommandLineTool", 
            "baseCommand": [
                "curl"
            ], 
            "doc": "transfer file from a remote FTP/HTTP server to the TES", 
            "requirements": [
                {
                    "class": "DockerRequirement", 
                    "dockerPull": "jlaitinen/lftpalpine"
                }, 
                {
                    "class": "ResourceRequirement", 
                    "tmpdirMin": 500, 
                    "outdirMin": 500
                }
            ], 
            "hints": [
                {
                    "class": "ResourceRequirement", 
                    "coresMin": 2, 
                    "ramMin": 2000
                }
            ], 
            "inputs": [
                {
                    "type": "File", 
                    "inputBinding": {
                        "prefix": "-K", 
                        "separate": true, 
                        "position": 1
                    }, 
                    "id": "#curl_indels.cwl/curl_config_file"
                }
            ], 
            "outputs": [
                {
                    "type": "File", 
                    "outputBinding": {
                        "glob": "*.vcf"
                    }, 
                    "id": "#curl_indels.cwl/known_indels_file"
                }
            ], 
            "id": "#curl_indels.cwl"
        }, 
        {
            "class": "CommandLineTool", 
            "baseCommand": [
                "curl"
            ], 
            "doc": "transfer file from a remote FTP/HTTP server to the TES", 
            "requirements": [
                {
                    "class": "DockerRequirement", 
                    "dockerPull": "jlaitinen/lftpalpine"
                }, 
                {
                    "class": "ResourceRequirement", 
                    "tmpdirMin": 2500, 
                    "outdirMin": 2500
                }
            ], 
            "hints": [
                {
                    "class": "ResourceRequirement", 
                    "coresMin": 2, 
                    "ramMin": 2000
                }
            ], 
            "inputs": [
                {
                    "type": "File", 
                    "inputBinding": {
                        "prefix": "-K", 
                        "separate": true, 
                        "position": 1
                    }, 
                    "id": "#curl_known_sites.cwl/curl_config_file"
                }
            ], 
            "outputs": [
                {
                    "type": "File", 
                    "outputBinding": {
                        "glob": "*.gz"
                    }, 
                    "id": "#curl_known_sites.cwl/known_sites_file"
                }
            ], 
            "id": "#curl_known_sites.cwl"
        }, 
        {
            "class": "CommandLineTool", 
            "id": "#cutadapt-v.1.18.cwl", 
            "requirements": [
                {
                    "class": "InlineJavascriptRequirement"
                }, 
                {
                    "class": "DockerRequirement", 
                    "dockerPull": "quay.io/biocontainers/cutadapt:1.18--py36h14c3975_1"
                }, 
                {
                    "class": "ResourceRequirement", 
                    "outdirMin": 2500, 
                    "tmpdirMin": 2500
                }
            ], 
            "hints": [
                {
                    "class": "ResourceRequirement", 
                    "coresMin": 4, 
                    "ramMin": 4000
                }
            ], 
            "baseCommand": [
                "cutadapt", 
                "--interleaved"
            ], 
            "arguments": [
                {
                    "position": 4, 
                    "prefix": "-o", 
                    "valueFrom": "$(inputs.raw_sequences[0].basename + \".trimmed.fastq.gz\")"
                }, 
                {
                    "position": 3, 
                    "prefix": "--overlap", 
                    "valueFrom": "6"
                }, 
                {
                    "position": 1, 
                    "prefix": "-j", 
                    "valueFrom": "0"
                }, 
                {
                    "position": 2, 
                    "prefix": "--error-rate", 
                    "valueFrom": "0.2"
                }
            ], 
            "inputs": [
                {
                    "id": "#cutadapt-v.1.18.cwl/raw_sequences", 
                    "type": {
                        "type": "array", 
                        "items": "File"
                    }, 
                    "inputBinding": {
                        "position": 20, 
                        "prefix": "", 
                        "separate": false
                    }
                }, 
                {
                    "id": "#cutadapt-v.1.18.cwl/adaptors_file", 
                    "type": [
                        "null", 
                        "File"
                    ], 
                    "inputBinding": {
                        "position": 10, 
                        "prefix": "-a"
                    }
                }
            ], 
            "outputs": [
                {
                    "id": "#cutadapt-v.1.18.cwl/trimmed_fastq", 
                    "type": "File", 
                    "outputBinding": {
                        "glob": "*.trimmed.fastq.gz"
                    }
                }
            ], 
            "label": "cutadapt"
        }, 
        {
            "class": "CommandLineTool", 
            "id": "#gatk-base_recalibration.cwl", 
            "requirements": [
                {
                    "class": "InlineJavascriptRequirement"
                }, 
                {
                    "class": "DockerRequirement", 
                    "dockerPull": "broadinstitute/gatk3:3.6-0"
                }, 
                {
                    "class": "InitialWorkDirRequirement", 
                    "listing": [
                        {
                            "entry": "$(inputs.reference_genome)"
                        }, 
                        {
                            "entry": "$(inputs.dict)"
                        }
                    ]
                }, 
                {
                    "class": "ResourceRequirement", 
                    "outdirMin": 7500, 
                    "tmpdirMin": 7700
                }
            ], 
            "hints": [
                {
                    "class": "ResourceRequirement", 
                    "coresMin": 4, 
                    "ramMin": 4000
                }
            ], 
            "baseCommand": [
                "java", 
                "-jar", 
                "/usr/GenomeAnalysisTK.jar", 
                "-T", 
                "BaseRecalibrator"
            ], 
            "inputs": [
                {
                    "id": "#gatk-base_recalibration.cwl/reference_genome", 
                    "type": "File", 
                    "inputBinding": {
                        "position": 1, 
                        "prefix": "-R"
                    }, 
                    "secondaryFiles": [
                        ".fai"
                    ]
                }, 
                {
                    "id": "#gatk-base_recalibration.cwl/dict", 
                    "type": "File"
                }, 
                {
                    "id": "#gatk-base_recalibration.cwl/unzipped_known_sites_file", 
                    "type": "File"
                }, 
                {
                    "id": "#gatk-base_recalibration.cwl/input", 
                    "type": "File", 
                    "inputBinding": {
                        "position": 2, 
                        "prefix": "-I"
                    }, 
                    "secondaryFiles": [
                        "^.bai"
                    ]
                }, 
                {
                    "id": "#gatk-base_recalibration.cwl/known_indels_file", 
                    "type": "File"
                }, 
                {
                    "id": "#gatk-base_recalibration.cwl/threads", 
                    "type": [
                        "null", 
                        "string"
                    ]
                }
            ], 
            "arguments": [
                {
                    "position": 0, 
                    "prefix": "-dt", 
                    "valueFrom": "NONE"
                }, 
                {
                    "position": 0, 
                    "prefix": "-nct", 
                    "valueFrom": "$(inputs.threads)"
                }, 
                {
                    "position": 0, 
                    "prefix": "--knownSites", 
                    "valueFrom": "$(inputs.known_indels_file)"
                }, 
                {
                    "position": 0, 
                    "prefix": "--knownSites", 
                    "valueFrom": "$(inputs.unzipped_known_sites_file)"
                }, 
                {
                    "position": 3, 
                    "prefix": "-o", 
                    "valueFrom": "$(inputs.input.nameroot).recalibrated.grp"
                }
            ], 
            "outputs": [
                {
                    "id": "#gatk-base_recalibration.cwl/br_model", 
                    "type": "File", 
                    "outputBinding": {
                        "glob": "*.grp"
                    }
                }
            ], 
            "label": "gatk3-base_recalibration"
        }, 
        {
            "class": "CommandLineTool", 
            "id": "#gatk-base_recalibration_print_reads.cwl", 
            "requirements": [
                {
                    "class": "InlineJavascriptRequirement"
                }, 
                {
                    "class": "DockerRequirement", 
                    "dockerPull": "broadinstitute/gatk3:3.6-0"
                }, 
                {
                    "class": "InitialWorkDirRequirement", 
                    "listing": [
                        {
                            "entry": "$(inputs.reference_genome)"
                        }, 
                        {
                            "entry": "$(inputs.dict)"
                        }, 
                        {
                            "entry": "$(inputs.br_model)"
                        }
                    ]
                }, 
                {
                    "class": "ResourceRequirement", 
                    "outdirMin": 7500, 
                    "tmpdirMin": 7700
                }
            ], 
            "hints": [
                {
                    "class": "ResourceRequirement", 
                    "coresMin": 8, 
                    "ramMin": 8000
                }
            ], 
            "baseCommand": [
                "java", 
                "-jar", 
                "/usr/GenomeAnalysisTK.jar", 
                "-T", 
                "PrintReads"
            ], 
            "inputs": [
                {
                    "id": "#gatk-base_recalibration_print_reads.cwl/reference_genome", 
                    "type": "File", 
                    "inputBinding": {
                        "position": 1, 
                        "prefix": "-R"
                    }, 
                    "secondaryFiles": [
                        ".fai"
                    ]
                }, 
                {
                    "id": "#gatk-base_recalibration_print_reads.cwl/dict", 
                    "type": "File"
                }, 
                {
                    "id": "#gatk-base_recalibration_print_reads.cwl/input", 
                    "type": [
                        "File"
                    ], 
                    "inputBinding": {
                        "position": 2, 
                        "prefix": "-I"
                    }, 
                    "secondaryFiles": [
                        "^.bai"
                    ]
                }, 
                {
                    "id": "#gatk-base_recalibration_print_reads.cwl/br_model", 
                    "type": [
                        "File"
                    ], 
                    "inputBinding": {
                        "position": 4, 
                        "prefix": "-BQSR"
                    }
                }
            ], 
            "arguments": [
                {
                    "position": 0, 
                    "prefix": "-dt", 
                    "valueFrom": "NONE"
                }, 
                {
                    "position": 3, 
                    "prefix": "-o", 
                    "valueFrom": "$(inputs.input.nameroot).bqsr.bam"
                }
            ], 
            "outputs": [
                {
                    "id": "#gatk-base_recalibration_print_reads.cwl/bqsr_bam", 
                    "type": "File", 
                    "outputBinding": {
                        "glob": "$(inputs.input.nameroot).bqsr.bam"
                    }, 
                    "secondaryFiles": [
                        "^.bai"
                    ]
                }
            ], 
            "label": "gatk-base_recalibration_print_reads"
        }, 
        {
            "class": "CommandLineTool", 
            "id": "#gatk-haplotype_caller.cwl", 
            "requirements": [
                {
                    "class": "InlineJavascriptRequirement"
                }, 
                {
                    "class": "DockerRequirement", 
                    "dockerPull": "broadinstitute/gatk3:3.6-0"
                }, 
                {
                    "class": "InitialWorkDirRequirement", 
                    "listing": [
                        {
                            "entry": "$(inputs.reference_genome)"
                        }, 
                        {
                            "entry": "$(inputs.dict)"
                        }
                    ]
                }, 
                {
                    "class": "ResourceRequirement", 
                    "outdirMin": 7500, 
                    "tmpdirMin": 7700
                }
            ], 
            "hints": [
                {
                    "class": "ResourceRequirement", 
                    "coresMin": 4, 
                    "ramMin": 4000
                }
            ], 
            "baseCommand": [
                "java", 
                "-jar", 
                "/usr/GenomeAnalysisTK.jar", 
                "-T", 
                "HaplotypeCaller", 
                "--never_trim_vcf_format_field"
            ], 
            "inputs": [
                {
                    "id": "#gatk-haplotype_caller.cwl/reference_genome", 
                    "type": "File", 
                    "inputBinding": {
                        "position": 1, 
                        "prefix": "-R"
                    }, 
                    "secondaryFiles": [
                        ".fai"
                    ]
                }, 
                {
                    "id": "#gatk-haplotype_caller.cwl/dict", 
                    "type": "File"
                }, 
                {
                    "id": "#gatk-haplotype_caller.cwl/input", 
                    "type": "File", 
                    "inputBinding": {
                        "position": 2, 
                        "prefix": "-I"
                    }, 
                    "secondaryFiles": [
                        "^.bai"
                    ]
                }, 
                {
                    "id": "#gatk-haplotype_caller.cwl/chromosome", 
                    "type": [
                        "null", 
                        "string"
                    ], 
                    "inputBinding": {
                        "position": 3, 
                        "prefix": "-L"
                    }
                }, 
                {
                    "id": "#gatk-haplotype_caller.cwl/ploidy", 
                    "type": [
                        "null", 
                        "int"
                    ], 
                    "inputBinding": {
                        "position": 5, 
                        "prefix": "-ploidy"
                    }
                }, 
                {
                    "id": "#gatk-haplotype_caller.cwl/gqb", 
                    "type": [
                        "null", 
                        {
                            "type": "array", 
                            "items": "int", 
                            "inputBinding": {
                                "prefix": "--GVCFGQBands"
                            }
                        }
                    ], 
                    "inputBinding": {
                        "position": 12
                    }
                }, 
                {
                    "id": "#gatk-haplotype_caller.cwl/threads", 
                    "type": [
                        "null", 
                        "string"
                    ], 
                    "default": "2"
                }
            ], 
            "arguments": [
                {
                    "position": 0, 
                    "prefix": "--num_cpu_threads_per_data_thread", 
                    "valueFrom": "$(inputs.threads)"
                }, 
                {
                    "position": 0, 
                    "prefix": "-dt", 
                    "valueFrom": "NONE"
                }, 
                {
                    "position": 0, 
                    "prefix": "-rf", 
                    "valueFrom": "BadCigar"
                }, 
                {
                    "position": 0, 
                    "prefix": "-ERC", 
                    "valueFrom": "GVCF"
                }, 
                {
                    "position": 0, 
                    "prefix": "-variant_index_type", 
                    "valueFrom": "LINEAR"
                }, 
                {
                    "position": 0, 
                    "prefix": "-variant_index_parameter", 
                    "valueFrom": "128000"
                }, 
                {
                    "position": 0, 
                    "prefix": "-o", 
                    "valueFrom": "$(inputs.input.nameroot).vcf.gz"
                }
            ], 
            "outputs": [
                {
                    "id": "#gatk-haplotype_caller.cwl/gvcf", 
                    "type": "File", 
                    "outputBinding": {
                        "glob": "*.gz"
                    }, 
                    "secondaryFiles": [
                        ".tbi"
                    ]
                }
            ], 
            "label": "gatk3-haplotypecaller"
        }, 
        {
            "class": "CommandLineTool", 
            "id": "#gatk-ir.cwl", 
            "requirements": [
                {
                    "class": "InlineJavascriptRequirement"
                }, 
                {
                    "class": "DockerRequirement", 
                    "dockerPull": "broadinstitute/gatk3:3.6-0"
                }, 
                {
                    "class": "InitialWorkDirRequirement", 
                    "listing": [
                        {
                            "entry": "$(inputs.reference_genome)"
                        }, 
                        {
                            "entry": "$(inputs.dict)"
                        }
                    ]
                }, 
                {
                    "class": "ResourceRequirement", 
                    "outdirMin": 7500, 
                    "tmpdirMin": 7700
                }
            ], 
            "hints": [
                {
                    "class": "ResourceRequirement", 
                    "coresMin": 8, 
                    "ramMin": 8000
                }
            ], 
            "baseCommand": [
                "java", 
                "-jar", 
                "/usr/GenomeAnalysisTK.jar", 
                "-T", 
                "IndelRealigner"
            ], 
            "inputs": [
                {
                    "id": "#gatk-ir.cwl/input", 
                    "type": [
                        "File", 
                        {
                            "type": "array", 
                            "items": "File"
                        }
                    ], 
                    "inputBinding": {
                        "position": 2, 
                        "prefix": "-I"
                    }, 
                    "secondaryFiles": [
                        "^.bai"
                    ]
                }, 
                {
                    "id": "#gatk-ir.cwl/rtc_intervals", 
                    "type": "File", 
                    "inputBinding": {
                        "position": 3, 
                        "prefix": "-targetIntervals"
                    }
                }, 
                {
                    "id": "#gatk-ir.cwl/reference_genome", 
                    "type": "File", 
                    "inputBinding": {
                        "position": 1, 
                        "prefix": "-R"
                    }, 
                    "secondaryFiles": [
                        ".fai"
                    ]
                }, 
                {
                    "id": "#gatk-ir.cwl/dict", 
                    "type": "File"
                }
            ], 
            "arguments": [
                {
                    "position": 5, 
                    "prefix": "-dt", 
                    "valueFrom": "NONE"
                }, 
                {
                    "position": 6, 
                    "prefix": "--maxReadsForRealignment", 
                    "valueFrom": "200000"
                }, 
                {
                    "position": 10, 
                    "prefix": "-o", 
                    "valueFrom": "$(inputs.input.nameroot).realigned.bam"
                }
            ], 
            "outputs": [
                {
                    "id": "#gatk-ir.cwl/realigned_bam", 
                    "type": "File", 
                    "outputBinding": {
                        "glob": "*.realigned.bam"
                    }, 
                    "secondaryFiles": [
                        "^.bai"
                    ]
                }
            ], 
            "label": "ir"
        }, 
        {
            "class": "CommandLineTool", 
            "id": "#gatk3-rtc.cwl", 
            "requirements": [
                {
                    "class": "InlineJavascriptRequirement"
                }, 
                {
                    "class": "DockerRequirement", 
                    "dockerPull": "broadinstitute/gatk3:3.6-0"
                }, 
                {
                    "class": "ResourceRequirement", 
                    "outdirMin": 12500, 
                    "tmpdirMin": 12500
                }, 
                {
                    "class": "InitialWorkDirRequirement", 
                    "listing": [
                        {
                            "entry": "$(inputs.reference_genome)"
                        }, 
                        {
                            "entry": "$(inputs.dict)"
                        }, 
                        {
                            "entry": "$(inputs.known_indels)"
                        }
                    ]
                }
            ], 
            "hints": [
                {
                    "class": "ResourceRequirement", 
                    "coresMin": 4, 
                    "ramMin": 8000
                }
            ], 
            "baseCommand": [
                "java", 
                "-jar", 
                "/usr/GenomeAnalysisTK.jar", 
                "-T", 
                "RealignerTargetCreator"
            ], 
            "inputs": [
                {
                    "id": "#gatk3-rtc.cwl/input", 
                    "type": "File", 
                    "inputBinding": {
                        "position": 2, 
                        "prefix": "-I"
                    }, 
                    "secondaryFiles": [
                        "^.bai"
                    ]
                }, 
                {
                    "id": "#gatk3-rtc.cwl/rtc_intervals_name", 
                    "type": [
                        "null", 
                        "string"
                    ], 
                    "default": "rtc_intervals.list"
                }, 
                {
                    "id": "#gatk3-rtc.cwl/reference_genome", 
                    "type": "File", 
                    "inputBinding": {
                        "position": 1, 
                        "prefix": "-R"
                    }, 
                    "secondaryFiles": [
                        ".fai"
                    ]
                }, 
                {
                    "id": "#gatk3-rtc.cwl/known_indels", 
                    "type": "File", 
                    "inputBinding": {
                        "position": 4, 
                        "prefix": "--known"
                    }
                }, 
                {
                    "id": "#gatk3-rtc.cwl/dict", 
                    "type": "File"
                }
            ], 
            "arguments": [
                {
                    "position": 5, 
                    "prefix": "-dt", 
                    "valueFrom": "NONE"
                }, 
                {
                    "position": 3, 
                    "prefix": "-o", 
                    "valueFrom": "$(inputs.rtc_intervals_name)"
                }
            ], 
            "outputs": [
                {
                    "id": "#gatk3-rtc.cwl/rtc_intervals_file", 
                    "type": "File", 
                    "outputBinding": {
                        "glob": "*.list"
                    }
                }
            ], 
            "label": "rtc"
        }, 
        {
            "class": "CommandLineTool", 
            "baseCommand": [
                "gunzip"
            ], 
            "arguments": [
                "-c", 
                "-v"
            ], 
            "requirements": [
                {
                    "class": "InlineJavascriptRequirement"
                }, 
                {
                    "class": "DockerRequirement", 
                    "dockerPull": "jlaitinen/lftpalpine"
                }, 
                {
                    "class": "ResourceRequirement", 
                    "outdirMin": 7500, 
                    "tmpdirMin": 7500
                }
            ], 
            "hints": [
                {
                    "class": "ResourceRequirement", 
                    "coresMin": 2, 
                    "ramMin": 5000
                }
            ], 
            "inputs": [
                {
                    "id": "#gunzip.cwl/reference_file", 
                    "type": {
                        "type": "array", 
                        "items": "File"
                    }, 
                    "inputBinding": {
                        "position": 2
                    }
                }
            ], 
            "outputs": [
                {
                    "id": "#gunzip.cwl/unzipped_fasta", 
                    "type": "stdout", 
                    "streamable": true
                }
            ], 
            "stdout": "$(inputs.reference_file[0].nameroot)", 
            "id": "#gunzip.cwl"
        }, 
        {
            "class": "CommandLineTool", 
            "baseCommand": [
                "gunzip"
            ], 
            "arguments": [
                "-c"
            ], 
            "requirements": [
                {
                    "class": "InlineJavascriptRequirement"
                }, 
                {
                    "class": "DockerRequirement", 
                    "dockerPull": "jlaitinen/lftpalpine"
                }, 
                {
                    "class": "ResourceRequirement", 
                    "coresMin": 2, 
                    "ramMin": 2000, 
                    "outdirMin": 12500, 
                    "tmpdirMin": 12500
                }
            ], 
            "inputs": [
                {
                    "id": "#gunzip_known_sites.cwl/known_sites_file", 
                    "type": "File", 
                    "inputBinding": {
                        "position": 1
                    }
                }
            ], 
            "outputs": [
                {
                    "id": "#gunzip_known_sites.cwl/unzipped_known_sites_file", 
                    "type": "stdout"
                }
            ], 
            "stdout": "$(inputs.known_sites_file.nameroot)", 
            "id": "#gunzip_known_sites.cwl"
        }, 
        {
            "class": "CommandLineTool", 
            "doc": "transfer file passed from the previous task to the remote ftp server", 
            "requirements": [
                {
                    "class": "InlineJavascriptRequirement"
                }, 
                {
                    "class": "DockerRequirement", 
                    "dockerPull": "jlaitinen/lftpalpine"
                }, 
                {
                    "class": "MultipleInputFeatureRequirement"
                }, 
                {
                    "class": "InitialWorkDirRequirement", 
                    "listing": "${ var r = []; for (var i=0; i < inputs.files_to_send.length; i++) { r.push(inputs.files_to_send[i]); } r.push(inputs.gvcf); r.push(inputs.bam); return r; }"
                }, 
                {
                    "class": "ResourceRequirement", 
                    "outdirMin": 7200
                }
            ], 
            "hints": [
                {
                    "class": "ResourceRequirement", 
                    "coresMin": 1, 
                    "ramMin": 2000
                }
            ], 
            "inputs": [
                {
                    "id": "#lftp.cwl/lftp_out_conf", 
                    "type": "File", 
                    "doc": "The parameters file for lftp", 
                    "inputBinding": {
                        "position": 1
                    }
                }, 
                {
                    "id": "#lftp.cwl/files_to_send", 
                    "type": {
                        "type": "array", 
                        "items": "File"
                    }
                }, 
                {
                    "id": "#lftp.cwl/bam", 
                    "type": "File", 
                    "secondaryFiles": [
                        "^.bai"
                    ]
                }, 
                {
                    "id": "#lftp.cwl/gvcf", 
                    "type": "File", 
                    "secondaryFiles": [
                        ".tbi"
                    ]
                }
            ], 
            "outputs": [
                {
                    "id": "#lftp.cwl/output", 
                    "type": "stdout"
                }
            ], 
            "baseCommand": [
                "lftp"
            ], 
            "arguments": [
                "-f"
            ], 
            "id": "#lftp.cwl"
        }, 
        {
            "class": "CommandLineTool", 
            "id": "#picard_dictionary.cwl", 
            "baseCommand": [
                "picard", 
                "CreateSequenceDictionary"
            ], 
            "requirements": [
                {
                    "class": "InlineJavascriptRequirement"
                }, 
                {
                    "class": "DockerRequirement", 
                    "dockerPull": "quay.io/biocontainers/picard:2.18.25--0"
                }, 
                {
                    "class": "ResourceRequirement", 
                    "outdirMin": 7500, 
                    "tmpdirMin": 7700
                }
            ], 
            "hints": [
                {
                    "class": "ResourceRequirement", 
                    "coresMin": 4, 
                    "ramMin": 4000
                }
            ], 
            "inputs": [
                {
                    "id": "#picard_dictionary.cwl/reference_genome", 
                    "type": "File", 
                    "inputBinding": {
                        "position": 1, 
                        "prefix": "R=", 
                        "separate": false
                    }
                }
            ], 
            "arguments": [
                {
                    "position": 2, 
                    "prefix": "O=", 
                    "separate": false, 
                    "valueFrom": "$(inputs.reference_genome.nameroot).dict"
                }
            ], 
            "outputs": [
                {
                    "id": "#picard_dictionary.cwl/dict", 
                    "type": "File", 
                    "outputBinding": {
                        "glob": "*.dict"
                    }
                }
            ]
        }, 
        {
            "class": "CommandLineTool", 
            "id": "#picard_markduplicates.cwl", 
            "baseCommand": [
                "picard", 
                "MarkDuplicates"
            ], 
            "requirements": [
                {
                    "class": "InlineJavascriptRequirement"
                }, 
                {
                    "class": "DockerRequirement", 
                    "dockerPull": "quay.io/biocontainers/picard:2.18.25--0"
                }, 
                {
                    "class": "ResourceRequirement", 
                    "outdirMin": 7500, 
                    "tmpdirMin": 7700
                }
            ], 
            "hints": [
                {
                    "class": "ResourceRequirement", 
                    "coresMin": 4, 
                    "ramMin": 4000
                }
            ], 
            "inputs": [
                {
                    "type": "File", 
                    "inputBinding": {
                        "position": 2, 
                        "prefix": "INPUT=", 
                        "separate": false
                    }, 
                    "id": "#picard_markduplicates.cwl/input"
                }
            ], 
            "arguments": [
                {
                    "position": 0, 
                    "prefix": "OPTICAL_DUPLICATE_PIXEL_DISTANCE=", 
                    "valueFrom": "100", 
                    "separate": false
                }, 
                {
                    "position": 0, 
                    "prefix": "TAGGING_POLICY=", 
                    "valueFrom": "All", 
                    "separate": false
                }, 
                {
                    "position": 0, 
                    "prefix": "CREATE_INDEX=", 
                    "valueFrom": "true", 
                    "separate": false
                }, 
                {
                    "position": 0, 
                    "prefix": "REMOVE_DUPLICATES=", 
                    "valueFrom": "true", 
                    "separate": false
                }, 
                {
                    "position": 0, 
                    "prefix": "TAG_DUPLICATE_SET_MEMBERS=", 
                    "valueFrom": "true", 
                    "separate": false
                }, 
                {
                    "position": 0, 
                    "prefix": "ASSUME_SORT_ORDER=", 
                    "valueFrom": "coordinate", 
                    "separate": false
                }, 
                {
                    "position": 1, 
                    "prefix": "METRICS_FILE=", 
                    "valueFrom": "$(inputs.input.nameroot).metrics.txt", 
                    "separate": false
                }, 
                {
                    "position": 3, 
                    "prefix": "OUTPUT=", 
                    "valueFrom": "$(inputs.input.nameroot).md.bam", 
                    "separate": false
                }
            ], 
            "outputs": [
                {
                    "id": "#picard_markduplicates.cwl/md_bam", 
                    "type": "File", 
                    "outputBinding": {
                        "glob": "*.md.bam"
                    }, 
                    "secondaryFiles": [
                        "^.bai"
                    ]
                }, 
                {
                    "id": "#picard_markduplicates.cwl/output_metrics", 
                    "type": "File", 
                    "outputBinding": {
                        "glob": "*.metrics.txt"
                    }
                }
            ], 
            "label": "picard-MD"
        }, 
        {
            "class": "CommandLineTool", 
            "id": "#samtools_index.cwl", 
            "baseCommand": [
                "samtools", 
                "faidx"
            ], 
            "requirements": [
                {
                    "class": "InlineJavascriptRequirement"
                }, 
                {
                    "class": "DockerRequirement", 
                    "dockerPull": "biocontainers/samtools:1.3.1"
                }, 
                {
                    "class": "InitialWorkDirRequirement", 
                    "listing": [
                        {
                            "entry": "$(inputs.input)"
                        }
                    ]
                }, 
                {
                    "class": "ResourceRequirement", 
                    "outdirMin": 7500, 
                    "tmpdirMin": 7700
                }
            ], 
            "hints": [
                {
                    "class": "ResourceRequirement", 
                    "coresMin": 8, 
                    "ramMin": 8000
                }
            ], 
            "inputs": [
                {
                    "id": "#samtools_index.cwl/input", 
                    "type": "File", 
                    "inputBinding": {
                        "position": 1
                    }
                }
            ], 
            "outputs": [
                {
                    "id": "#samtools_index.cwl/index_fai", 
                    "type": "File", 
                    "outputBinding": {
                        "glob": "*.fa"
                    }, 
                    "secondaryFiles": [
                        ".fai"
                    ]
                }
            ], 
            "label": "samtools-faidx"
        }, 
        {
            "class": "CommandLineTool", 
            "id": "#samtools_sort_bam.cwl", 
            "baseCommand": [
                "samtools", 
                "sort"
            ], 
            "requirements": [
                {
                    "class": "InlineJavascriptRequirement"
                }, 
                {
                    "class": "DockerRequirement", 
                    "dockerPull": "biocontainers/samtools:1.3.1"
                }, 
                {
                    "class": "ResourceRequirement", 
                    "outdirMin": 7500, 
                    "tmpdirMin": 7700
                }
            ], 
            "hints": [
                {
                    "class": "ResourceRequirement", 
                    "coresMin": 8, 
                    "ramMin": 8000
                }
            ], 
            "inputs": [
                {
                    "id": "#samtools_sort_bam.cwl/input", 
                    "type": "File", 
                    "inputBinding": {
                        "position": 2
                    }
                }, 
                {
                    "id": "#samtools_sort_bam.cwl/threads", 
                    "type": [
                        "null", 
                        "string"
                    ], 
                    "default": 8, 
                    "inputBinding": {
                        "position": 1, 
                        "prefix": "--threads"
                    }
                }
            ], 
            "arguments": [
                {
                    "position": 2, 
                    "prefix": "-o", 
                    "valueFrom": "$(inputs.input.nameroot).sorted.bam"
                }
            ], 
            "outputs": [
                {
                    "id": "#samtools_sort_bam.cwl/sorted_bam", 
                    "type": "File", 
                    "outputBinding": {
                        "glob": "*.sorted.bam"
                    }
                }
            ], 
            "label": "samtools-bam_sort"
        }, 
        {
            "class": "Workflow", 
            "id": "#main", 
            "label": "RD_Connect", 
            "inputs": [
                {
                    "id": "#main/curl_reference_genome_url", 
                    "type": "File"
                }, 
                {
                    "id": "#main/curl_fastq_urls", 
                    "type": "File"
                }, 
                {
                    "id": "#main/curl_known_indels_url", 
                    "type": "File"
                }, 
                {
                    "id": "#main/curl_known_sites_url", 
                    "type": "File"
                }, 
                {
                    "id": "#main/readgroup_str", 
                    "type": "string"
                }, 
                {
                    "id": "#main/chromosome", 
                    "type": [
                        "null", 
                        "string"
                    ]
                }, 
                {
                    "id": "#main/threads", 
                    "type": [
                        "null", 
                        "string"
                    ]
                }, 
                {
                    "id": "#main/sample_name", 
                    "type": "string"
                }, 
                {
                    "id": "#main/lftp_out_conf", 
                    "type": "File"
                }
            ], 
            "outputs": [], 
            "steps": [
                {
                    "id": "#main/fastqs_in", 
                    "in": [
                        {
                            "id": "#main/fastqs_in/curl_config_file", 
                            "source": "#main/curl_fastq_urls"
                        }
                    ], 
                    "out": [
                        {
                            "id": "#main/fastqs_in/in_files"
                        }
                    ], 
                    "run": "#curl.cwl"
                }, 
                {
                    "id": "#main/reference_in", 
                    "in": [
                        {
                            "id": "#main/reference_in/curl_config_file", 
                            "source": "#main/curl_reference_genome_url"
                        }
                    ], 
                    "out": [
                        {
                            "id": "#main/reference_in/in_files"
                        }
                    ], 
                    "run": "#curl.cwl"
                }, 
                {
                    "id": "#main/known_indels_in", 
                    "in": [
                        {
                            "id": "#main/known_indels_in/curl_config_file", 
                            "source": "#main/curl_known_indels_url"
                        }
                    ], 
                    "out": [
                        {
                            "id": "#main/known_indels_in/known_indels_file"
                        }
                    ], 
                    "run": "#curl_indels.cwl"
                }, 
                {
                    "id": "#main/known_sites_in", 
                    "in": [
                        {
                            "id": "#main/known_sites_in/curl_config_file", 
                            "source": "#main/curl_known_sites_url"
                        }
                    ], 
                    "out": [
                        {
                            "id": "#main/known_sites_in/known_sites_file"
                        }
                    ], 
                    "run": "#curl_known_sites.cwl"
                }, 
                {
                    "id": "#main/unzipped_known_sites", 
                    "in": [
                        {
                            "id": "#main/unzipped_known_sites/known_sites_file", 
                            "source": [
                                "#main/known_sites_in/known_sites_file"
                            ]
                        }
                    ], 
                    "out": [
                        {
                            "id": "#main/unzipped_known_sites/unzipped_known_sites_file"
                        }
                    ], 
                    "run": "#gunzip_known_sites.cwl"
                }, 
                {
                    "id": "#main/gunzip", 
                    "in": [
                        {
                            "id": "#main/gunzip/reference_file", 
                            "source": [
                                "#main/reference_in/in_files"
                            ]
                        }
                    ], 
                    "out": [
                        {
                            "id": "#main/gunzip/unzipped_fasta"
                        }
                    ], 
                    "run": "#gunzip.cwl"
                }, 
                {
                    "id": "#main/picard_dictionary", 
                    "in": [
                        {
                            "id": "#main/picard_dictionary/reference_genome", 
                            "source": [
                                "#main/gunzip/unzipped_fasta"
                            ]
                        }
                    ], 
                    "out": [
                        {
                            "id": "#main/picard_dictionary/dict"
                        }
                    ], 
                    "run": "#picard_dictionary.cwl"
                }, 
                {
                    "id": "#main/cutadapt2", 
                    "in": [
                        {
                            "id": "#main/cutadapt2/raw_sequences", 
                            "source": [
                                "#main/fastqs_in/in_files"
                            ]
                        }
                    ], 
                    "out": [
                        {
                            "id": "#main/cutadapt2/trimmed_fastq"
                        }
                    ], 
                    "run": "#cutadapt-v.1.18.cwl"
                }, 
                {
                    "id": "#main/bwa_index", 
                    "in": [
                        {
                            "id": "#main/bwa_index/reference_genome", 
                            "source": [
                                "#main/gunzip/unzipped_fasta"
                            ]
                        }
                    ], 
                    "out": [
                        {
                            "id": "#main/bwa_index/output"
                        }
                    ], 
                    "run": "#bwa-index.cwl"
                }, 
                {
                    "id": "#main/samtools_index", 
                    "in": [
                        {
                            "id": "#main/samtools_index/input", 
                            "source": [
                                "#main/gunzip/unzipped_fasta"
                            ]
                        }
                    ], 
                    "out": [
                        {
                            "id": "#main/samtools_index/index_fai"
                        }
                    ], 
                    "run": "#samtools_index.cwl"
                }, 
                {
                    "id": "#main/bwa_mem", 
                    "in": [
                        {
                            "id": "#main/bwa_mem/trimmed_fastq", 
                            "source": [
                                "#main/cutadapt2/trimmed_fastq"
                            ]
                        }, 
                        {
                            "id": "#main/bwa_mem/read_group", 
                            "source": [
                                "#main/readgroup_str"
                            ]
                        }, 
                        {
                            "id": "#main/bwa_mem/sample_name", 
                            "source": [
                                "#main/sample_name"
                            ]
                        }, 
                        {
                            "id": "#main/bwa_mem/reference_genome", 
                            "source": [
                                "#main/bwa_index/output"
                            ]
                        }, 
                        {
                            "id": "#main/bwa_mem/threads", 
                            "source": [
                                "#main/threads"
                            ]
                        }
                    ], 
                    "out": [
                        {
                            "id": "#main/bwa_mem/aligned_sam"
                        }
                    ], 
                    "run": "#bwa-mem.cwl"
                }, 
                {
                    "id": "#main/samtools_sort", 
                    "in": [
                        {
                            "id": "#main/samtools_sort/input", 
                            "source": [
                                "#main/bwa_mem/aligned_sam"
                            ]
                        }, 
                        {
                            "id": "#main/samtools_sort/threads", 
                            "source": [
                                "#main/threads"
                            ]
                        }
                    ], 
                    "out": [
                        {
                            "id": "#main/samtools_sort/sorted_bam"
                        }
                    ], 
                    "run": "#samtools_sort_bam.cwl"
                }, 
                {
                    "id": "#main/picard_markduplicates", 
                    "in": [
                        {
                            "id": "#main/picard_markduplicates/input", 
                            "source": [
                                "#main/samtools_sort/sorted_bam"
                            ]
                        }
                    ], 
                    "out": [
                        {
                            "id": "#main/picard_markduplicates/md_bam"
                        }, 
                        {
                            "id": "#main/picard_markduplicates/output_metrics"
                        }
                    ], 
                    "run": "#picard_markduplicates.cwl", 
                    "label": "picard-MD"
                }, 
                {
                    "id": "#main/gatk3-rtc", 
                    "in": [
                        {
                            "id": "#main/gatk3-rtc/input", 
                            "source": [
                                "#main/picard_markduplicates/md_bam"
                            ]
                        }, 
                        {
                            "id": "#main/gatk3-rtc/reference_genome", 
                            "source": [
                                "#main/samtools_index/index_fai"
                            ]
                        }, 
                        {
                            "id": "#main/gatk3-rtc/dict", 
                            "source": [
                                "#main/picard_dictionary/dict"
                            ]
                        }, 
                        {
                            "id": "#main/gatk3-rtc/known_indels", 
                            "source": [
                                "#main/known_indels_in/known_indels_file"
                            ]
                        }
                    ], 
                    "out": [
                        {
                            "id": "#main/gatk3-rtc/rtc_intervals_file"
                        }
                    ], 
                    "run": "#gatk3-rtc.cwl", 
                    "label": "gatk3-rtc"
                }, 
                {
                    "id": "#main/gatk-ir", 
                    "in": [
                        {
                            "id": "#main/gatk-ir/input", 
                            "source": [
                                "#main/picard_markduplicates/md_bam"
                            ]
                        }, 
                        {
                            "id": "#main/gatk-ir/rtc_intervals", 
                            "source": [
                                "#main/gatk3-rtc/rtc_intervals_file"
                            ]
                        }, 
                        {
                            "id": "#main/gatk-ir/reference_genome", 
                            "source": [
                                "#main/samtools_index/index_fai"
                            ]
                        }, 
                        {
                            "id": "#main/gatk-ir/dict", 
                            "source": [
                                "#main/picard_dictionary/dict"
                            ]
                        }
                    ], 
                    "out": [
                        {
                            "id": "#main/gatk-ir/realigned_bam"
                        }
                    ], 
                    "run": "#gatk-ir.cwl", 
                    "label": "gatk-ir"
                }, 
                {
                    "id": "#main/gatk-base_recalibration", 
                    "in": [
                        {
                            "id": "#main/gatk-base_recalibration/reference_genome", 
                            "source": [
                                "#main/samtools_index/index_fai"
                            ]
                        }, 
                        {
                            "id": "#main/gatk-base_recalibration/dict", 
                            "source": [
                                "#main/picard_dictionary/dict"
                            ]
                        }, 
                        {
                            "id": "#main/gatk-base_recalibration/input", 
                            "source": [
                                "#main/gatk-ir/realigned_bam"
                            ]
                        }, 
                        {
                            "id": "#main/gatk-base_recalibration/unzipped_known_sites_file", 
                            "source": [
                                "#main/unzipped_known_sites/unzipped_known_sites_file"
                            ]
                        }, 
                        {
                            "id": "#main/gatk-base_recalibration/known_indels_file", 
                            "source": [
                                "#main/known_indels_in/known_indels_file"
                            ]
                        }, 
                        {
                            "id": "#main/gatk-base_recalibration/threads", 
                            "source": [
                                "#main/threads"
                            ]
                        }
                    ], 
                    "out": [
                        {
                            "id": "#main/gatk-base_recalibration/br_model"
                        }
                    ], 
                    "run": "#gatk-base_recalibration.cwl", 
                    "label": "gatk-base_recalibration"
                }, 
                {
                    "id": "#main/gatk-base_recalibration_print_reads", 
                    "in": [
                        {
                            "id": "#main/gatk-base_recalibration_print_reads/reference_genome", 
                            "source": [
                                "#main/samtools_index/index_fai"
                            ]
                        }, 
                        {
                            "id": "#main/gatk-base_recalibration_print_reads/dict", 
                            "source": [
                                "#main/picard_dictionary/dict"
                            ]
                        }, 
                        {
                            "id": "#main/gatk-base_recalibration_print_reads/input", 
                            "source": [
                                "#main/gatk-ir/realigned_bam"
                            ]
                        }, 
                        {
                            "id": "#main/gatk-base_recalibration_print_reads/br_model", 
                            "source": [
                                "#main/gatk-base_recalibration/br_model"
                            ]
                        }
                    ], 
                    "out": [
                        {
                            "id": "#main/gatk-base_recalibration_print_reads/bqsr_bam"
                        }
                    ], 
                    "run": "#gatk-base_recalibration_print_reads.cwl", 
                    "label": "gatk-base_recalibration_print_reads"
                }, 
                {
                    "id": "#main/gatk_haplotype_caller", 
                    "in": [
                        {
                            "id": "#main/gatk_haplotype_caller/reference_genome", 
                            "source": [
                                "#main/samtools_index/index_fai"
                            ]
                        }, 
                        {
                            "id": "#main/gatk_haplotype_caller/dict", 
                            "source": [
                                "#main/picard_dictionary/dict"
                            ]
                        }, 
                        {
                            "id": "#main/gatk_haplotype_caller/input", 
                            "source": [
                                "#main/gatk-base_recalibration_print_reads/bqsr_bam"
                            ]
                        }, 
                        {
                            "id": "#main/gatk_haplotype_caller/chromosome", 
                            "source": [
                                "#main/chromosome"
                            ]
                        }, 
                        {
                            "id": "#main/gatk_haplotype_caller/threads", 
                            "source": [
                                "#main/threads"
                            ]
                        }
                    ], 
                    "out": [
                        {
                            "id": "#main/gatk_haplotype_caller/gvcf"
                        }
                    ], 
                    "run": "#gatk-haplotype_caller.cwl", 
                    "label": "gatk-haplotype_caller"
                }, 
                {
                    "id": "#main/lftp_out", 
                    "in": [
                        {
                            "id": "#main/lftp_out/lftp_out_conf", 
                            "source": "#main/lftp_out_conf"
                        }, 
                        {
                            "id": "#main/lftp_out/files_to_send", 
                            "source": [
                                "#main/picard_markduplicates/output_metrics", 
                                "#main/samtools_index/index_fai"
                            ]
                        }, 
                        {
                            "id": "#main/lftp_out/bam", 
                            "source": [
                                "#main/gatk-base_recalibration_print_reads/bqsr_bam"
                            ]
                        }, 
                        {
                            "id": "#main/lftp_out/gvcf", 
                            "source": [
                                "#main/gatk_haplotype_caller/gvcf"
                            ]
                        }
                    ], 
                    "out": [], 
                    "run": "#lftp.cwl"
                }
            ], 
            "requirements": [
                {
                    "class": "MultipleInputFeatureRequirement"
                }
            ]
        }
    ]
}