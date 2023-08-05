import traceback
from pycompss.api.task import task
from pycompss.api.constraint import constraint
from pycompss.api.parameter import FILE_IN, FILE_OUT
from biobb_common.tools import file_utils as fu
from biobb_analysis.ambertools import cpptraj

@task(input_top_path=FILE_IN, input_traj_path=FILE_IN, output_dat_path=FILE_OUT)
def cpptraj_pc(input_top_path, input_traj_path, output_dat_path, properties, **kwargs):
    try:
        cpptraj.Cpptraj(input_top_path=input_top_path, input_traj_path=input_traj_path, output_dat_path=output_dat_path, properties=properties, **kwargs).launch()
    except Exception:
        traceback.print_exc()
        fu.write_failed_output(output_dat_path)
