import traceback
from pycompss.api.task import task
from pycompss.api.constraint import constraint
from pycompss.api.parameter import FILE_IN, FILE_OUT
from biobb_common.tools import file_utils as fu
from biobb_md.gromacs import mdrun
import os

@task(input_tpr_path=FILE_IN, output_trr_path=FILE_OUT, output_gro_path=FILE_OUT, output_edr_path=FILE_OUT, output_log_path=FILE_OUT)
def mdrun_cpt_pc(input_tpr_path, output_trr_path, output_gro_path, output_edr_path, output_log_path, output_cpt_path, properties, **kwargs):
    try:
        mdrun.Mdrun(input_tpr_path=input_tpr_path, output_trr_path=output_trr_path, output_gro_path=output_gro_path, output_edr_path=output_edr_path, output_log_path=output_log_path, output_cpt_path=output_cpt_path, properties=properties, **kwargs).launch()
        if not os.path.exists(output_trr_path):
            fu.write_failed_output(output_trr_path)
        if not os.path.exists(output_edr_path):
            fu.write_failed_output(output_edr_path)
        if not os.path.exists(output_log_path):
            fu.write_failed_output(output_log_path)

    except Exception:
        traceback.print_exc()
        fu.write_failed_output(output_trr_path)
        fu.write_failed_output(output_gro_path)
        fu.write_failed_output(output_edr_path)
        fu.write_failed_output(output_log_path)
        fu.write_failed_output(output_cpt_path)
