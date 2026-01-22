from dataclasses import dataclass
@dataclass(frozen=True)
class Request: text:str; path:str; dry_run:bool=True

def parse(argv_or_text, path)->Request:
    p = str(path).strip()
    p = p.replace("\\ ", " ")
    return Request(text=str(argv_or_text).strip(), path=p, dry_run=True)