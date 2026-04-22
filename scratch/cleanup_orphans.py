import os
import re
import glob
import time

# Paths
BLOG_DATA_DIR = r"src\data\blog"
SOURCE_POSTS_DIR = r"source\posts"
SOURCE_ACCORDIAN_DIR = r"source\accordian"
SOURCE_GLOSSARY_DIR = r"source\glossary"

def get_referenced_files():
    referenced = set()
    md_files = glob.glob(os.path.join(BLOG_DATA_DIR, "**", "*.md"), recursive=True)
    
    # Improved Regex: match references starting with source/
    # This captures alphanumeric chars and common path symbols including parentheses
    pattern = re.compile(r'source/([a-zA-Z0-9_\-\.\/ \(\)]+?\.(?:webp|png|jpg|jpeg|txt))')
    
    for md_path in md_files:
        with open(md_path, "r", encoding="utf-8") as f:
            content = f.read()
            # Match anything starting with source/ and ending in a known extension
            matches = pattern.findall(content)
            for m in matches:
                clean_ref = m.strip()
                
                # Normalize
                ref_path = clean_ref.replace("/", os.sep).strip()
                idx = ref_path.find("source")
                if idx != -1:
                    ref_path = ref_path[idx:].lstrip(os.sep)
                
                referenced.add(os.path.normpath(ref_path).lower())
    return referenced

def cleanup(dry_run=True):
    referenced = get_referenced_files()
    total_deleted = 0
    
    # Safety window: Don't delete anything created in the last 1 hour
    current_time = time.time()
    safety_window = 3600 # 1 hour
    
    print(f"--- Orphaned Files Discovery (Dry Run: {dry_run}) ---")
    
    target_dirs = [SOURCE_POSTS_DIR, SOURCE_ACCORDIAN_DIR, SOURCE_GLOSSARY_DIR]
    orphans = []
    
    for t_dir in target_dirs:
        if not os.path.exists(t_dir):
            continue
            
        for root, dirs, files in os.walk(t_dir):
            for file in files:
                full_path = os.path.join(root, file)
                
                # Safety 1: Time check
                file_mtime = os.path.getmtime(full_path)
                if (current_time - file_mtime) < safety_window:
                    continue
                
                rel_path = os.path.relpath(full_path, os.getcwd())
                norm_rel_path = os.path.normpath(rel_path).lower()
                filename_only = file.lower()
                
                is_orphan = False
                if t_dir == SOURCE_ACCORDIAN_DIR:
                    keyword = os.path.splitext(file)[0].lower()
                    found = False
                    for ref in referenced:
                        if keyword in ref:
                            found = True
                            break
                    if not found:
                        is_orphan = True
                else:
                    # Safety 2: Strict path check OR filename partial match check
                    # To be extra safe with encoding issues, if the filename appears in any ref string, we keep it.
                    found_in_refs = False
                    if norm_rel_path in referenced:
                        found_in_refs = True
                    else:
                        for ref in referenced:
                            if filename_only in ref:
                                found_in_refs = True
                                break
                    
                    if not found_in_refs:
                        is_orphan = True
                
                if is_orphan:
                    orphans.append(full_path)

    if not orphans:
        print("✅ No orphaned files found.")
        return

    print(f"Found {len(orphans)} orphaned files:")
    for p in orphans:
        print(f"  [ORPHAN] {p}")
        if not dry_run:
            try:
                os.remove(p)
                print(f"    [DELETED] {p}")
                total_deleted += 1
            except Exception as e:
                print(f"    [ERROR] deleting {p}: {e}")

    # Cleanup empty directories
    if not dry_run:
        for t_dir in target_dirs:
            for root, dirs, files in os.walk(t_dir, topdown=False):
                for d in dirs:
                    d_path = os.path.join(root, d)
                    if not os.listdir(d_path):
                        os.rmdir(d_path)
                        print(f"  [REMOVED_DIR] {d_path}")

    print(f"\nTotal orphaned files identified: {len(orphans)}")
    if not dry_run:
        print(f"Total files deleted: {total_deleted}")

if __name__ == "__main__":
    import sys
    is_dry = "--delete" not in sys.argv
    cleanup(dry_run=is_dry)
