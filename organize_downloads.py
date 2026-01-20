from pathlib import Path 


DOWNLOADS_DIR = Path.home() / "Downloads"

assert DOWNLOADS_DIR.exists()

items  = list(DOWNLOADS_DIR.iterdir())

files = [p for p in items if p.is_file()]
print(f"files:",len(files))

def ext(path:Path) -> str:
    return path.suffix.lower()

print(sorted({ext(f) for f in files}))


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

def category(p:Path):
    e = ext(p)
    return  next((name for name, exts in CATS.items() if e in  exts),"Other")


sample = sorted(files,key = lambda p: ext(p))[:10]

for p in sample: print(ext(p),"->", category(p), ":" , p.name)

moves = []
for  p in files: 
  folder  = DOWNLOADS_DIR /category(p)
  moves.append((p, unique_path(folder/p.name)))

moved = errors = 0
for src, dest in moves:
  try:
    dest.parent.mkdir(exist_ok=True)
    src.rename(dest); moved+=1
  except Exception as e:
    errors+= 1


print(f"moved",moved)
print(f"errors",errors)