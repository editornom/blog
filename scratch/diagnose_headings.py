import os
import re
import sys

BLOG_DIR = r"c:\Users\haionnet\Desktop\editornom\src\data\blog"
DATES = ["260508_", "260509_", "260510_", "260511_"]

matching_files = []
for root, dirs, files in os.walk(BLOG_DIR):
    for file in files:
        if file.endswith(".md") and any(file.startswith(date) for date in DATES) and "posts" in root:
            matching_files.append(os.path.join(root, file))
            
matching_files.sort()

report_lines = []
for fp in matching_files:
    rel_path = os.path.relpath(fp, BLOG_DIR)
    with open(fp, 'r', encoding='utf-8') as f:
        content = f.read()
        
    parts = content.split("---", 2)
    if len(parts) < 3:
        continue
    body = parts[2]
    
    # Find lines starting with #, ##, ### in body
    headers = [line.strip() for line in body.split("\n") if line.strip().startswith("#")]
    report_lines.append(f"{rel_path}: {headers}")

with open(r"c:\Users\haionnet\Desktop\editornom\scratch\headings_report.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(report_lines))

print("Report written successfully.")
