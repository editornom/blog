import os
import re
import sys
import yaml
import datetime

# Add scripts directory to path
sys.path.append(os.path.abspath("scripts"))

from reviewer import review_manuscript

file_path = r"src\data\blog\ko\posts\260422_oauth-supply-chain-security-risks-lessons.md"

with open(file_path, "r", encoding="utf-8") as f:
    orig_content = f.read()

# Run the review (which now has the Tech Magazine persona)
reviewed_content = review_manuscript(orig_content)

# Update metadata
yaml_match = re.match(r'^---\s*\n(.*?)\n---\s*\n', reviewed_content, re.DOTALL)
if yaml_match:
    fm_raw = yaml_match.group(1)
    body = reviewed_content[yaml_match.end():]
    fm = yaml.safe_load(fm_raw)
    
    # Update EEAT fields
    fm['author_role'] = "Senior Tech Editor"
    fm['modDatetime'] = datetime.datetime.now().astimezone().isoformat()
    
    new_fm = yaml.dump(fm, allow_unicode=True, sort_keys=False)
    final_content = f"---\n{new_fm}---\n\n{body.strip()}\n"
else:
    final_content = reviewed_content

with open(file_path, "w", encoding="utf-8") as f:
    f.write(final_content)

print(f"Successfully refreshed {file_path} with Tech Magazine persona.")
