import sys
sys.stdout.reconfigure(encoding='utf-8')
import os
import glob
import re

base_dir = "src/data/blog"
langs = ['ko', 'en', 'jp', 'cn']
folders = ['posts', 'glossary']
fixed_count = 0

# 1. Fix BOM in all .md files
print("=== Fixing BOM (Byte Order Mark) ===")
for lang in langs:
    for folder in folders:
        d = os.path.join(base_dir, lang, folder)
        if not os.path.exists(d):
            continue
        for f in os.listdir(d):
            if not f.endswith('.md'):
                continue
            fp = os.path.join(d, f)
            with open(fp, 'rb') as fh:
                raw = fh.read()
            if raw.startswith(b'\xef\xbb\xbf'):
                raw = raw[3:]  # Remove BOM
                with open(fp, 'wb') as fh:
                    fh.write(raw)
                print(f"  [FIX] Removed BOM from {fp}")
                fixed_count += 1

# 2. Fix broken image paths (parentheses in path cause regex to cut off)
print("\n=== Fixing image path issues ===")
# The audit showed image paths get cut off at parentheses.
# Let's check what's actually in source/posts
source_posts = os.path.join("source", "posts")
if os.path.exists(source_posts):
    actual_dirs = os.listdir(source_posts)
    print(f"  Source post dirs: {actual_dirs}")

# Check a sample to understand the image path issue
sample_files = [
    "src/data/blog/ko/posts/260425_mcp-ai-integration-standard-protocol.md",
    "src/data/blog/ko/posts/260425_single-token-native-multimodal-ai.md",
    "src/data/blog/ko/posts/260426_ebpf-observability-ideals-reality.md",
    "src/data/blog/ko/posts/260427_attention-transformers-tech-landscape.md",
]
for sf in sample_files:
    if os.path.exists(sf):
        with open(sf, 'r', encoding='utf-8') as fh:
            content = fh.read()
        # Find all image references
        imgs = re.findall(r'!\[.*?\]\((.*?)\)', content)
        for img in imgs:
            resolved = os.path.normpath(os.path.join(os.path.dirname(sf), img))
            exists = os.path.exists(resolved)
            if not exists:
                print(f"  [MISSING] {sf}")
                print(f"           Path: {img}")
                print(f"           Resolved: {resolved}")
                # Try to find the actual directory by checking partial match
                parent_dir = os.path.dirname(resolved)
                grandparent = os.path.dirname(parent_dir)
                target_basename = os.path.basename(resolved)
                if os.path.exists(grandparent):
                    for d in os.listdir(grandparent):
                        possible = os.path.join(grandparent, d, target_basename)
                        if os.path.exists(possible):
                            print(f"           FOUND at: {possible}")

# 3. Fix pubDatetime mismatches (these were caught as 0 errors, so skip)

print(f"\n=== Summary ===")
print(f"Fixed {fixed_count} BOM issues")
