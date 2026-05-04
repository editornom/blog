import os
import re

def ensure_spacing_and_fix_headers(project_root):
    blog_dir = os.path.join(project_root, "src/data/blog")
    
    for root, dirs, files in os.walk(blog_dir):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                parts = content.split('---', 2)
                if len(parts) < 3:
                    continue
                
                fm = parts[1]
                body = parts[2]
                
                # 1. Ensure empty line before H2 headers
                # We look for any text immediately followed by ## Title
                # [^\n] matches any char except newline. \n## matches a newline followed by ##.
                # We replace with \n\n##
                fixed_body = re.sub(r'([^\n])\n##\s', r'\1\n\n## ', body)
                
                # 2. Ensure empty line AFTER H2 headers (if missing)
                # fixed_body = re.sub(r'\n##\s([^\n]+)\n([^\n])', r'\n## \1\n\n\2', fixed_body)
                
                if fixed_body != body:
                    new_content = f"---{fm}---{fixed_body}"
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"Improved spacing in {file_path}")

if __name__ == "__main__":
    ensure_spacing_and_fix_headers(os.getcwd())
