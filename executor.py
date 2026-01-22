from pathlib import Path
from datetime import datetime



def run(plan, tools,undo_path=Path("undo.log")):
    out = []
    log=Path(undo_path).open("a",encoding="utf-8")
    log.write(f"# RUN {datetime.utcnow().isoformat()}\n")
    for step in plan.get("steps", []):
        r=tools[step["tool"]].fn(**step["args"]);
        out.append(r); 
        moves = (r.get("moves") if isinstance(r, dict) else r) or []
        for a,b in moves: log.write(f"{a}\t{b}\n")
    log.close();
    return out