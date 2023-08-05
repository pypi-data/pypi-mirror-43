import traceback
from pycompss.api.task import task
from pycompss.api.constraint import constraint
from pycompss.api.parameter import FILE_IN, FILE_OUT
from biobb_common.tools import file_utils as fu
from biobb_md.gromacs import solvate

@task(input_solute_gro_path=FILE_IN, output_gro_path=FILE_OUT, input_top_zip_path=FILE_IN, output_top_zip_path=FILE_OUT)
def solvate_pc(input_solute_gro_path, output_gro_path, input_top_zip_path, output_top_zip_path, properties, **kwargs):
    try:
        solvate.Solvate(input_solute_gro_path=input_solute_gro_path, output_gro_path=output_gro_path, input_top_zip_path=input_top_zip_path, output_top_zip_path=output_top_zip_path, properties=properties, **kwargs).launch()
    except Exception:
        traceback.print_exc()
        fu.write_failed_output(output_gro_path)
        fu.write_failed_output(output_top_zip_path)
