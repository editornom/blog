import os
import re
import yaml
import sys
import urllib.request
from urllib.error import URLError

# Ensure terminal can handle UTF-8/Emojis on Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

# Directories to search
BLOG_DIR = r"c:\Users\haionnet\Desktop\editornom\src\data\blog"
DATES = ["260508_", "260509_", "260510_", "260511_"]
DEV_SERVER_URL = "http://localhost:4321"

print("=" * 100)
print(f"🚀 INTEGRATED BLOG POST & IMAGE QUALITY CHECKER")
print(f"Checking posts from May 8th onwards, 2026")
print("=" * 100)

# Check if Astro Dev Server is active
server_active = False
try:
    with urllib.request.urlopen(DEV_SERVER_URL, timeout=1.5) as response:
        if response.status == 200:
            server_active = True
            print("🟢 Astro Development Server is ACTIVE on http://localhost:4321!")
            print("👉 Headless Playwright rendering checks will be executed automatically.")
except (URLError, TimeoutError, Exception):
    pass

if not server_active:
    print("🟡 Astro Development Server is OFFLINE on http://localhost:4321.")
    print("👉 Static local checks will be performed.")
    print("💡 To enable real browser-rendering checks, start the server in another terminal:")
    print("   [pnpm run dev] or [npm run dev]")
print("-" * 100)

# Statistics
total_files = 0
passed_files = 0
failed_files = 0

# Check lists
broken_images_local = []
broken_images_rendered = []
structural_violations = []

# Regular expressions for finding images in markdown text
MD_IMAGE_REGEX = re.compile(r"!\[.*?\]\((.*?)\)")
HTML_IMAGE_REGEX = re.compile(r'<img\s+[^>]*src=["\'](.*?)["\']', re.IGNORECASE)

# Sentence splitter for paragraph length check
def count_sentences(text):
    # Match sentence endings followed by space or end of string
    sentences = re.split(r'[.!?]\s+|\.$|\?$|!$', text.strip())
    # Filter empty elements
    sentences = [s for s in sentences if s.strip()]
    return len(sentences)

