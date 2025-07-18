import os
import json
import pyfabricops as pf

from _data_pipelines_manipulation import replace_data_pipeline_variables_with_placeholders

project_path = 'src'
workspace_path = 'PFO_002_Fabric'
workspace_alias = "PFO_002_Fabric"
branch = pf.get_current_branch()
workspace_suffix = pf.get_workspace_suffix(branch=branch) 
config_path = f'{project_path}/config.json'

data_pipeline_name = 'CopyData'
data_pipeline_path = f'{project_path}/{workspace_path}/Orchestration/{data_pipeline_name}.DataPipeline/pipeline-content.json'

with open(config_path, 'r') as file:
    config = json.load(file)

variables = config[branch][workspace_alias]['data_pipelines'][data_pipeline_name]['variables']

print(variables) 

if not variables:
    print(f"No variables found for {data_pipeline_name} in {config_path}.")
    exit(0)

modified_content = replace_data_pipeline_variables_with_placeholders(data_pipeline_path, variables)

# Save the modified content back to the file
with open(data_pipeline_path, 'w') as file:
    file.write(modified_content)

print(f"Variables from {config_path} replaced in {data_pipeline_path} with placeholders.") 
