import os
import re

def test_regex_fix(path):
    print(f"=== Testing Regex Fix on: {path} ===")
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    parts = content.split('---', 2)
    if len(parts) < 3:
        print("Failed to split frontmatter.")
        return
        
    body = parts[2]
    print("Original body actual newlines:", body.count('\n'))
    
    # Let's apply regex to restore newlines
    # Add newlines before headings
    fixed = re.sub(r'(?<!\n)(##+ )', r'\n\n\1', body)
    # Add newlines before images
    fixed = re.sub(r'(?<!\n)(!\[)', r'\n\n\1\n\n', fixed)
    # Add newlines before blockquotes
    fixed = re.sub(r'(?<!\n)(>\s+)', r'\n\n\1', fixed)
    
    # Wait, tables are tricky, we can do it before '|' but only if there's no '|' earlier on the same line
    # Let's see if we can split by '|' or handle tables simply
    # For eBPF, we can also restore lists
    fixed = re.sub(r'(?<!\n)(\*\s+)', r'\n\1', fixed)
    
    # Let's see how it looks
    print("Fixed body actual newlines:", fixed.count('\n'))
    print("First 1500 chars of fixed body:")
    print(fixed[:1500])

test_regex_fix('src/data/blog/ko/posts/260511_ebpf-linux-kernel-semantic-gap.md')
