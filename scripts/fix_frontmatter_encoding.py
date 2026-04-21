import os
import yaml
import html

base_path = "src/data/blog"
count = 0

for root, dirs, files in os.walk(base_path):
    for file in files:
        if file.endswith(".md"):
            path = os.path.join(root, file)
            try:
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                
                parts = content.split("---", 2)
                if len(parts) < 3:
                    continue
                
                fm_data = yaml.safe_load(parts[1])
                if "faqs" in fm_data and isinstance(fm_data["faqs"], list):
                    modified = False
                    for item in fm_data["faqs"]:
                        new_q = html.unescape(item.get("q", ""))
                        new_a = html.unescape(item.get("a", ""))
                        if new_q != item.get("q") or new_a != item.get("a"):
                            item["q"] = new_q
                            item["a"] = new_a
                            modified = True
                    
                    if modified:
                        new_fm = yaml.dump(fm_data, allow_unicode=True, sort_keys=False, indent=2)
                        new_content = f"---\n{new_fm.strip()}\n---\n{parts[2]}"
                        with open(path, "w", encoding="utf-8") as f:
                            f.write(new_content)
                        print(f"[OK] Fixed encoding in: {path}")
                        count += 1
            except Exception as e:
                print(f"[ERROR] {path}: {e}")

print(f"\nEncoding fix complete. Files fixed: {count}")
