import os
import re

def fix_blank_lines(project_root):
    blog_dir = os.path.join(project_root, "src/data/blog")
    fixed_count = 0
    
    for root, dirs, files in os.walk(blog_dir):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Ensure blank lines around markdown image tags
                # Find lines that start with ![ and end with ) or ) trailing whitespace
                # and ensure they have \n\n before and after.
                
                # First, extract frontmatter to avoid modifying it
                parts = content.split('---', 2)
                if len(parts) >= 3:
                    fm = parts[1]
                    body = parts[2]
                else:
                    fm = ""
                    body = content
                
                # Replace <p>![...]</p> directly to \n\n![...]\n\n just in case there are any left
                body = re.sub(r'<p>\s*(!\[.*?\]\(.*?\))\s*</p>', r'\n\n\1\n\n', body)
                
                # For images already on their own lines without blank lines:
                # We can use regex to find ![...] and surround with \n\n
                # r'(?<!\n\n)(!\[.*?\]\(.*?\))(?!(\n\n))' -> wait, easier to just replace any \n![ with \n\n![
                # and ) \n with )\n\n
                
                # Split body by lines
                lines = body.split('\n')
                new_lines = []
                for i, line in enumerate(lines):
                    stripped = line.strip()
                    if stripped.startswith('![') and stripped.endswith(')'):
                        # It's an image line
                        if new_lines and new_lines[-1].strip() != '':
                            new_lines.append('') # Add blank line before
                        new_lines.append(stripped)
                        new_lines.append('') # Add blank line after
                    else:
                        new_lines.append(line)
                        
                # Join back
                fixed_body = '\n'.join(new_lines)
                # Cleanup multiple blank lines
                fixed_body = re.sub(r'\n{3,}', '\n\n', fixed_body)
                
                new_content = content
                if fm:
                    new_content = f"---{fm}---{fixed_body}"
                else:
                    new_content = fixed_body
                
                if new_content != content:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"Added blank lines around images in {file_path}")
                    fixed_count += 1
                    
    print(f"Total files fixed: {fixed_count}")

if __name__ == "__main__":
    fix_blank_lines(os.getcwd())