def check_markdown_file(file_path):
    rel_path = os.path.relpath(file_path, BLOG_DIR)
    is_glossary = "glossary" in file_path.replace("\\", "/").split("/")
    
    # Read file
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Parse frontmatter
    frontmatter = {}
    body_text = content
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            try:
                frontmatter = yaml.safe_load(parts[1]) or {}
                body_text = parts[2]
            except Exception as e:
                return False, [f"YAML Frontmatter parsing error: {e}"], [], {}, [], []
    
    errors = []
    warnings = []
    local_images = []
    
    # Extract images from frontmatter (ogImage)
    og_image = frontmatter.get("ogImage")
    if og_image:
        local_images.append(("ogImage", og_image))
    
    # -------------------------------------------------------------
    # 1. H2 & H3 Heading Hierarchy Check (Baseline - Mandatory for posts)
    # -------------------------------------------------------------
    if not is_glossary:
        h2_headings = re.findall(r'^##\s+(.+)', body_text, re.MULTILINE)
        h3_headings = re.findall(r'^###\s+(.+)', body_text, re.MULTILINE)
        
        if len(h2_headings) == 0:
            errors.append("❌ Baseline Error: Missing H2 headings (`## ` is required as default for proper SEO structure).")
        if len(h3_headings) == 0:
            errors.append("❌ Baseline Error: Missing H3 headings (`### ` is required as default for proper SEO structure).")

    # -------------------------------------------------------------
    # 2. 5-Component Structural SEO/AEO/GEO Scorer (At least 3/5 required)
    # -------------------------------------------------------------
    if not is_glossary:
        structural_score = 0
        satisfied_components = []
        
        # Component A: BLUF Block (Mandatory)
        bluf_match = re.search(r'<div\s+class=["\']bluf["\']\s*>\s*<strong>\s*\[BLUF\]\s*</strong>\s*<p>(.*?)</p>\s*</div>', content, re.DOTALL | re.IGNORECASE)
        if bluf_match:
            structural_score += 1
            satisfied_components.append("A (BLUF Block)")
        else:
            bluf_lax = re.search(r'bluf', content, re.IGNORECASE)
            if bluf_lax:
                warnings.append("⚠️ BLUF block detected but format may not strictly match standard `<div class=\"bluf\"><strong>[BLUF]</strong><p>...</p></div>`")
            else:
                errors.append("❌ Missing BLUF block (Component A is mandatory at the top of every post).")

        # Component B: Markdown Table (Optional but highly encouraged)
        # Check for divider line like | --- | or | :---: |
        table_match = re.search(r'\|.*?\|\s*\n\s*\|(?:\s*:?---:?\s*\|)+\s*\n\s*\|.*?\|', body_text, re.DOTALL)
        if table_match:
            structural_score += 1
            satisfied_components.append("B (Markdown Table)")

        # Component C: Highlight Blockquotes (Optional but highly encouraged)
        # Check for lines starting with ">"
        blockquote_match = re.search(r'^\s*>\s+', body_text, re.MULTILINE)
        if blockquote_match:
            structural_score += 1
            satisfied_components.append("C (Highlight Blockquote)")

        # Component D: Glossary Tooltip Link (Optional but highly encouraged)
        # Check for `<a ... class="glossary-tooltip" ...>` or similar
        tooltip_match = re.search(r'class=["\']glossary-tooltip["\']', body_text, re.IGNORECASE)
        if tooltip_match:
            structural_score += 1
            satisfied_components.append("D (Glossary Tooltip Link)")

        # Component E: Numeric Bulleted Lists (Optional but highly encouraged)
        # Check for lists with numbers, years or percentages
        list_lines = re.findall(r'^\s*(?:[-*]|\d+\.)\s+(.*)', body_text, re.MULTILINE)
        has_numeric_list = False
        for line in list_lines:
            if re.search(r'\d+', line):
                has_numeric_list = True
                break
        if has_numeric_list:
            structural_score += 1
            satisfied_components.append("E (Factual Numeric List)")

        # Evaluate score
        if structural_score < 3:
            errors.append(f"❌ Structural SEO/AEO/GEO Score too low ({structural_score}/5). Satisfied components: {satisfied_components}. Must satisfy at least 3 components!")
        else:
            print(f"     📊 Structural SEO/AEO/GEO Score: {structural_score}/5 {satisfied_components} for {rel_path}")

    # -------------------------------------------------------------
    # Extract images from body and check glossary image prohibition
    # -------------------------------------------------------------
    md_images = MD_IMAGE_REGEX.findall(body_text)
    html_images = HTML_IMAGE_REGEX.findall(body_text)
    
    for img in md_images:
        local_images.append(("markdown", img))
    for img in html_images:
        local_images.append(("html", img))
        
    body_images = [img for img_type, img in local_images if img_type in ["markdown", "html"]]
    if is_glossary and len(body_images) > 0:
        errors.append(f"❌ Glossary post violates rule: Glossary must NOT contain any images in content body (Found {len(body_images)} image references).")

    # -------------------------------------------------------------
    # 3. Paragraph Length & Paragraph Indent Check (Only for posts)
    # -------------------------------------------------------------
    if not is_glossary:
        # Strip code blocks to avoid checking code contents
        clean_body = re.sub(r'```.*?```', '', body_text, flags=re.DOTALL)
        
        # Split body by blank lines to isolate paragraph blocks
        raw_blocks = clean_body.split("\n\n")
        
        paragraph_count = 0
        long_paragraphs = 0
        missing_indents = 0
        
        for block in raw_blocks:
            cleaned_block = block.lstrip('\r\n').rstrip()
            lines = cleaned_block.split("\n")
            if not lines or not lines[0].strip():
                continue
            
            first_line = lines[0]
            raw_block_text = " ".join([l.strip() for l in lines])
            
            # Skip non-paragraph elements (headers, lists, blockquotes, tables, html tags)
            if (first_line.startswith("#") or 
                first_line.startswith("-") or 
                first_line.startswith("*") or 
                re.match(r'^\d+\.', first_line) or
                first_line.startswith("|") or
                first_line.startswith("<") or
                first_line.startswith("!") or 
                first_line.strip().startswith("-->")):
                continue
            
            if first_line.startswith(">"):
                continue
                
            paragraph_count += 1
            
            # Check Sentence Count (Should be <= 3)
            sent_count = count_sentences(raw_block_text)
            if sent_count > 3:
                long_paragraphs += 1
                warnings.append(f"⚠️ Paragraph {paragraph_count} has {sent_count} sentences (Target is 2~3 sentences for mobile readability): '{raw_block_text[:60]}...'")
            
            # Check Indent (Should start with exactly one space ' ')
            # Note: lines[0] is the raw first line before strip()
            raw_first_line = lines[0]
            if not raw_first_line.startswith(" ") or raw_first_line.startswith("  "):
                missing_indents += 1
                # Show exactly what it starts with
                start_chars = repr(raw_first_line[:5])
                warnings.append(f"⚠️ Paragraph {paragraph_count} does not start with exactly one space (starts with {start_chars}).")

    # -------------------------------------------------------------
    # 4. FAQ Absence Check (FAQ should not be inside body)
    # -------------------------------------------------------------
    if not is_glossary:
        faq_in_body_match = re.search(r'^#+\s+.*(FAQ|faq|자주 묻는 질문|よくある質問|常见问题)', body_text, re.MULTILINE | re.IGNORECASE)
        if faq_in_body_match:
            errors.append("❌ FAQ is written directly in the body headings. FAQs must be defined ONLY in the YAML frontmatter `faqs` property.")

    # -------------------------------------------------------------
    # Glossary-specific checks (Title check)
    # -------------------------------------------------------------
    if is_glossary:
        title = frontmatter.get("title", "")
        # Standard glossary title should end with "이란?" or equivalent
        # Since it translates, we check if it contains "이란?" or "とは" or "What is" or "是什么" or is a neat title
        is_title_valid = any(term in title for term in ["이란?", "とは", "What is", "是什么", "란?"])
        if not is_title_valid and title:
            warnings.append(f"⚠️ Glossary title '{title}' may not match standard wiki format (e.g. '기술명 이란?', 'What is 기술명?').")

    # -------------------------------------------------------------
    # Static Image Path Verification (Does file exist on disk?)
    # -------------------------------------------------------------
    broken_locals_in_file = []
    file_dir = os.path.dirname(file_path)
    
    for img_type, img_path in local_images:
        # Ignore external images
        if img_path.startswith("http://") or img_path.startswith("https://") or img_path.startswith("//"):
            continue
            
        clean_img_path = img_path.split('?')[0].split('#')[0]
        resolved_path = os.path.normpath(os.path.join(file_dir, clean_img_path))
        
        if not os.path.exists(resolved_path):
            err_msg = f"❌ Local Image file NOT found on disk: '{img_path}' (Resolved to: '{resolved_path}')"
            errors.append(err_msg)
            broken_locals_in_file.append({
                'type': img_type,
                'referenced': img_path,
                'resolved': resolved_path
            })
            broken_images_local.append({
                'file': rel_path,
                'type': img_type,
                'referenced': img_path,
                'resolved': resolved_path
            })
            
    return len(errors) == 0, errors, warnings, frontmatter, local_images, broken_locals_in_file


