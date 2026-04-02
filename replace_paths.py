import os

langs = ["en", "cn", "jp"]
base_dir = r"src/pages"

for lang in langs:
    target_dir = os.path.join(base_dir, lang)
    for root, dirs, files in os.walk(target_dir):
        for file in files:
            if file.endswith(".astro"):
                file_path = os.path.join(root, file)
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                
                # Replace occurrences of "/ko/" with the current language path
                new_content = content.replace('"/ko/"', f'"/{lang}/"')
                new_content = new_content.replace("'/ko/'", f"'/{lang}/'")
                
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(new_content)

print("Replacement done.")
