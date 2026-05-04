import os
import re

def fix_headers_comprehensive(project_root):
    blog_dir = os.path.join(project_root, "src/data/blog")
    
    # 1. Bolded text on its own line -> H2
    # re.MULTILINE is used to match ^ and $ at start/end of lines
    bold_pattern = re.compile(r'^\s*\*\*([^*]+?)\:?\*\*\s*$', re.MULTILINE)
    
    # 2. H3 at start of line -> H2
    # We only do this in the body (after the frontmatter)
    h3_pattern = re.compile(r'^###\s', re.MULTILINE)

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
                
                # Apply transformations
                new_body = bold_pattern.sub(r'## \1', body)
                new_body = h3_pattern.sub(r'## ', new_body)
                
                # Clean up any Double-H2 that might have resulted from promoting H3
                # e.g. if someone wrote ## **Title** and we converted it... wait.
                # Let's handle ## **Title** -> ## Title
                new_body = re.sub(r'## \*\*([^*]+)\*\*', r'## \1', new_body)
                
                # Check for duplicate H2 headers like "## ## Title"
                new_body = re.sub(r'^##\s+##\s+', r'## ', new_body, flags=re.M)
                
                if new_body != body:
                    new_content = f"---{fm}---{new_body}"
                    # Use PowerShell to write to avoid encoding issues if possible, 
                    # but here we are in Python, so let's try writing normally first.
                    try:
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        print(f"Fixed headers in {file_path}")
                    except Exception as e:
                        print(f"Error writing {file_path}: {e}")

if __name__ == "__main__":
    fix_headers_comprehensive(os.getcwd())
