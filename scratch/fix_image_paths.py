import sys
sys.stdout.reconfigure(encoding='utf-8')
import os
import re
import glob

base_dir = "src/data/blog"
langs = ['ko', 'en', 'jp', 'cn']
folders = ['posts', 'glossary']
fixed_count = 0

# Fix image paths with parentheses in directory names
# Markdown treats ) as end of link, so we need to encode ( and ) in paths
# The fix: replace ( with %28 and ) with %29 in image paths only

print("=== Fixing parentheses in image paths ===")
for lang in langs:
    for folder in folders:
        d = os.path.join(base_dir, lang, folder)
        if not os.path.exists(d):
            continue
        for f in os.listdir(d):
            if not f.endswith('.md'):
                continue
            fp = os.path.join(d, f)
            with open(fp, 'r', encoding='utf-8') as fh:
                content = fh.read()
            
            original = content
            
            # Find markdown image patterns and encode parentheses in path
            # Pattern: ![alt](path) - but path may contain () which breaks it
            # We need to find lines with ![...](... and fix the path
            
            # Strategy: find all image-like patterns and fix the paths
            # Look for ![...](../../../../../source/posts/...) pattern
            def fix_image_path(match):
                alt = match.group(1)
                path = match.group(2)
                # Encode parentheses in path
                path = path.replace('(', '%28').replace(')', '%29')
                return f'![{alt}]({path})'
            
            # Match ![alt text](path that might have parens)
            # We need a smarter regex since ) in path breaks normal regex
            # Instead, find lines starting with ![ and manually parse
            lines = content.split('\n')
            new_lines = []
            for line in lines:
                if '![' in line and 'source/posts/' in line:
                    # Find the image tag
                    # Pattern: ![...](path/with(parens)/file.webp)
                    # Manual parse: find ![ then ] then ( then match to .webp)
                    idx = line.find('![')
                    if idx >= 0:
                        bracket_close = line.find('](', idx)
                        if bracket_close >= 0:
                            path_start = bracket_close + 2
                            # Find the .webp) ending
                            webp_idx = line.find('.webp', path_start)
                            if webp_idx >= 0:
                                path_end = webp_idx + 5  # after .webp
                                # Check if there's a closing )
                                if path_end < len(line) and line[path_end] == ')':
                                    path_end += 1  # Already properly closed
                                    path = line[path_start:webp_idx + 5]
                                else:
                                    # Path likely broken by parens, reconstruct
                                    # Look further for )
                                    close_idx = line.find(')', path_end)
                                    if close_idx >= 0:
                                        path = line[path_start:close_idx]
                                    else:
                                        path = line[path_start:webp_idx + 5]
                                
                                # Now encode parens in the path
                                encoded_path = path.replace('(', '%28').replace(')', '%29')
                                alt_text = line[idx+2:bracket_close]
                                prefix = line[:idx]
                                suffix_start = path_start + len(path)
                                if suffix_start < len(line) and line[suffix_start] == ')':
                                    suffix = line[suffix_start+1:]
                                else:
                                    suffix = line[suffix_start:] if suffix_start < len(line) else ''
                                
                                new_line = f'{prefix}![{alt_text}]({encoded_path}){suffix}'
                                if new_line != line:
                                    print(f"  [FIX] {fp}")
                                    print(f"         Before: ...{line[idx:idx+80]}...")
                                    print(f"         After:  ...{new_line[idx:idx+80]}...")
                                    fixed_count += 1
                                    line = new_line
                
                new_lines.append(line)
            
            new_content = '\n'.join(new_lines)
            if new_content != original:
                with open(fp, 'w', encoding='utf-8') as fh:
                    fh.write(new_content)

print(f"\n=== Fixed {fixed_count} image path issues ===")
