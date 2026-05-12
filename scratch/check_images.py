import os
import re
import yaml

# Directories to search
BLOG_DIR = r"c:\Users\haionnet\Desktop\editornom\src\data\blog"
DATES = ["260506_", "260507_", "260508_", "260509_", "260510_"]

print("=" * 80)
print(f"Starting image check for dates {DATES} in {BLOG_DIR}")
print("=" * 80)

# Statistics
total_files_checked = 0
total_images_checked = 0
broken_images = []

# Regular expressions for finding images in markdown text
MD_IMAGE_REGEX = re.compile(r"!\[.*?\]\((.*?)\)")
HTML_IMAGE_REGEX = re.compile(r'<img\s+[^>]*src=["\'](.*?)["\']', re.IGNORECASE)

# Walk through the blog directory
for root, dirs, files in os.walk(BLOG_DIR):
    for file in files:
        # Check if the file name starts with one of our target dates and is a markdown file
        if file.endswith(".md") and any(file.startswith(date) for date in DATES):
            file_path = os.path.join(root, file)
            rel_file_path = os.path.relpath(file_path, BLOG_DIR)
            total_files_checked += 1
            
            # Read file content
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Parse frontmatter to find ogImage
            og_image = None
            if content.startswith("---"):
                parts = content.split("---", 2)
                if len(parts) >= 3:
                    try:
                        frontmatter = yaml.safe_load(parts[1])
                        if frontmatter and 'ogImage' in frontmatter:
                            og_image = frontmatter['ogImage']
                    except Exception as e:
                        print(f"[Error parsing frontmatter] {rel_file_path}: {e}")
            
            # Find all markdown/HTML images
            md_images = MD_IMAGE_REGEX.findall(content)
            html_images = HTML_IMAGE_REGEX.findall(content)
            
            all_referenced_images = []
            if og_image:
                all_referenced_images.append(('ogImage', og_image))
            for img in md_images:
                all_referenced_images.append(('markdown', img))
            for img in html_images:
                all_referenced_images.append(('html', img))
                
            file_has_error = False
            file_report = []
            
            for img_type, img_path in all_referenced_images:
                total_images_checked += 1
                # Standardize path
                # Clean query params or anchors if any (unlikely in local images, but good practice)
                clean_img_path = img_path.split('?')[0].split('#')[0]
                
                # Check if it is a local relative path
                if not (clean_img_path.startswith("http://") or clean_img_path.startswith("https://") or clean_img_path.startswith("//")):
                    # Resolve path relative to the markdown file's directory
                    resolved_path = os.path.normpath(os.path.join(root, clean_img_path))
                    exists = os.path.exists(resolved_path)
                    
                    if not exists:
                        file_has_error = True
                        broken_images.append({
                            'file': rel_file_path,
                            'type': img_type,
                            'referenced_path': img_path,
                            'resolved_path': resolved_path
                        })
                        file_report.append(f"  [BROKEN] {img_type}: '{img_path}' -> Resolved to: '{resolved_path}'")
                    else:
                        file_report.append(f"  [OK] {img_type}: '{img_path}'")
                else:
                    file_report.append(f"  [EXTERNAL] {img_type}: '{img_path}'")
            
            if file_has_error:
                print(f"\n❌ {rel_file_path}")
                for line in file_report:
                    if "[BROKEN]" in line:
                        print(line)
            else:
                # Optionally print OK files too
                # print(f"\n✅ {rel_file_path}")
                pass

print("\n" + "=" * 80)
print("SUMMARY REPORT")
print("=" * 80)
print(f"Total markdown files matching date criteria: {total_files_checked}")
print(f"Total image references checked: {total_images_checked}")
print(f"Total broken image references found: {len(broken_images)}")

if broken_images:
    print("\nDetailed list of broken images:")
    for idx, bi in enumerate(broken_images, 1):
        print(f"{idx}. File: {bi['file']}")
        print(f"   Type: {bi['type']}")
        print(f"   Referenced: {bi['referenced_path']}")
        print(f"   Resolved to: {bi['resolved_path']}")
else:
    print("\n🎉 Excellent! No broken image references found!")
print("=" * 80)
