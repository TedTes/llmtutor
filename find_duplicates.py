from pathlib import Path
import sys
from collections import  defaultdict
import hashlib
from datetime import datetime

def main():
    print("Duplicate  File Finder")
    print("-----------------------")
    folder_input = input("Folder to scan (Enter = current):").strip()
    if not folder_input:
          folder_input = "."
    folder = Path(folder_input).resolve()
    if not folder.is_dir():
        print(f"Error:'{folder}' is not a directory.")
        sys.exit(1)
    print(f"\n Scanning: {folder}")
    print("This may take a while downloading on folder size..")

    test_path = Path(__file__).resolve()
    hash_value = get_file_hash(test_path)
    print(f"Hash of this script:{hash_value}")

    duplicates = find_duplicates(folder)
  
    print_duplicate_groups(duplicates)


def  get_file_hash(path:Path) -> str:
    """ Compute SHA-256 hash of file content."""
    try :
        sha256 = hashlib.sha256()
        with open(path, 'rb') as f:
            while True:
                chunk = f.read(65536)
                if not chunk: 
                    break
                sha256.update(chunk)
        return sha256.hexdigest()
    except  Exception as e:
        print(f"error occured in get_file_hash method",e)
        raise RuntimeError(f"Failed to hash {path}: {e}")

def find_duplicates(folder: Path) -> dict[str, list[str]]:
        """Find duplicate groups by hash."""
  
        hash_to_paths = defaultdict(list)
        root = folder.resolve()
        if not root.is_dir:
            raise ValueError(f"Not a directory: {root}")


        for path in  root.rglob('*'):
           try:
                if path.is_file() and not path.name.startswith(".") and not path.is_symlink():
                    file_hash = get_file_hash(path)
                    hash_to_paths[file_hash].append(str(path))
            
           except Exception as e:
                print(f"error in find_duplicates",e)
                continue
        duplicates_only = {h:paths for  h,paths in  hash_to_paths.items() if len(paths) > 1}
        return duplicates_only 

def human_size(size_bytes: int) -> str:
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 ** 2:
        return f"{size_bytes / 1024:.1f} KB"
    elif size_bytes < 1024 ** 3:

def print_duplicate_groups(duplicates: dict[str,list[str]]):
   """ Display duplicate groups nicel. """
   if not duplicates:
     print("No duplicate groups found.")
     return
   print(f"Found {len(duplicates)} group(s) of duplicates:")

   for hash_val, paths in duplicates.items():
       print(f"\n Group (hash :{hash_val[:12]}....):" )
       for p in paths:
          size_kb = Path(p).stat().st_size/1024
          print(f"{p} ({size_kb:,.1f}KB)")
          mtime = Path(p).stat().st_mtime
          mtime_str = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M")
          print(f"     modified: {mtime_str}")
          print("-" * 60)
if __name__ == "__main__":
     main()
