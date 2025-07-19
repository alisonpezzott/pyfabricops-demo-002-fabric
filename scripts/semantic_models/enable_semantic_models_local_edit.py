import pyfabricops as pf

project_path="src"
workspace_alias="PFO_002_Fabric"

pf.replace_semantic_models_placeholders_with_parameters(
        project_path=project_path,
        workspace_alias=workspace_alias,
    )
