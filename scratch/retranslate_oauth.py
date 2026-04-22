import os
import sys

# Add scripts directory to path
sys.path.append(os.path.abspath("scripts"))

from translator import translate_and_save

file_path = r"src\data\blog\ko\posts\260422_oauth-supply-chain-security-risks-lessons.md"
slug = "oauth-supply-chain-security-risks-lessons"
folder = "posts"

with open(file_path, "r", encoding="utf-8") as f:
    draft = f.read()

print(f"Re-translating {slug} to all languages...")
translate_and_save(draft, slug, folder)

print("Translation sync complete.")
