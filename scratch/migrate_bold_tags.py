import os
import re
import glob

def migrate_bold_tags(target_dir):
    md_files = glob.glob(os.path.join(target_dir, "**", "*.md"), recursive=True)
    
    # Pattern to find **text** while avoiding single * or ***
    # This regex ensures we only match double asterisks
    pattern = re.compile(r'\*\*([^*]+)\*\*')
    
    total_files = 0
    total_matches = 0
    
    for file_path in md_files:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Simple parser to skip code blocks
        parts = re.split(r'(```[\s\S]*?```|`[^`]*?`)', content)
        new_parts = []
        file_matches = 0
        
        for part in parts:
            if part.startswith('`'):
                # Skip code blocks and inline code
                new_parts.append(part)
            else:
                # Replace in regular text
                matches = pattern.findall(part)
                file_matches += len(matches)
                new_parts.append(pattern.sub(r'<b>\1</b>', part))
        
        new_content = "".join(new_parts)
        
        if new_content != content:
            total_files += 1
            total_matches += file_matches
            print(f"Migrated: {file_path} ({file_matches} matches)")
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
                
    print(f"\nMigration Complete!")
    print(f"Total files updated: {total_files}")
    print(f"Total tags converted: {total_matches}")

if __name__ == "__main__":
    import sys
    target = "src/data/blog" if len(sys.argv) < 2 else sys.argv[1]
    migrate_bold_tags(target)
