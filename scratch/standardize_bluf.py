import os
import re

def standardize_bluf(project_root):
    blog_dir = os.path.join(project_root, "src/data/blog")
    fixed_count = 0
    
    # Regex to match <aside> or <div> with class bluf and capture its inner text, removing any inner tags like <strong> or <p> for a clean rebuild.
    # It's better to capture the whole tag and then extract the text.
    bluf_pattern = re.compile(r'<(div|aside)[^>]*class=["\']bluf["\'][^>]*>(.*?)</\1>', re.IGNORECASE | re.DOTALL)
    
    for root, dirs, files in os.walk(blog_dir):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                new_content = content
                matches = bluf_pattern.finditer(content)
                for match in matches:
                    original_match = match.group(0)
                    inner_html = match.group(2)
                    
                    # Strip all tags from inner_html to get pure text
                    pure_text = re.sub(r'<[^>]+>', '', inner_html)
                    # Remove the prefix like [BLUF: ... ] or [핵심 요약]
                    pure_text = re.sub(r'\[(BLUF|핵심 요약)[^\]]*\]', '', pure_text, flags=re.IGNORECASE).strip()
                    
                    # Also replace any leading colons or hyphens
                    pure_text = re.sub(r'^[:\-]\s*', '', pure_text).strip()
                    
                    # Rebuild
                    replacement = f'\n\n<div class="bluf"><strong>[BLUF]</strong><p>{pure_text}</p></div>\n\n'
                    
                    new_content = new_content.replace(original_match, replacement)
                
                # Cleanup multiple newlines
                new_content = re.sub(r'\n{3,}', '\n\n', new_content)
                
                if new_content != content:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"Standardized BLUF in {file_path}")
                    fixed_count += 1
                    
    print(f"Total files standardized: {fixed_count}")

if __name__ == "__main__":
    standardize_bluf(os.getcwd())
