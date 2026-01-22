from dataclasses import dataclass
from tools import organize_files, find_duplicates

@dataclass(frozen=True)
class Tool: name:str; desc:str; fn:callable; args_schema:dict

TOOLS: dict[str, Tool] = {}

def register(t: Tool) -> None:
    TOOLS[t.name] = t



register(Tool("organize","Organize files in a folder",organize_files,{"path":str,"dry_run":bool}))
register(Tool("dedupe","Find duplicate files",find_duplicates,{"path":str,"method":None,"dry_run":bool}))