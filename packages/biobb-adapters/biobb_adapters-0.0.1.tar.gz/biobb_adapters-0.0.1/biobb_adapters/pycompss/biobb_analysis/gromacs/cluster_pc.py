import traceback
from pycompss.api.task import task
from pycompss.api.constraint import constraint
from pycompss.api.parameter import FILE_IN, FILE_OUT
from biobb_common.tools import file_utils as fu
from biobb_analysis.gromacs import cluster

@task(input_gro_path=FILE_IN, input_traj_path=FILE_IN, output_pdb_path=FILE_OUT)
def cluster_pc(input_gro_path, input_traj_path, output_pdb_path, properties, **kwargs):
    try:
        cluster.Cluster(input_gro_path=input_gro_path, input_traj_path=input_traj_path, output_pdb_path=output_pdb_path, properties=properties, **kwargs).launch()
    except Exception:
        traceback.print_exc()
        fu.write_failed_output(output_pdb_path)
