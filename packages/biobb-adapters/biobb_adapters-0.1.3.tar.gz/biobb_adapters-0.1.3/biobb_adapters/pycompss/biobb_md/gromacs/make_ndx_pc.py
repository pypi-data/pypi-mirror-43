import traceback
from pycompss.api.task import task
from pycompss.api.constraint import constraint
from pycompss.api.parameter import FILE_IN, FILE_OUT
from biobb_common.tools import file_utils as fu
from biobb_md.gromacs import make_ndx

@task(input_structure_path=FILE_IN, output_ndx_path=FILE_OUT)
def make_ndx_pc(input_structure_path, output_ndx_path, properties, **kwargs):
    try:
        make_ndx.MakeNdx(input_structure_path=input_structure_path, output_ndx_path=output_ndx_path, properties=properties, **kwargs).launch()
    except Exception:
        traceback.print_exc()
        fu.write_failed_output(output_ndx_path)
