from pathlib import Path 


def ext(path:Path) -> str:
    return path.suffix.lower()

CATS = {
 "Images":{".png",".jpg",".jpeg"},
 "Docs":{".pdf"},
 "Data":{".csv",".xlsx"},
 "3D":{".fbx",".glb",".blend1"},
 "Zips":{".zip"}
}

def unique_path(dest: Path) -> Path:
    if not dest.exists(): return dest

    stem , suffix =  dest.stem , dest.suffix

    for i in range(1, 10000):
         cand = dest.with_name(f"{stem}-{i}{suffix}")
         if not cand.exists(): return cand
    raise RuntimeError(f"No unique name for {dest}")

def category(p:Path):
    e = ext(p)
    return  next((name for name, exts in CATS.items() if e in  exts),"Other")



def organize_files(path:Path,dry_run=True):
    DOWNLOADS_DIR = Path(path).expanduser().resolve()
    if not DOWNLOADS_DIR.is_dir(): raise ValueError(f"Not a directory: {DOWNLOADS_DIR}")
    assert DOWNLOADS_DIR.exists()

    items  = list(DOWNLOADS_DIR.iterdir())

    files = [p for p in items if p.is_file()]
    print(f"files:",len(files))
    # print(sorted({ext(f) for f in files}))

    sample = sorted(files,key = lambda p: ext(p))[:10]
    for p in sample: print(ext(p),"->", category(p), ":" , p.name)
    moves = []
    for  p in files: 
      folder  = DOWNLOADS_DIR /category(p)
      moves.append((p, unique_path(folder/p.name)))

    moved = errors = 0
    moves_done = []
    for src, dest in moves:
      try:
        moves_done.append((str(src), str(dest)))
        (dest.parent.mkdir(parents=True, exist_ok=True), src.rename(dest), moved:=moved+1) if (not dry_run) else None
        return {"tool":"organize","dry_run":dry_run,"moved":moved,"errors":errors,"moves":moves_done}
      except Exception as e:
        errors+= 1

     
    print(f"moved",moved)
    print(f"errors",errors)