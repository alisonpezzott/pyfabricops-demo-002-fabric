# scripts/bootstrap.py
from dotenv import load_dotenv
import pyfabricops as pf
import os

# loading .env
load_dotenv()

# common settings
pf.set_auth_provider('env')
pf.setup_logging(level='info', format_style='minimal')

project_path   = 'src'
workspace_path = 'PF_002_Fabric'
branch         = pf.get_current_branch()
workspace_alias = "PF_002_Fabric"
workspace_suffix = pf.get_workspace_suffix(
    branch=branch,
    path='branches.json'
)
workspace_name = f'{workspace_alias}{workspace_suffix}'
config_path    = os.path.join(project_path, 'config.json')
