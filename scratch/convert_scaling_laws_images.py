from PIL import Image
import os

# Source images generated
src1 = r"C:\Users\haionnet\.gemini\antigravity\brain\92729822-5571-4c6f-a774-123c7aa0ca70\scaling_laws_crystals_1778463145493.png"
src2 = r"C:\Users\haionnet\.gemini\antigravity\brain\92729822-5571-4c6f-a774-123c7aa0ca70\scaling_laws_collision_1778463162503.png"
src3 = r"C:\Users\haionnet\.gemini\antigravity\brain\92729822-5571-4c6f-a774-123c7aa0ca70\scaling_laws_waves_1778463179495.png"

# Destination paths
dest_dir = r"c:\Users\haionnet\Desktop\editornom\source\posts\Scaling_Laws"
dest1 = os.path.join(dest_dir, "3e3a47da-0.webp")
dest2 = os.path.join(dest_dir, "4a8f94d2-1.webp")
dest3 = os.path.join(dest_dir, "5eb89cf2-2.webp")

def convert_to_webp(src, dest):
    print(f"Converting {src} to {dest}...")
    try:
        im = Image.open(src)
        # Ensure destination directory exists
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        im.save(dest, "WEBP", quality=90)
        print("Success!")
    except Exception as e:
        print(f"Error: {e}")

convert_to_webp(src1, dest1)
convert_to_webp(src2, dest2)
convert_to_webp(src3, dest3)
