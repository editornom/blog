import os

files = [
    "src/data/blog/cn/posts/anthropic-leaks-analysis-claude-code-mythos-insight.md",
    "src/data/blog/en/posts/anthropic-leaks-analysis-claude-code-mythos-insight.md",
    "src/data/blog/jp/posts/anthropic-leaks-analysis-claude-code-mythos-insight.md",
    "src/data/blog/ko/posts/anthropic-leaks-analysis-claude-code-mythos-insight.md"
]

for file_path in files:
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        # Replace the old path with the correct 4-level deep path
        new_content = content.replace("../../assets/images/", "../../../../assets/images/")
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"Fixed image paths in: {file_path}")
    else:
        print(f"File not found: {file_path}")

print("\nDone fixing recent post image paths.")
