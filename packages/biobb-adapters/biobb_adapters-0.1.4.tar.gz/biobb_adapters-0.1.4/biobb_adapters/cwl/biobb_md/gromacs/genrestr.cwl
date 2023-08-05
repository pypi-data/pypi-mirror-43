#!/usr/bin/env cwl-runner
cwlVersion: v1.0
class: CommandLineTool
baseCommand: genrestr
hints:
  DockerRequirement:
    dockerPull: quay.io/biocontainers/biobb_md:0.1.5--py_0
inputs:
  input_structure_path:
    type: File
    format: edam:format_GROMACS_GRO
    inputBinding:
      position: 1
      prefix: --input_structure_path

  input_ndx_path:
    type: File
    format: edam:format_2330
format: edam:format_2330
    inputBinding:
      position: 2
      prefix: --input_ndx_path

  input_top_zip_path:
    type: File
    format: edam:format_2333
    inputBinding:
      position: 3
      prefix: --input_top_zip_path

  output_top_zip_path:
    type: string
    inputBinding:
      position: 4
      prefix: --output_top_zip_path
    default: "topology_restraint.zip"

  config:
    type: string?
    inputBinding:
      position: 5
      prefix: --config

outputs:
  output_top_zip_file:
    type: File
    format: edam:format_2333
    outputBinding:
      glob: $(inputs.output_top_zip_path)

$namespaces:
  edam: http://edamontology.org/
$schemas:
  - https://raw.githubusercontent.com/edamontology/edamontology/master/EDAM_dev.owl
