import json
import pyfabricops as pf

from _dataflow_gen2_manipulation import extract_dataflow_gen2_variables

project_path = 'src'
workspace_path = 'PFO_002_Fabric'
workspace_alias = "PFO_002_Fabric"
branch = pf.get_current_branch()
workspace_suffix = pf.get_workspace_suffix(branch=branch) 
config_path = f'{project_path}/config.json'

dataflow_name = 'UpdateCalendar'
dataflow_path = f'{project_path}/{workspace_path}/Orchestration/{dataflow_name}.Dataflow/mashup.pq'

# Extract current parameters from the dataflow file
current_parameters = extract_dataflow_gen2_variables(dataflow_path)

if not current_parameters:
    print(f"No parameters found in {dataflow_path}.")
    exit(0)

# Save the extracted parameters to config.json
with open(config_path, 'r') as file:
    config = json.load(file)

# Add dataflow configuration if it doesn't exist
if 'dataflows' not in config[branch][workspace_alias]:
    config[branch][workspace_alias]['dataflows'] = {}

if dataflow_name not in config[branch][workspace_alias]['dataflows']:
    config[branch][workspace_alias]['dataflows'][dataflow_name] = {}

# Save the extracted parameters as variables
config[branch][workspace_alias]['dataflows'][dataflow_name]['variables'] = current_parameters

# Save updated config
with open(config_path, 'w') as file:
    json.dump(config, file, indent=4)

print(f"Parameters saved to {config_path} under dataflows.{dataflow_name}.variables")
