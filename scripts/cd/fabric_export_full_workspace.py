from dotenv import load_dotenv
import pyfabricops as pf

# Settings
pf.set_auth_provider('env') # Available env, vault, oauth
pf.setup_logging(format_style='minimal')
branch = pf.get_current_branch()
workspace_suffix = pf.get_workspace_suffix(branch=branch)
workspace_alias = 'PFO_002_Fabric'
workspace_name = workspace_alias + workspace_suffix

# Load .env from root repository directory
load_dotenv()  

# Run export
pf.export_full_workspace(
    workspace=workspace_name,
    project_path="src",
    workspace_path=workspace_alias,
    branch=branch,
    workspace_suffix=workspace_suffix,
)
