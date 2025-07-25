# scripts/deploy_powerbi.py
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

pf.export_all_semantic_models(
    workspace_name,
    project_path=project_path,
    workspace_path=workspace_path,
    config_path=config_path,
    branch=branch,
    workspace_suffix=workspace_suffix,
    excluded_starts=('Main',)
)

pf.deploy_all_reports_cicd(
    project_path=project_path,
    workspace_alias=workspace_alias,
    config_path=config_path,
    branch=branch,
    workspace_suffix=workspace_suffix,
)
