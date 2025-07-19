import json
import pyfabricops as pf

from _data_pipelines_manipulation import extract_data_pipeline_variables

project_path = 'src'
workspace_path = 'PFO_002_Fabric'
workspace_alias = "PFO_002_Fabric"
branch = pf.get_current_branch()
workspace_suffix = pf.get_workspace_suffix(branch=branch) 
config_path = f'{project_path}/config.json'

data_pipeline_name = 'CopyData'
data_pipeline_path = f'{project_path}/{workspace_path}/Orchestration/{data_pipeline_name}.DataPipeline/pipeline-content.json'

variables = extract_data_pipeline_variables(data_pipeline_path) 

if not variables:
    print(f"No variables found in {data_pipeline_name}.")
    exit(0)

with open(config_path, 'r') as file:
    config = json.load(file)

    if 'variables' not in config[branch][workspace_alias]['data_pipelines'][data_pipeline_name]:
        config[branch][workspace_alias]['data_pipelines'][data_pipeline_name]['variables'] = {}
    config[branch][workspace_alias]['data_pipelines'][data_pipeline_name]['variables'] = variables

with open(config_path, 'w') as file:
    json.dump(config, file, indent=4)

print(f"Variables from {data_pipeline_name} extracted and saved to {config_path}.") 