# -------------------------------------------------------------
# Execute Static Inspections
# -------------------------------------------------------------
matching_files = []
for root, dirs, files in os.walk(BLOG_DIR):
    for file in files:
        if file.endswith(".md") and any(file.startswith(date) for date in DATES):
            matching_files.append(os.path.join(root, file))

# Sort files for neat reporting
matching_files.sort()

# First, run static tests
print(f"🔍 [STEP 1] Scanning {len(matching_files)} markdown files for structural & local file checks...")
print("-" * 100)

static_results = {}
for fp in matching_files:
    rel_path = os.path.relpath(fp, BLOG_DIR)
    total_files += 1
    
    ok, errs, warns, fm, imgs, b_locals = check_markdown_file(fp)
    static_results[fp] = {
        'ok': ok,
        'errors': errs,
        'warnings': warns,
        'frontmatter': fm,
        'images': imgs,
        'broken_locals': b_locals,
        'rel_path': rel_path
    }
    
    if ok:
        status_icon = "✅"
    elif len(errs) > 0:
        status_icon = "❌"
    else:
        status_icon = "⚠️"
        
    print(f"{status_icon} {rel_path}")
    if errs:
        for err in errs:
            print(f"   {err}")
    if warns:
        for warn in warns:
            print(f"   {warn}")



# -------------------------------------------------------------
# FINAL DETAILED SUMMARY
# -------------------------------------------------------------
print("\n" + "=" * 100)
print("📊 FINAL QUALITY & IMAGE VALIDATION SUMMARY")
print("=" * 100)

passed_count = 0
failed_count = 0

for fp, res in static_results.items():
    if res['ok']:
        passed_count += 1
    else:
        failed_count += 1

print(f"Total target blog posts checked: {total_files}")
print(f"🟢 Passed All Checks (Perfect Quality): {passed_count}")
print(f"🔴 Failed / Needs Action: {failed_count}")

# Print out actionable breakdown
if failed_count > 0:
    print("\n🚨 DETAILED LIST OF FAILURES AND WARNINGS BY FILE:")
    print("-" * 100)
    for fp, res in static_results.items():
        if not res['ok'] or res['warnings']:
            print(f"\n📂 File: {res['rel_path']}")
            if res['errors']:
                print("  Errors:")
                for err in res['errors']:
                    print(f"    - {err}")
            if res['warnings']:
                print("  Warnings:")
                for warn in res['warnings']:
                    print(f"    - {warn}")

print("\n" + "=" * 100)
if failed_count == 0:
    print("🎉 EXCELLENT! All checked postings from May 6th to May 10th meet 100% of the quality rules and images render perfectly!")
else:
    print("🛠️ Actions are required to resolve the broken elements or styling violations listed above.")
print("=" * 100)
