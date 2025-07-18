import json
import pyfabricops as pf

from _dataflow_gen2_manipulation import replace_dataflow_gen2_placeholders_with_parameters

project_path = 'src'
workspace_path = 'PFO_002_Fabric'
workspace_alias = "PFO_002_Fabric"
branch = pf.get_current_branch()
workspace_suffix = pf.get_workspace_suffix(branch=branch) 
config_path = f'{project_path}/config.json'

dataflow_name = 'UpdateCalendar'
dataflow_path = f'{project_path}/{workspace_path}/Orchestration/{dataflow_name}.Dataflow/mashup.pq'

with open(config_path, 'r') as file:
    config = json.load(file)

variables = config[branch][workspace_alias]['dataflows'][dataflow_name]['variables']

print("Variables from config:")
print(variables)

if not variables:
    print(f"No variables found for {dataflow_name} in {config_path}.")
    exit(0)

# Replace placeholders with actual values
modified_content = replace_dataflow_gen2_placeholders_with_parameters(dataflow_path, variables, dataflow_name)

# Save the modified content back to the file
with open(dataflow_path, 'w', encoding='utf-8') as file:
    file.write(modified_content)

print(f"Placeholders replaced with variables from {config_path} in {dataflow_path}.")
