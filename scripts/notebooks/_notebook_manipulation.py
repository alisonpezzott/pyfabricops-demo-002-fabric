import re

def extract_parameters_notebook(path: str) -> list:
    """
    Extract parameters from a Fabric notebook-content.py file.
    
    Args:
        path (str): Path to the notebook-content.py file
        
    Returns:
        list: List of dictionaries containing the extracted parameters
    """
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    parameters = []
    
    # Find the PARAMETERS CELL section
    # Look for "# PARAMETERS CELL ********************" followed by the parameters
    parameters_pattern = r'# PARAMETERS CELL \*+\s*\n(.*?)(?=# METADATA|# CELL|# MARKDOWN|$)'
    parameters_match = re.search(parameters_pattern, content, re.DOTALL)
    
    if parameters_match:
        parameters_content = parameters_match.group(1).strip()
        
        # Extract variable assignments
        # Pattern to find variable = "value" or variable = f"value"
        variable_patterns = [
            r'(\w+)\s*=\s*"([^"]*)"',  # variable = "value"
            r'(\w+)\s*=\s*f"([^"]*)"', # variable = f"value"
            r'(\w+)\s*=\s*\'([^\']*)\'', # variable = 'value'
            r'(\w+)\s*=\s*f\'([^\']*)\'' # variable = f'value'
        ]
        
        for pattern in variable_patterns:
            matches = re.findall(pattern, parameters_content)
            for var_name, var_value in matches:
                # Skip variables that are derived from other variables (contain f-string references)
                if not re.search(r'\{[^}]+\}', var_value):
                    parameters.append({
                        'variable_name': var_name,
                        'variable_value': var_value,
                        'parameter_type': 'string'
                    })
        
        # Also look for numeric and boolean assignments
        numeric_pattern = r'(\w+)\s*=\s*(\d+(?:\.\d+)?)'
        numeric_matches = re.findall(numeric_pattern, parameters_content)
        for var_name, var_value in numeric_matches:
            parameters.append({
                'variable_name': var_name,
                'variable_value': var_value,
                'parameter_type': 'numeric'
            })
        
        boolean_pattern = r'(\w+)\s*=\s*(True|False)'
        boolean_matches = re.findall(boolean_pattern, parameters_content)
        for var_name, var_value in boolean_matches:
            parameters.append({
                'variable_name': var_name,
                'variable_value': var_value,
                'parameter_type': 'boolean'
            })
    
    return parameters


def replace_notebook_parameters_with_placeholders(path: str, parameters: list, notebook_name: str) -> str:
    """
    Replace parameters with placeholders in a Fabric notebook-content.py file.
    
    Args:
        path (str): Path to the notebook-content.py file
        parameters (list): List of parameter dictionaries to replace
        notebook_name (str): Name of the notebook for placeholder naming
        
    Returns:
        str: Modified content with placeholders
    """
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace each parameter with a placeholder
    for param_dict in parameters:
        var_name = param_dict['variable_name']
        var_value = param_dict['variable_value']
        param_type = param_dict['parameter_type']
        
        placeholder = f"#{{{notebook_name}_{var_name}}}#"
        
        # Create different replacement patterns based on parameter type
        if param_type == 'string':
            # Handle both regular strings and f-strings
            old_patterns = [
                f'{var_name} = "{var_value}"',
                f'{var_name} = f"{var_value}"',
                f'{var_name} = \'{var_value}\'',
                f'{var_name} = f\'{var_value}\''
            ]
            new_value = f'{var_name} = "{placeholder}"'
        elif param_type in ['numeric', 'boolean']:
            old_patterns = [f'{var_name} = {var_value}']
            new_value = f'{var_name} = "{placeholder}"'
        
        # Replace all matching patterns
        for old_pattern in old_patterns:
            if old_pattern in content:
                content = content.replace(old_pattern, new_value)
                break
    
    return content


def replace_notebook_placeholders_with_parameters(path: str, parameters: list, notebook_name: str) -> str:
    """
    Replace placeholders with actual parameters in a Fabric notebook-content.py file.
    
    Args:
        path (str): Path to the notebook-content.py file
        parameters (list): List of parameter dictionaries with actual values
        notebook_name (str): Name of the notebook for placeholder naming
        
    Returns:
        str: Modified content with actual parameter values
    """
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace placeholders with actual values
    for param_dict in parameters:
        var_name = param_dict['variable_name']
        var_value = param_dict['variable_value']
        param_type = param_dict['parameter_type']
        
        placeholder = f"#{{{notebook_name}_{var_name}}}#"
        
        # Restore original format based on parameter type
        if param_type == 'string':
            new_value = f'{var_name} = "{var_value}"'
        elif param_type in ['numeric', 'boolean']:
            new_value = f'{var_name} = {var_value}'
        
        # Replace placeholder with original value
        old_pattern = f'{var_name} = "{placeholder}"'
        if old_pattern in content:
            content = content.replace(old_pattern, new_value)
    
    return content

