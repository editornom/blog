import yaml
import os

files = [
    ".github/workflows/auto-09-tech-news.yml",
    ".github/workflows/auto-12-tech-feature.yml",
    ".github/workflows/auto-15-ai-news.yml",
    ".github/workflows/auto-18-ai-feature.yml"
]

for f in files:
    if os.path.exists(f):
        try:
            with open(f, 'r', encoding='utf-8') as fh:
                yaml.safe_load(fh)
            print(f"{f}: OK")
        except Exception as e:
            print(f"{f}: ERROR - {e}")
    else:
        print(f"{f}: NOT FOUND")
