import os

BLOG_DIR = r"c:\Users\haionnet\Desktop\editornom\src\data\blog"
DATES = ["260508_", "260509_", "260510_", "260511_"]

matching_files = []
for root, dirs, files in os.walk(BLOG_DIR):
    for file in files:
        if file.endswith(".md") and any(file.startswith(date) for date in DATES):
            matching_files.append(os.path.relpath(os.path.join(root, file), BLOG_DIR))

matching_files.sort()
print(f"Total files: {len(matching_files)}")
for f in matching_files:
    print(f)
