import os
import sys

# Add scratch to path or copy checker logic
sys.path.append(r"c:\Users\haionnet\Desktop\editornom\scratch")
from comprehensive_checker import check_markdown_file, BLOG_DIR, DATES

matching_files = []
for root, dirs, files in os.walk(BLOG_DIR):
    for file in files:
        if file.endswith(".md") and any(file.startswith(date) for date in DATES):
            matching_files.append(os.path.join(root, file))

matching_files.sort()

error_files = []
for fp in matching_files:
    ok, errs, warns, fm, imgs, b_locals = check_markdown_file(fp)
    if not ok:
        error_files.append((os.path.relpath(fp, BLOG_DIR), errs))

print(f"Total error files: {len(error_files)}")
for f, errs in error_files:
    print(f"\n❌ {f}")
    for err in errs:
        print(f"   {err}")
