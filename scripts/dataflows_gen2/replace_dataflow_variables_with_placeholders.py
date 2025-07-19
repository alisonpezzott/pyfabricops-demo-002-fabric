import json
import pyfabricops as pf

from _dataflow_gen2_manipulation import replace_dataflow_gen2_parameters_with_placeholders

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

if not variables:
    print(f"No parameters found in {dataflow_path}.")
    exit(0)

# Replace parameters with placeholders
modified_content = replace_dataflow_gen2_parameters_with_placeholders(dataflow_path, variables, dataflow_name)

# Save the modified content back to the file
with open(dataflow_path, 'w', encoding='utf-8') as file:
    file.write(modified_content)

print(f"Parameters replaced with placeholders in {dataflow_path}.")
