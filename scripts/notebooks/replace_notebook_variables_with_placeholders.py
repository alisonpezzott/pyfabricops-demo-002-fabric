import json
import pyfabricops as pf
from _notebook_manipulation import replace_notebook_parameters_with_placeholders

# Set up paths
project_path = 'src'
workspace_path = 'PFO_002_Fabric'
workspace_alias = "PFO_002_Fabric"
branch = pf.get_current_branch()
workspace_suffix = pf.get_workspace_suffix(branch=branch) 
config_path = f'{project_path}/config.json'
notebook_name = 'TransformAndLoad'
notebook_path = f'{project_path}/{workspace_path}/Orchestration/{notebook_name}.Notebook/notebook-content.py'

# Retrieve variables from config
with open(config_path, 'r') as file:
    config = json.load(file)

notebook_variables = config[branch][workspace_alias]['notebooks'][notebook_name]['variables']

print("Current variables extracted from notebook:")

if not notebook_variables:
    print(f"No variables found for {notebook_name} in {config_path}.")
    exit(0)

# Replace variables with placeholders
print("\nReplacing variables with placeholders...")
modified_content = replace_notebook_parameters_with_placeholders(notebook_path, notebook_variables, notebook_name)

# Save the modified content back to the file
with open(notebook_path, 'w', encoding='utf-8') as file:
    file.write(modified_content)

print(f"✓ Variables replaced with placeholders in {notebook_path}.")
