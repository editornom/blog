from PIL import Image
import os

# Source images generated
src1 = r"C:\Users\haionnet\.gemini\antigravity\brain\92729822-5571-4c6f-a774-123c7aa0ca70\mcp_connectivity_1778463079131.png"
src2 = r"C:\Users\haionnet\.gemini\antigravity\brain\92729822-5571-4c6f-a774-123c7aa0ca70\asymmetric_key_1778463097419.png"

# Destination paths
dest1 = r"c:\Users\haionnet\Desktop\editornom\source\posts\Model_Context_Protocol\593d2810-0.webp"
dest2 = r"c:\Users\haionnet\Desktop\editornom\source\posts\Asymmetric_Cryptography\95b12afe-0.webp"

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
