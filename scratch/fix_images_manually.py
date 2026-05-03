import os
import re
import uuid
import sys
from dotenv import load_dotenv

# Add scripts folder to path to import helpers
sys.path.append(os.path.join(os.getcwd(), 'scripts'))
from imagen_helper import generate_image
from translator import translate_text

load_dotenv()

def fix_missing_images(target_files, keyword, source_folder):
    for post_path in target_files:
        if not os.path.exists(post_path):
            print(f"File not found: {post_path}")
            continue
            
        print(f"Processing {post_path}...")
        with open(post_path, "r", encoding="utf-8") as f:
            draft = f.read()
            
        # Detect ![Description] or [이미지: Description]
        image_placeholders = re.findall(r'(?:!\[|\[이미지:\s*)(.*?)(?:\)|\])', draft)
        
        if not image_placeholders:
            print("No image placeholders found.")
            continue
            
        print(f"Found {len(image_placeholders)} potential images to generate.")
        
        folder = "posts"
        source_img_dir = os.path.join("source", folder, source_folder)
        os.makedirs(source_img_dir, exist_ok=True)
        
        for i, prompt in enumerate(image_placeholders):
            # Skip if already a path
            if prompt.startswith('/') or 'source/' in prompt or 'http' in prompt or prompt.endswith('.webp'):
                continue
                
            img_uuid = str(uuid.uuid4())[:8]
            img_filename = f"{img_uuid}-{i}.webp"
            img_path = os.path.join(source_img_dir, img_filename)
            
            print(f"Generating AI image for: {prompt[:50]}...")
            generated_path, img_error = generate_image(prompt, img_path, context=f"Topic: {keyword}")
            
            if generated_path:
                rel_path = f"../../../../../source/{folder}/{source_folder}/{img_uuid}-{i}.webp"
                # Encode parens
                encoded_rel_path = rel_path.replace('(', '%28').replace(')', '%29')
                
                alt_clean_prompt = f"다음 이미지 생성용 프롬프트에서 시각적 스타일 키워드를 제외하고 요약해서 ko로 번역해줘:\n{prompt}"
                translated_alt = translate_text(alt_clean_prompt, "ko")
                
                md_img_link = f"![{translated_alt}]({encoded_rel_path})"
                
                # Replace the original tag
                draft = draft.replace(f"![{prompt}]", md_img_link)
                draft = draft.replace(f"[이미지: {prompt}]", md_img_link)
                
                if i == 0:
                    # Set first image as ogImage
                    draft = re.sub(r'ogImage:.*', f'ogImage: "{rel_path}"', draft)
            else:
                print(f"Error generating image: {img_error}")
                
        with open(post_path, "w", encoding="utf-8") as f:
            f.write(draft)
        
        print(f"Successfully updated {post_path}")

if __name__ == "__main__":
    # Fix Agentic Cybersecurity post (corrected filename)
    fix_missing_images(
        ["src/data/blog/ko/posts/260427_agentic-cybersecurity-autonomous-defense.md"], 
        "Agentic_Cybersecurity", 
        "에이전틱_사이버_보안_(Agentic_Cybersecurity)"
    )
