import sys
sys.stdout.reconfigure(encoding='utf-8')

import os
import re
import glob
import yaml

base_dir = "src/data/blog"
langs = ['ko', 'en', 'jp', 'cn']
folders = ['posts', 'glossary']
issues = []

def add_issue(severity, filepath, message):
    issues.append((severity, filepath, message))

# 1. Check for double-prefixed filenames (e.g. 260428_260428_...)
print("=== 1. Double-prefix filename check ===")
for lang in langs:
    for folder in folders:
        d = os.path.join(base_dir, lang, folder)
        if not os.path.exists(d):
            continue
        for f in os.listdir(d):
            if re.match(r'^\d{6}_\d{6}_', f):
                add_issue("CRITICAL", os.path.join(d, f), f"Double-prefixed filename: {f}")

# 2. Frontmatter validation
print("=== 2. Frontmatter validation ===")
for lang in langs:
    for folder in folders:
        d = os.path.join(base_dir, lang, folder)
        if not os.path.exists(d):
            continue
        for f in sorted(os.listdir(d)):
            if not f.endswith('.md'):
                continue
            filepath = os.path.join(d, f)
            with open(filepath, 'r', encoding='utf-8') as fh:
                content = fh.read()
            
            if not content.startswith('---'):
                add_issue("CRITICAL", filepath, "Missing frontmatter (no --- at start)")
                continue
            
            parts = content.split('---', 2)
            if len(parts) < 3:
                add_issue("CRITICAL", filepath, "Malformed frontmatter (can't split by ---)")
                continue
            
            try:
                fm = yaml.safe_load(parts[1])
            except Exception as e:
                add_issue("CRITICAL", filepath, f"YAML parse error: {e}")
                continue
            
            if not fm:
                add_issue("CRITICAL", filepath, "Empty frontmatter")
                continue
            
            # Required fields
            for field in ['title', 'slug', 'pubDatetime']:
                if field not in fm or not fm[field]:
                    add_issue("CRITICAL", filepath, f"Missing required field: {field}")
            
            # Check draft status
            if fm.get('draft', False):
                add_issue("WARNING", filepath, "Post is set to draft: true")
            
            # Check ogImage exists
            og = fm.get('ogImage', '')
            if og and 'placeholder' not in str(og):
                # Resolve relative path
                og_path = os.path.normpath(os.path.join(os.path.dirname(filepath), str(og)))
                if not os.path.exists(og_path):
                    add_issue("WARNING", filepath, f"ogImage file not found: {og}")

            # Body checks
            body = parts[2]
            
            # Check for broken image tags (!![)
            if '!![' in body:
                add_issue("ERROR", filepath, "Broken image tag: !![...")
            
            # Check for unclosed code blocks
            if body.count('```') % 2 != 0:
                add_issue("ERROR", filepath, "Unclosed code block (odd number of ```)")
            
            # Check for <script> tags in body
            if '<script' in body.lower():
                add_issue("ERROR", filepath, "Contains <script> tag in body")
            
            # Check for broken markdown images (no closing paren)
            broken_imgs = re.findall(r'!\[.*?\]\([^)]*$', body, re.MULTILINE)
            if broken_imgs:
                add_issue("ERROR", filepath, f"Broken image markdown (unclosed parenthesis)")
            
            # Check image paths exist
            img_matches = re.findall(r'!\[.*?\]\((.*?)\)', body)
            for img_path in img_matches:
                if img_path.startswith('http'):
                    continue
                resolved = os.path.normpath(os.path.join(os.path.dirname(filepath), img_path))
                if not os.path.exists(resolved):
                    add_issue("WARNING", filepath, f"Image not found: {img_path}")

# 3. Cross-language consistency check
print("=== 3. Cross-language consistency check ===")
for folder in folders:
    ko_dir = os.path.join(base_dir, 'ko', folder)
    if not os.path.exists(ko_dir):
        continue
    ko_files = set(f for f in os.listdir(ko_dir) if f.endswith('.md'))
    
    for lang in ['en', 'jp', 'cn']:
        lang_dir = os.path.join(base_dir, lang, folder)
        if not os.path.exists(lang_dir):
            add_issue("ERROR", lang_dir, f"Directory missing entirely")
            continue
        lang_files = set(f for f in os.listdir(lang_dir) if f.endswith('.md'))
        
        # Files in ko but not in other lang
        missing = ko_files - lang_files
        for m in missing:
            add_issue("ERROR", os.path.join(lang_dir, m), f"Missing translation (exists in ko but not in {lang})")
        
        # Files in other lang but not in ko (orphans)
        orphans = lang_files - ko_files
        for o in orphans:
            add_issue("WARNING", os.path.join(lang_dir, o), f"Orphan file (exists in {lang} but not in ko)")

