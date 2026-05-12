import os

files = [
    r"c:\Users\haionnet\Desktop\editornom\src\data\blog\ko\posts\260509_scaling-laws-agi-mirage.md",
    r"c:\Users\haionnet\Desktop\editornom\src\data\blog\en\posts\260509_scaling-laws-agi-mirage.md",
    r"c:\Users\haionnet\Desktop\editornom\src\data\blog\jp\posts\260509_scaling-laws-agi-mirage.md",
    r"c:\Users\haionnet\Desktop\editornom\src\data\blog\cn\posts\260509_scaling-laws-agi-mirage.md"
]

substitutions = [
    "../../../../../source/posts/Scaling_Laws/3e3a47da-0.webp", # ogImage
    "../../../../../source/posts/Scaling_Laws/3e3a47da-0.webp", # inline 1
    "../../../../../source/posts/Scaling_Laws/4a8f94d2-1.webp", # inline 2
    "../../../../../source/posts/Scaling_Laws/5eb89cf2-2.webp"  # inline 3
]

for filepath in files:
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        continue
    
    print(f"Updating placeholders in {os.path.basename(filepath)}...")
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    # We want to replace each occurrence of "placeholder.png" sequentially with the corresponding substitution
    parts = content.split("../../../../assets/images/placeholder.png")
    if len(parts) != 5:
        print(f"Warning: Unexpected number of placeholders in {os.path.basename(filepath)}: found {len(parts)-1} instead of 4")
        # Let's try alternative prefix (e.g. maybe 4 directories back or something, check grep output: it says '../../../../assets/images/placeholder.png')
        continue
        
    new_content = ""
    for i in range(4):
        new_content += parts[i] + substitutions[i]
    new_content += parts[4]
    
    with open(filepath, "w", encoding="utf-8", newline="\n") as f:
        f.write(new_content)
    print("Successfully updated!")
