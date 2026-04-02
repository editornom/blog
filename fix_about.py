import os

langs = ["ko", "en", "cn", "jp"]
base_dir = "src/pages"

for lang in langs:
    file_path = os.path.join(base_dir, lang, "about.md")
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Fix layout path and ensure it's not double-replaced
    if 'layout: ../layouts/AboutLayout.astro' in content:
        content = content.replace('layout: ../layouts/AboutLayout.astro', 'layout: ../../layouts/AboutLayout.astro')
        
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

print("Fixed layout paths in all about.md files.")
