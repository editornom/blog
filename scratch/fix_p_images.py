import os
import re

def fix_p_images(project_root):
    blog_dir = os.path.join(project_root, "src/data/blog")
    fixed_count = 0
    
    for root, dirs, files in os.walk(blog_dir):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                fixed_content = re.sub(r'<p>\s*(!\[.*?\]\(.*?\))\s*</p>', r'\n\1\n', content)
                
                if fixed_content != content:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(fixed_content)
                    print(f"Fixed images in {file_path}")
                    fixed_count += 1
                    
    print(f"Total files fixed: {fixed_count}")

if __name__ == "__main__":
    fix_p_images(os.getcwd())
