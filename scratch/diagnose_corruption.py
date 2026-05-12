import os

BLOG_DIR = r"c:\Users\haionnet\Desktop\editornom\src\data\blog"
DATES = ["260508_", "260509_", "260510_", "260511_"]

corrupted_files = []
for root, dirs, files in os.walk(BLOG_DIR):
    for file in files:
        if file.endswith(".md") and any(file.startswith(date) for date in DATES):
            fp = os.path.join(root, file)
            with open(fp, 'r', encoding='utf-8') as f:
                content = f.read()
            # Check for literal \n or escaped quotes class=\"
            if "\\n" in content or 'class=\\"' in content:
                corrupted_files.append(os.path.relpath(fp, BLOG_DIR))

print(f"Corrupted files count: {len(corrupted_files)}")
for cf in corrupted_files:
    print(cf)
