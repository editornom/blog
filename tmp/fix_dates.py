import os
import re

def fix_all_dates():
    root_dir = 'src/data/blog'
    # Target date: Today at the very beginning of the day (UTC)
    target_time = '2026-04-07T00:01:00Z'
    
    count = 0
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.md'):
                path = os.path.join(root, file)
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # If pubDatetime is in the future (today's afternoon UTC time)
                if 'pubDatetime: 2026-04-07T' in content:
                    # Specifically look for times that are today
                    new_content = re.sub(r'pubDatetime: 2026-04-07T[0-9:.]+Z', f'pubDatetime: {target_time}', content)
                    if content != new_content:
                        with open(path, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        print(f"Fixed date for: {path}")
                        count += 1
    
    print(f"Total files updated: {count}")

if __name__ == "__main__":
    fix_all_dates()
