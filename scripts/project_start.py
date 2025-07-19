# scripts/project_start.py
from scripts.bootstrap import (
    pf,
    project_path, workspace_alias, config_path, branch, workspace_path
)

workspaces = pf.list_workspaces(df=True) 
print(workspaces) 