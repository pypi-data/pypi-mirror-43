import traceback
from pycompss.api.task import task
from pycompss.api.constraint import constraint
from pycompss.api.parameter import FILE_IN, FILE_OUT
from biobb_common.tools import file_utils as fu
from biobb_md.gromacs import grompp

@task(input_gro_path=FILE_IN, input_top_zip_path=FILE_IN, output_tpr_path=FILE_OUT)
def grompp_pc(input_gro_path, input_top_zip_path, output_tpr_path, properties, **kwargs):
    try:
        grompp.Grompp(input_gro_path=input_gro_path, input_top_zip_path=input_top_zip_path, output_tpr_path=output_tpr_path, properties=properties, **kwargs).launch()
    except Exception:
        traceback.print_exc()
        fu.write_failed_output(output_tpr_path)
