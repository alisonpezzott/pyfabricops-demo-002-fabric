import re

def extract_dataflow_gen2_variables(path: str) -> list:
    """
    Extract parameters from a Dataflow Gen2 mashup.pq file, identifying each destination separately.
    
    Args:
        path (str): Path to the mashup.pq file
        
    Returns:
        list: List of dictionaries containing the extracted parameters for each destination
    """
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read() 

    parameters = []
    
    # Pattern to find DataDestination sections
    # Look for shared QueryName_DataDestination = let
    destination_pattern = r'shared\s+(\w+)_DataDestination\s*=\s*let(.*?)in\s*\w+;'
    destination_matches = re.findall(destination_pattern, content, re.DOTALL)
    
    for query_name, destination_content in destination_matches:
        param_dict = {
            'destination_name': f"{query_name}_DataDestination",
            'query_name': query_name
        }
        
        # Extract workspaceId
        workspace_pattern = r'workspaceId\s*=\s*"([a-f0-9-]+)"'
        workspace_match = re.search(workspace_pattern, destination_content)
        if workspace_match:
            param_dict['workspaceId'] = workspace_match.group(1)
        
        # Extract lakehouseId
        lakehouse_pattern = r'lakehouseId\s*=\s*"([a-f0-9-]+)"'
        lakehouse_match = re.search(lakehouse_pattern, destination_content)
        if lakehouse_match:
            param_dict['lakehouseId'] = lakehouse_match.group(1)
            param_dict['destination_type'] = 'Lakehouse'
        
        # Extract warehouseId
        warehouse_pattern = r'warehouseId\s*=\s*"([a-f0-9-]+)"'
        warehouse_match = re.search(warehouse_pattern, destination_content)
        if warehouse_match:
            param_dict['warehouseId'] = warehouse_match.group(1)
            param_dict['destination_type'] = 'Warehouse'
        
        # Extract semanticModelId (if present)
        semantic_pattern = r'semanticModelId\s*=\s*"([a-f0-9-]+)"'
        semantic_match = re.search(semantic_pattern, destination_content)
        if semantic_match:
            param_dict['semanticModelId'] = semantic_match.group(1)
            param_dict['destination_type'] = 'SemanticModel'
        
        # Only add if we found at least one ID parameter
        if any(key.endswith('Id') for key in param_dict.keys()):
            parameters.append(param_dict)
    
    return parameters


def replace_dataflow_gen2_parameters_with_placeholders(path: str, parameters: list, dataflow_name: str) -> str:
    """
    Replace parameters with placeholders in a Dataflow Gen2 mashup.pq file.
    Each destination gets unique placeholders based on its query name.
    
    Args:
        path (str): Path to the mashup.pq file
        parameters (list): List of parameter dictionaries to replace
        dataflow_name (str): Name of the dataflow for placeholder naming
        
    Returns:
        str: Modified content with placeholders
    """
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace each destination's parameters with unique placeholders
    for param_dict in parameters:
        query_name = param_dict['query_name']
        
        # Replace workspaceId
        if 'workspaceId' in param_dict:
            workspace_id = param_dict['workspaceId']
            placeholder = f"#{{{dataflow_name}_{query_name}_workspaceId}}#"
            content = content.replace(f'workspaceId = "{workspace_id}"', f'workspaceId = "{placeholder}"')
        
        # Replace lakehouseId
        if 'lakehouseId' in param_dict:
            lakehouse_id = param_dict['lakehouseId']
            placeholder = f"#{{{dataflow_name}_{query_name}_lakehouseId}}#"
            content = content.replace(f'lakehouseId = "{lakehouse_id}"', f'lakehouseId = "{placeholder}"')
        
        # Replace warehouseId
        if 'warehouseId' in param_dict:
            warehouse_id = param_dict['warehouseId']
            placeholder = f"#{{{dataflow_name}_{query_name}_warehouseId}}#"
            content = content.replace(f'warehouseId = "{warehouse_id}"', f'warehouseId = "{placeholder}"')
        
        # Replace semanticModelId
        if 'semanticModelId' in param_dict:
            semantic_id = param_dict['semanticModelId']
            placeholder = f"#{{{dataflow_name}_{query_name}_semanticModelId}}#"
            content = content.replace(f'semanticModelId = "{semantic_id}"', f'semanticModelId = "{placeholder}"')
    
    return content


def replace_dataflow_gen2_placeholders_with_parameters(path: str, parameters: list, dataflow_name: str) -> str:
    """
    Replace placeholders with actual parameters in a Dataflow Gen2 mashup.pq file.
    
    Args:
        path (str): Path to the mashup.pq file
        parameters (list): List of parameter dictionaries with actual values
        dataflow_name (str): Name of the dataflow for placeholder naming
        
    Returns:
        str: Modified content with actual parameter values
    """
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace placeholders with actual values for each destination
    for param_dict in parameters:
        query_name = param_dict['query_name']
        
        # Replace workspaceId placeholder
        if 'workspaceId' in param_dict:
            workspace_id = param_dict['workspaceId']
            placeholder = f"#{{{dataflow_name}_{query_name}_workspaceId}}#"
            content = content.replace(f'workspaceId = "{placeholder}"', f'workspaceId = "{workspace_id}"')
        
        # Replace lakehouseId placeholder
        if 'lakehouseId' in param_dict:
            lakehouse_id = param_dict['lakehouseId']
            placeholder = f"#{{{dataflow_name}_{query_name}_lakehouseId}}#"
            content = content.replace(f'lakehouseId = "{placeholder}"', f'lakehouseId = "{lakehouse_id}"')
        
        # Replace warehouseId placeholder
        if 'warehouseId' in param_dict:
            warehouse_id = param_dict['warehouseId']
            placeholder = f"#{{{dataflow_name}_{query_name}_warehouseId}}#"
            content = content.replace(f'warehouseId = "{placeholder}"', f'warehouseId = "{warehouse_id}"')
        
        # Replace semanticModelId placeholder
        if 'semanticModelId' in param_dict:
            semantic_id = param_dict['semanticModelId']
            placeholder = f"#{{{dataflow_name}_{query_name}_semanticModelId}}#"
            content = content.replace(f'semanticModelId = "{placeholder}"', f'semanticModelId = "{semantic_id}"')
    
    return content
