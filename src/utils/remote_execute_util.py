
from azureml.core import Workspace, Experiment
from azureml.train.estimator import Estimator
from azureml.core.authentication import InteractiveLoginAuthentication

from utils.aml_util import prepare_remote_compute
import os


def get_ws(tenant=None):
    """
    :param tenant:
    :return:
    """
    if tenant:
        auth = InteractiveLoginAuthentication(tenant_id = tenant)
        ws = Workspace.from_config(auth = auth)
    else:
        ws = Workspace.from_config()
    return ws

def prepare_remote_experiment(ws, regularization):
    # Connect to remote Machine Learning Services Workspace (MLSW).
    # Needs config.json in the root of the project. You can download it from portal.azure.com -> MLSW

    ds = ws.get_default_datastore()

    #Check that remote computing exists
    compute_target = prepare_remote_compute(ws)

    #Define the folder that is sent to remote computing
    script_folder  = os.path.join(os.getcwd(), "../src")

    #An estimator object is used to submit the run.
    script_params = {
        '--data-folder': ds.path('mnist').as_mount(),
        '--regularization': regularization
    }

    return Estimator(source_directory=script_folder,
                    script_params=script_params,
                    compute_target=compute_target,
                    entry_script='train.py',
                    pip_requirements_file_path='../requirements_remote.txt')

def create_experiment(experiment_name):
    return Experiment(workspace= Workspace.from_config(), name=experiment_name)




