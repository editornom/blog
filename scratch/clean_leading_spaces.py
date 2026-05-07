import os
import re
from pathlib import Path

def clean_markdown_files():
    blog_dir = Path("src/data/blog")
    md_files = list(blog_dir.rglob("*.md"))
    fixed_count = 0
    for md_file in md_files:
        with open(md_file, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Split into frontmatter and body
        parts = content.split("---")
        if len(parts) < 3:
            continue
            
        frontmatter = parts[1]
        body = parts[2]
        
        lines = body.splitlines(keepends=True)
        modified = False
        new_lines = []
        for line in lines:
            stripped = line.lstrip()
            # If line starts with space and then normal character or ![
            # We don't want to strip list items like "  - ", "  * ", "  1. ", "  q: ", "  a: "
            # We also don't want to strip blockquotes starting with "  > "
            if line.startswith(" ") and not line.startswith("  -") and not line.startswith("  *") and not line.startswith("  >") and not re.match(r'^\s+\d+\.\s', line):
                # Let's check what the first non-space character is
                if stripped and (stripped[0].isalnum() or stripped.startswith("![") or stripped.startswith("<") or stripped.startswith("**") or stripped.startswith("“") or stripped.startswith("「") or stripped.startswith("『") or stripped.startswith("-")):
                    # Wait, if stripped starts with "-", we must make sure it's not a list item that we missed due to tab or space counts
                    if stripped.startswith("- ") or stripped.startswith("* "):
                        new_lines.append(line)
                    else:
                        new_lines.append(stripped)
                        modified = True
                    continue
            new_lines.append(line)
            
        if modified:
            new_body = "".join(new_lines)
            new_content = "---" + frontmatter + "---" + new_body
            with open(md_file, "w", encoding="utf-8", newline="") as f:
                f.write(new_content)
            print(f"Cleaned leading spaces in {md_file}")
            fixed_count += 1
            
    print(f"Finished. Cleaned {fixed_count} files.")

if __name__ == "__main__":
    clean_markdown_files()
