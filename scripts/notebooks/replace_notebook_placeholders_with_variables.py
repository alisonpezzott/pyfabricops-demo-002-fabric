import json
import pyfabricops as pf
from _notebook_manipulation import replace_notebook_placeholders_with_parameters

# Set up paths
project_path = 'src'
workspace_path = 'PFO_002_Fabric'
workspace_alias = "PFO_002_Fabric"
branch = pf.get_current_branch()
workspace_suffix = pf.get_workspace_suffix(branch=branch) 
config_path = f'{project_path}/config.json'
notebook_name = 'TransformAndLoad'
notebook_path = f'{project_path}/{workspace_path}/Orchestration/{notebook_name}.Notebook/notebook-content.py'

# Load parameters from config
print("Loading parameters from config...")
with open(config_path, 'r') as file:
    config = json.load(file)

variables = config[branch][workspace_alias]['notebooks'][notebook_name]['variables']

if not variables:
    print(f"No variables found for {notebook_name} in {config_path}.")
    exit(0)

# Replace placeholders with actual values
print("\nReplacing placeholders with actual values...")
modified_content = replace_notebook_placeholders_with_parameters(notebook_path, variables, notebook_name)

# Save the modified content back to the file
with open(notebook_path, 'w', encoding='utf-8') as file:
    file.write(modified_content)

print(f"✓ Placeholders replaced with variables from {config_path} in {notebook_path}.")
