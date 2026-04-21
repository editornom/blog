import os
import re
import yaml

base_path = "src/data/blog"

# Regex to find the FAQ section in the markdown body
# Matches starting from '## ✅ ... (FAQ)' until the end of the file or next separator
faq_section_re = re.compile(r'\n*## ✅.*?\([^\)]*?FAQ[^\)]*?\)\s*(.*?)(?=\n---|\Z)', re.DOTALL)

# Regex to find individual <details> blocks
details_re = re.compile(r'<details>[\s\S]*?<summary>(.*?)</summary>[\s\S]*?<div class="faq-content">([\s\S]*?)</div>[\s\S]*?</details>', re.DOTALL)

count = 0

for root, dirs, files in os.walk(base_path):
    for file in files:
        if file.endswith(".md"):
            path = os.path.join(root, file)
            try:
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                
                # 1. Extract Frontmatter and Body
                parts = content.split("---", 2)
                if len(parts) < 3:
                    continue
                
                frontmatter_raw = parts[1]
                body = parts[2]
                
                # 2. Find FAQ block in body
                faq_match = faq_section_re.search(body)
                if not faq_match:
                    continue
                
                faq_html = faq_match.group(1)
                
                # 3. Parse <details> tags
                faqs = []
                for m in details_re.finditer(faq_html):
                    q = m.group(1).strip()
                    a = m.group(2).strip()
                    faqs.append({"q": q, "a": a})
                
                if not faqs:
                    continue
                
                # 4. Update Frontmatter
                # Load existing frontmatter to avoid overwriting or messing up formatting
                fm_data = yaml.safe_load(frontmatter_raw)
                fm_data["faqs"] = faqs
                
                new_frontmatter = yaml.dump(fm_data, allow_unicode=True, sort_keys=False, indent=2)
                
                # 5. Remove FAQ section from Body
                new_body = faq_section_re.sub("", body).strip()
                
                # 6. Reconstruct file
                new_content = f"---\n{new_frontmatter.strip()}\n---\n\n{new_body}\n"
                
                with open(path, "w", encoding="utf-8") as f:
                    f.write(new_content)
                
                print(f"[OK] Migrated: {path} ({len(faqs)} items)")
                count += 1
                
            except Exception as e:
                print(f"[ERROR] Error processing {path}: {e}")

print(f"\nMigration complete. Total files migrated: {count}")
