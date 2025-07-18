import json
import pyfabricops as pf

from _notebook_manipulation import extract_parameters_notebook

project_path = 'src'
workspace_path = 'PFO_002_Fabric'
workspace_alias = "PFO_002_Fabric"
branch = pf.get_current_branch()
workspace_suffix = pf.get_workspace_suffix(branch=branch) 
config_path = f'{project_path}/config.json'

notebook_name = 'TransformAndLoad'
notebook_path = f'{project_path}/{workspace_path}/Orchestration/{notebook_name}.Notebook/notebook-content.py'

# Extract current parameters from the notebook file
current_parameters = extract_parameters_notebook(notebook_path)

if not current_parameters:
    print(f"No parameters found in {notebook_path}.")
    exit(0)

# Save the extracted parameters to config.json
with open(config_path, 'r') as file:
    config = json.load(file)

# Add notebook configuration if it doesn't exist
if 'notebooks' not in config[branch][workspace_alias]:
    config[branch][workspace_alias]['notebooks'] = {}

if notebook_name not in config[branch][workspace_alias]['notebooks']:
    config[branch][workspace_alias]['notebooks'][notebook_name] = {}

# Save the extracted parameters as variables
config[branch][workspace_alias]['notebooks'][notebook_name]['variables'] = current_parameters

# Save updated config
with open(config_path, 'w') as file:
    json.dump(config, file, indent=4)

print(f"Parameters saved to {config_path} under notebooks.{notebook_name}.variables")
