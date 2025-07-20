# scripts/project_start.py
import sys
import os

from pathlib import Path

# Ensure the parent directory is in the path for module imports
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(".."), "..")))

from scripts.bootstrap import (
    branch,
    config_path,
    pf,
    project_path, 
    root_path,
    workspace_alias,
    workspace_name,   
    workspace_path,   
    workspace_suffix,
)

# Set the capacity ID for the project
capacity_id = '7732a1eb-3893-4642-a85c-93fc3f35d076'


# Create a new workspace
workspace = pf.create_workspace(
    workspace_name,
    capacity=capacity_id,
    description='A Microsoft Fabric project with PyFabricOps',
    roles = pf.read_json('workspaces_roles.json')
)
print(workspace) 


# Export the workspace to config
pf.export_workspace_config(
    workspace_name,
    project_path=project_path,
    config_path=config_path,
    branch=branch,
    workspace_suffix=workspace_suffix,
)

# Retrieve the workspace_id from config
workspace_id = pf.read_json(config_path)[branch][workspace_alias]['workspace_config']['workspace_id']
print(f"Workspace ID: {workspace_id}")

# Create the folder structure for the project
pf.create_folder(
    workspace_id,
    folder='Engineering',
)

pf.create_folder(
    workspace_id,
    folder='PowerBI',
)

pf.create_folder(
    workspace_id,
    folder='Direct',
    parent_folder='PowerBI',
)

pf.create_folder(
    workspace_id,
    folder='Import',
    parent_folder='PowerBI',
)

pf.export_folders(
    workspace_id,
    project_path=project_path,
    workspace_path=workspace_path,
    config_path=config_path,
    branch=branch,
    workspace_suffix=workspace_suffix,
)

# Create the lakehouse
lakehouse = pf.create_lakehouse(
    workspace_id,
    display_name='MainStorageLakehouse',
    description='A lakehouse for the Microsoft Fabric project with PyFabricOps',
    folder='Engineering',
)

# Export the lakehouse to config
pf.export_all_lakehouses(
    workspace_id,
    project_path=project_path,
    workspace_path=workspace_path,
    config_path=config_path,
    branch=branch,
    workspace_suffix=workspace_suffix,
)

