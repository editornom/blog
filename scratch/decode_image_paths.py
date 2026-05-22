import os
import glob

def decode_image_paths():
    # Recursively find all markdown files in src/data/blog
    md_files = glob.glob("src/data/blog/**/*.md", recursive=True)
    count = 0
    
    for file_path in md_files:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        # We can perform a safe decoding of %28 and %29 in the file
        if "%28" in content or "%29" in content:
            new_content = content.replace("%28", "(").replace("%29", ")")
            
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"Decoded paths in {file_path}")
            count += 1
            
    print(f"Successfully decoded paths in {count} files.")

if __name__ == "__main__":
    decode_image_paths()