# 4. Glossary link integrity
print("=== 4. Glossary link integrity ===")
# Collect all glossary slugs
glossary_slugs = set()
ko_glossary_dir = os.path.join(base_dir, 'ko', 'glossary')
if os.path.exists(ko_glossary_dir):
    for f in os.listdir(ko_glossary_dir):
        if not f.endswith('.md'):
            continue
        fp = os.path.join(ko_glossary_dir, f)
        with open(fp, 'r', encoding='utf-8') as fh:
            content = fh.read()
        parts = content.split('---', 2)
        if len(parts) >= 3:
            try:
                fm = yaml.safe_load(parts[1])
                if fm and fm.get('slug'):
                    glossary_slugs.add(fm['slug'])
            except:
                pass

# Check glossary tooltip links in posts
for lang in langs:
    posts_dir = os.path.join(base_dir, lang, 'posts')
    if not os.path.exists(posts_dir):
        continue
    for f in os.listdir(posts_dir):
        if not f.endswith('.md'):
            continue
        fp = os.path.join(posts_dir, f)
        with open(fp, 'r', encoding='utf-8') as fh:
            content = fh.read()
        # Find glossary links
        links = re.findall(r'href="/' + lang + r'/glossary/([^"]+)"', content)
        for link_slug in links:
            if link_slug not in glossary_slugs:
                add_issue("WARNING", fp, f"Glossary link points to non-existent slug: {link_slug}")

# 5. Date consistency check across languages
print("=== 5. Date consistency check ===")
for folder in folders:
    ko_dir = os.path.join(base_dir, 'ko', folder)
    if not os.path.exists(ko_dir):
        continue
    for f in os.listdir(ko_dir):
        if not f.endswith('.md'):
            continue
        ko_fp = os.path.join(ko_dir, f)
        with open(ko_fp, 'r', encoding='utf-8') as fh:
            ko_content = fh.read()
        ko_date_match = re.search(r'pubDatetime:\s*(.+)', ko_content)
        if not ko_date_match:
            continue
        ko_date = ko_date_match.group(1).strip()
        
        for lang in ['en', 'jp', 'cn']:
            lang_fp = os.path.join(base_dir, lang, folder, f)
            if not os.path.exists(lang_fp):
                continue
            with open(lang_fp, 'r', encoding='utf-8') as fh:
                lang_content = fh.read()
            lang_date_match = re.search(r'pubDatetime:\s*(.+)', lang_content)
            if lang_date_match:
                lang_date = lang_date_match.group(1).strip()
                if ko_date != lang_date:
                    add_issue("ERROR", lang_fp, f"pubDatetime mismatch: ko={ko_date} vs {lang}={lang_date}")

# === REPORT ===
print("\n" + "="*60)
print("📋 AUDIT REPORT")
print("="*60)

criticals = [i for i in issues if i[0] == "CRITICAL"]
errors = [i for i in issues if i[0] == "ERROR"]
warnings = [i for i in issues if i[0] == "WARNING"]

print(f"\n🔴 CRITICAL: {len(criticals)}")
for sev, fp, msg in criticals:
    print(f"  [{sev}] {fp}")
    print(f"         → {msg}")

print(f"\n🟠 ERROR: {len(errors)}")
for sev, fp, msg in errors:
    print(f"  [{sev}] {fp}")
    print(f"         → {msg}")

print(f"\n🟡 WARNING: {len(warnings)}")
for sev, fp, msg in warnings:
    print(f"  [{sev}] {fp}")
    print(f"         → {msg}")

print(f"\n{'='*60}")
print(f"Total issues: {len(issues)} (CRITICAL: {len(criticals)}, ERROR: {len(errors)}, WARNING: {len(warnings)})")
print("="*60)
