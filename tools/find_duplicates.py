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
    if duplicates:
        cleanup_choice = input("\nClean up duplicates? (y/n): ").strip().lower()
        if cleanup_choice == 'y':
           interactive_cleanup(duplicates)
        else : print("Cleanup skipped.")

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

def find_duplicates(path, method="hash", dry_run=True) -> dict[str, list[str]]:
        """Find duplicate groups by hash."""
        folder = Path(str(path).strip()).expanduser().resolve()
        dups = _find_duplicates(folder) 
        groups=[{"hash":h,"paths":ps} for h,ps in dups.items()]
        return {"tool":"dedupe","dry_run":dry_run,"method":method,"groups":groups,"group_count":len(groups)}

def _find_duplicates(folder:Path):
        hash_to_paths = defaultdict(list)
        if not folder.is_dir():
            raise ValueError(f"Not a directory: {root}")


        for path in  root.rglob('*'):
           try:
                if path.is_file() and not path.name.startswith(".") and not path.is_symlink():
                    file_hash = get_file_hash(path)
                    hash_to_paths[file_hash].append(str(path))
            
           except Exception as e:
                continue
        duplicates_only = {h:paths for  h,paths in  hash_to_paths.items() if len(paths) > 1}
        return duplicates_only 

def human_size(size_bytes: int) -> str:
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 ** 2:
        return f"{size_bytes / 1024:.1f} KB"
    elif size_bytes < 1024 ** 3:
        return f"{size_bytes / (1024 ** 2):.1f} MB"
    elif size_bytes < 1034 ** 4:
        return f"{size_bytes/(1024 ** 3):.1f}GB"
    return f"{size_bytes / (1024 ** 4):.2f} TB"
def print_duplicate_groups(duplicates: dict[str,list[str]]):
   """ Display duplicate groups nicel. """
   if not duplicates:
     print("No duplicate groups found.")
     return
   print(f"Found {len(duplicates)} group(s) of duplicates:")

   for hash_val, paths in duplicates.items():
       print(f"\n Group (hash :{hash_val[:12]}....):" )
       for p in paths:
          size_bytes = Path(p).stat().st_size
          print(f"{p}")
          print(f"     size: {human_size(size_bytes)}")
          mtime = Path(p).stat().st_mtime
          mtime_str = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M")
          print(f"     modified: {mtime_str}")
          print("-" * 60)
       if len(paths) > 1:
            saved = (len(paths) - 1) * size_bytes
            print(f"    Potential space saved if keep 1: {human_size(saved)}")
   total_saved = sum((len(paths) - 1) * Path(paths[0]).stat().st_size for paths in duplicates.values())
   if total_saved > 0:
        print(f"\nTotal potential space saved: {human_size(total_saved)}")


def interactive_clearnup(duplicates: dict[str,list[str]]):
    """ Ask user what to delete per group. """
    for hash_val , paths in  duplicates.items():
        print(f"\nGroup (hash:{hash_val[:12]}...):")
        for idx , p in enumerate(paths, 1):
            print(f"   {idx}: {p}")
        choice = input("\nDelete which? (comma-separated numbers, 'a' all but first, 'n' none): ").strip().lower()
        if choice == 'n':
            continue
        if choice == 'a':
            to_delete = paths[1:]
        else:
            to_delete_idx = [int(i.strip()) - 1 for i in choice.split(',') if i.strip().isdigit()]
            to_delete = [paths[idx] for idx in to_delete_idx if 0 <= idx < len(paths)]
            for file_path in to_delete:
                try:
                    Path(file_path).unlink()
                    print(f"Deleted: {file_path}")
                except Exception as e:
                    print(f"Failed to delete {file_path}: {e}")
if __name__ == "__main__":
     main()
