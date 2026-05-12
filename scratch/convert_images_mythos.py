import os
import shutil
from PIL import Image

src_img1 = r"C:\Users\haionnet\.gemini\antigravity\brain\56ab5df4-38fb-47f3-b2be-f96641a1c476\mythos_evaluation_main_1778552736452.png"
src_img2 = r"C:\Users\haionnet\.gemini\antigravity\brain\56ab5df4-38fb-47f3-b2be-f96641a1c476\agentic_cybersecurity_1778552754493.png"

dest_dir = r"c:\Users\haionnet\Desktop\editornom\source\posts\metr_claude_mythos"
os.makedirs(dest_dir, exist_ok=True)

dest_img1 = os.path.join(dest_dir, "og-image.webp")
dest_img2 = os.path.join(dest_dir, "agentic-ai-cybersecurity.webp")

def convert_to_webp(src, dest):
    try:
        im = Image.open(src)
        im.save(dest, "WEBP", quality=85)
        print(f"Successfully converted and saved: {dest}")
    except Exception as e:
        print(f"Failed to convert ({e}). Copying directly.")
        shutil.copy2(src, dest.replace(".webp", ".png"))

convert_to_webp(src_img1, dest_img1)
convert_to_webp(src_img2, dest_img2)
