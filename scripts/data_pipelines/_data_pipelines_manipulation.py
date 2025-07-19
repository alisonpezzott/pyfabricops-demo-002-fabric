import json

def extract_data_pipeline_variables(path: str) -> list:

    with open(path, 'r') as f:
        content = json.load(f)

    activities = content['properties']['activities'] 

    variables = []

    for activity_index, activity in enumerate(activities):
        activity_name = activity['name']

        subactivities = activity['typeProperties']['activities']
        for subactivity_index, subactivity in enumerate(subactivities):
            subactivity_name = subactivity['name']
            properties = subactivity['typeProperties']
            
            source = properties['source']['datasetSettings']
            source_database = source['typeProperties']['database']
            source_connection = source['externalReferences']['connection']

            sink = properties['sink']['datasetSettings']['linkedService']
            sink_name = sink['name']
            sink_properties = sink['properties']['typeProperties']
            sink_workspace_id = sink_properties['workspaceId']
            sink_artifact_id = sink_properties['artifactId']

            variables.append(
                {
                    'activity_index': activity_index,
                    'activity_name': activity_name,
                    'subactivity_index': subactivity_index,
                    'subactivity_name': subactivity_name,
                    'source_database': source_database,
                    'source_connection': source_connection,
                    'sink_name': sink_name,
                    'sink_workspace_id': sink_workspace_id,
                    'sink_artifact_id': sink_artifact_id
                }
            )

    return variables


def replace_data_pipeline_variables_with_placeholders(path: str, variables: list) -> str:

    with open(path, 'r') as f:
        content = json.load(f)

    for variable in variables:
        # Use indexes to find correct variable - Does not assume unique names
        # This allows multiple activities/subactivities with the same name
        activity_idx = variable['activity_index']
        subactivity_idx = variable['subactivity_index']
        
        # Substitute just the values that need to be replaced with placeholders
        # Database
        content['properties']['activities'][activity_idx]['typeProperties']['activities'][subactivity_idx]['typeProperties']['source']['datasetSettings']['typeProperties']['database'] = f"#{{{variable['activity_name']}_{variable['subactivity_name']}_source_database}}#"
        
        # Connection  
        content['properties']['activities'][activity_idx]['typeProperties']['activities'][subactivity_idx]['typeProperties']['source']['datasetSettings']['externalReferences']['connection'] = f"#{{{variable['activity_name']}_{variable['subactivity_name']}_source_connection}}#"
        
        # Workspace ID
        content['properties']['activities'][activity_idx]['typeProperties']['activities'][subactivity_idx]['typeProperties']['sink']['datasetSettings']['linkedService']['properties']['typeProperties']['workspaceId'] = f"#{{{variable['activity_name']}_{variable['subactivity_name']}_sink_workspace_id}}#"
        
        # Artifact ID
        content['properties']['activities'][activity_idx]['typeProperties']['activities'][subactivity_idx]['typeProperties']['sink']['datasetSettings']['linkedService']['properties']['typeProperties']['artifactId'] = f"#{{{variable['activity_name']}_{variable['subactivity_name']}_sink_artifact_id}}#"

    return json.dumps(content, indent=2)


def create_data_pipeline_placeholder_mapping(variables: list) -> dict:
    """
    Creates a mapping of placeholders to their real values based on the extracted variables.
    """
    placeholder_mapping = {}
    
    for variable in variables:
        activity_name = variable['activity_name']
        subactivity_name = variable['subactivity_name']
        
        # Create a unique placeholder for each variable
        placeholder_mapping[f"{activity_name}_{subactivity_name}_source_database"] = variable['source_database']
        placeholder_mapping[f"{activity_name}_{subactivity_name}_source_connection"] = variable['source_connection']
        placeholder_mapping[f"{activity_name}_{subactivity_name}_sink_workspace_id"] = variable['sink_workspace_id']
        placeholder_mapping[f"{activity_name}_{subactivity_name}_sink_artifact_id"] = variable['sink_artifact_id']
    
    return placeholder_mapping


def replace_data_pipeline_placeholders_with_variables(path: str, variables: list) -> str:

    with open(path, 'r') as f:
        content_str = f.read()

    mappings = create_data_pipeline_placeholder_mapping(variables)

    # Substitute each placeholder with the corresponding value
    for placeholder, value in mappings.items():
        placeholder_pattern = f"#{{{placeholder}}}#"
        content_str = content_str.replace(placeholder_pattern, value)
    
    return content_str

