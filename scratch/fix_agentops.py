with open('src/data/blog/ko/posts/260511_agentops-autonomy-or-black-box.md', 'r', encoding='utf-8') as f:
    content = f.read()

parts = content.split('---', 2)
if len(parts) >= 3:
    body = parts[2]
    print("Before fix - body length:", len(body))
    print("Before fix - actual newlines:", body.count('\n'))
    print("Before fix - literal newlines:", body.count('\\n'))
    
    fixed_body = body.replace('\\n', '\n')
    print("After fix - body length:", len(fixed_body))
    print("After fix - actual newlines:", fixed_body.count('\n'))
    print("After fix - literal newlines:", fixed_body.count('\\n'))
    
    with open('src/data/blog/ko/posts/260511_agentops-autonomy-or-black-box.md', 'w', encoding='utf-8') as f:
        f.write(parts[0] + '---' + parts[1] + '---' + fixed_body)
    print("Saved fix to file!")
else:
    print("Frontmatter split failed!")
