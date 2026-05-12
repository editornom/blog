import os

def inspect_full_file(path):
    print(f"=== {path} ===")
    if not os.path.exists(path):
        print("File does not exist.")
        return
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    parts = content.split('---', 2)
    if len(parts) < 3:
        print("Invalid frontmatter structure.")
        return
        
    body = parts[2]
    print("Body length:", len(body))
    print("Actual newline count (\\n):", body.count('\n'))
    print("Literal newline count (\\\\n):", body.count('\\n'))
    print("First 1000 characters of body:")
    print(body[:1000])

inspect_full_file('src/data/blog/ko/posts/260511_agentops-autonomy-or-black-box.md')
inspect_full_file('src/data/blog/ko/posts/260511_ebpf-linux-kernel-semantic-gap.md')
inspect_full_file('src/data/blog/ko/posts/260511_mysql-lts-innovation-vs-control.md')
