class: Workflow
cwlVersion: v1.0
dct:creator: {'@id': 'http://orcid.org/0000-0002-7681-6415', 'foaf:mbox': tnv@synapse.org,
  'foaf:name': tnv}
doc: 'SMC-RNA challenge fusion detection submission

  FusionRnadt workflow: gunzip, indexing,  fusion count, gene-fusion detection'
hints: []
id: main
inputs:
- {id: TUMOR_FASTQ_1, type: File}
- {id: TUMOR_FASTQ_2, type: File}
- {id: cndaFa, type: File}
- {id: gtffile, type: File}
- {id: sqlitefile, type: File}
- {id: txAnnofile, type: File}
name: main
outputs:
- {id: OUTPUT, outputSource: runRscript/fusionout, type: File}
steps:
- id: FusionRnadt_counting
  in:
  - {id: fastq1, source: gunzipfastq1/output}
  - {id: fastq2, source: gunzipfastq2/output}
  - {id: gtffn, source: gunzipgtffile/output}
  - {id: indexDir, source: FusionRnadt_indexing/output}
  - {default: ISR, id: libtype}
  - {default: fusionCountRes, id: output_name}
  - {default: 8, id: threads}
  out: [output]
  run: extractFusionCount.cwl
- id: FusionRnadt_indexing
  in:
  - {default: sailfish_Homo_sapiens_GRCh3775_cdna_all_idx, id: output_name}
  - {id: txFasta, source: gunzipcndaFa/output}
  out: [output]
  run: createIndex.cwl
- id: gunzipcndaFa
  in:
  - {id: input, source: cndaFa}
  out: [output]
  run: gunzip.cwl
- id: gunzipfastq1
  in:
  - {id: input, source: TUMOR_FASTQ_1}
  out: [output]
  run: gunzip.cwl
- id: gunzipfastq2
  in:
  - {id: input, source: TUMOR_FASTQ_2}
  out: [output]
  run: gunzip.cwl
- id: gunzipgtffile
  in:
  - {id: input, source: gtffile}
  out: [output]
  run: gunzip.cwl
- id: runRscript
  in:
  - {default: /opt/tmpCodes/Rscripts/detectFusionGenes2.R, id: RscriptFile}
  - {id: fusionCountDir, source: FusionRnadt_counting/output}
  - {id: gtfSqlite, source: sqlitefile}
  - {default: fusionGenes.bedpe, id: output_name}
  - {id: txAnno, source: txAnnofile}
  out: [fusionout]
  run: detectFusionGenes.cwl