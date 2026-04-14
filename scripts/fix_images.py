import os
import re
import uuid
import time
from imagen_helper import generate_image

def fix_images_in_latest_post():
    blog_dir = os.path.join("src", "data", "blog")
    posts = [f for f in os.listdir(blog_dir) if f.endswith(".md")]
    if not posts:
        print("No posts found.")
        return
        
    # Get the newest file
    latest_post = max([os.path.join(blog_dir, f) for f in posts], key=os.path.getmtime)
    print(f"Fixing images for {latest_post}")
    
    with open(latest_post, "r", encoding="utf-8") as f:
        content = f.read()
        
    placeholders = re.findall(r'\[이미지: (.*?)\]', content)
    print(f"Found {len(placeholders)} placeholders.")
    
    for i, prompt in enumerate(placeholders):
        img_uuid = str(uuid.uuid4())[:8]
        img_filename = f"post-img-{img_uuid}-{i}.png"
        img_path = os.path.join("src", "assets", "images", img_filename)
        
        print(f"Generating AI image for: {prompt[:50]}...")
        generated_path = generate_image(prompt, img_path)
        
        # Note: Rate limiting is now handled internally by imagen_helper via TokenBucket.
        
        if generated_path:
            md_img_link = f"![AI Generated Image](../../assets/images/{img_filename})"
            content = content.replace(f"[이미지: {prompt}]", md_img_link)
            
            # Update ogImage if it's the first one
            if i == 0:
                content = re.sub(r'ogImage: ".*?"', f'ogImage: "../../assets/images/{img_filename}"', content)
    
    with open(latest_post, "w", encoding="utf-8") as f:
        f.write(content)
    print("Done fixing images!")

if __name__ == "__main__":
    fix_images_in_latest_post()
