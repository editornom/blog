import os
import re

def fix_headers(project_root):
    blog_dir = os.path.join(project_root, "src/data/blog")
    
    # Pattern to match lines like **Title** or **Title:** on their own line
    # We allow optional colon at the end.
    header_pattern = re.compile(r'^\s*\*\*([^*]+?)\:?\*\*\s*$', re.MULTILINE)

    for root, dirs, files in os.walk(blog_dir):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Split frontmatter and body
                parts = content.split('---', 2)
                if len(parts) < 3:
                    continue
                
                fm = parts[1]
                body = parts[2]
                
                # Replace **Title** with ## Title
                # We use group 1 (the title text)
                new_body = header_pattern.sub(r'## \1', body)
                
                # Also handle some edge cases like '### **Title**' -> '### Title'
                new_body = re.sub(r'### \*\*([^*]+)\*\*', r'### \1', new_body)
                new_body = re.sub(r'## \*\*([^*]+)\*\*', r'## \1', new_body)
                
                if new_body != body:
                    new_content = f"---{fm}---{new_body}"
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"Fixed headers in {file_path}")

if __name__ == "__main__":
    fix_headers(os.getcwd())
