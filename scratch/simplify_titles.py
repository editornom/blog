import sys
sys.stdout.reconfigure(encoding='utf-8')
import os
import glob
import re
from google import genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

base_dir = "src/data/blog"
ko_glossary_dir = os.path.join(base_dir, 'ko', 'glossary')

def simplify_title(old_title):
    prompt = f"""
?ㅼ쓬? ?뚰겕 釉붾줈洹??⑹뼱 ?ъ쟾(Glossary)??湲곗〈 ?쒕ぉ?낅땲??
湲곗〈 ?쒕ぉ: "{old_title}"

???쒕ぉ?먯꽌 嫄곗갹???ㅻ챸?대굹 遺?쒕? 紐⑤몢 吏?곌퀬, ?듭떖 ?⑹뼱留?戮묒븘??"?듭떖?⑹뼱??" ?먮뒗 "?듭떖?⑹뼱? 臾댁뾿?멸??" ?뺥깭??媛???⑥닚??臾몄옄???섎굹留?諛섑솚?섏꽭??
?덉떆:
"eBPF: 由щ늼??而ㅻ꼸???좎뿰?깃낵 ?덉쟾?깆쓣 洹밸??뷀븯???뚮뱶諛뺤뒪 湲곗닠" -> "eBPF??"
"SBOM (?뚰봽?몄썾???먯옱紐낆꽭?? ?뺤쓽? 蹂댁븞 愿由ъ뿉?쒖쓽 ??븷" -> "SBOM?대??"

?곗샂???놁씠 ?쒕ぉ留?異쒕젰?섏꽭??
"""
    try:
        response = client.models.generate_content(
            model='models/gemini-3-flash-preview', 
            contents=prompt
        )
        return response.text.strip().replace('"', '').replace("'", "")
    except Exception as e:
        print(f"Error calling Gemini: {e}")
        return old_title

def translate_title(ko_title, lang):
    if lang == 'en':
        prompt = f"Translate this short Korean title to English, keeping it simple. Example: 'eBPF??' -> 'What is eBPF?'. Title: '{ko_title}'. Output only the translation without quotes."
    elif lang == 'jp':
        prompt = f"Translate this short Korean title to Japanese, keeping it simple. Example: 'eBPF??' -> 'eBPF?ⓦ겘竊?. Title: '{ko_title}'. Output only the translation without quotes."
    elif lang == 'cn':
        prompt = f"Translate this short Korean title to Simplified Chinese, keeping it simple. Example: 'eBPF??' -> '餓阿덃삸 eBPF竊?. Title: '{ko_title}'. Output only the translation without quotes."
    else:
        return ko_title
        
    try:
        response = client.models.generate_content(
            model='models/gemini-3-flash-preview', 
            contents=prompt
        )
        return response.text.strip().replace('"', '').replace("'", "")
    except Exception as e:
        print(f"Error translating title: {e}")
        return ko_title

for filepath in glob.glob(os.path.join(ko_glossary_dir, "*.md")):
    filename = os.path.basename(filepath)
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    match = re.search(r'title:\s*(.+)', content)
    if not match:
        continue
        
    old_title = match.group(1).strip()
    # Remove quotes if present
    if old_title.startswith('"') and old_title.endswith('"'):
        old_title = old_title[1:-1]
        
    if "?대?" in old_title or "臾댁뾿?멸?" in old_title:
        # Already simple? Let's check length just in case
        if len(old_title) < 15:
            continue
            
    print(f"Simplifying: {old_title}")
    new_ko_title = simplify_title(old_title)
    print(f"  -> {new_ko_title}")
    
    # Apply to all languages
    for lang in ['ko', 'en', 'jp', 'cn']:
        lang_filepath = os.path.join(base_dir, lang, 'glossary', filename)
        if not os.path.exists(lang_filepath):
            continue
            
        with open(lang_filepath, 'r', encoding='utf-8') as f:
            lang_content = f.read()
            
        if lang == 'ko':
            new_title = new_ko_title
        else:
            new_title = translate_title(new_ko_title, lang)
            
        # Update title in frontmatter
        lang_content = re.sub(r'title:\s*.*', f'title: "{new_title}"', lang_content)
        
        # We also need to update the H1 in the content if there is one? 
        # No, generator doesn't put an H1, the site uses the title from frontmatter.
        # But wait, in generator.py it says: 1. ?쒕ぉ: "{primary_topic}?대??" (???쒕ぉ ?몄뿉 ?ㅻⅨ ??쒕ぉ? ?ъ슜?섏? 留덉꽭??)
        # Usually it puts `# {Title}` at the top of the body. Let's replace the first # heading if it matches the old title closely.
        # It's safer just to update the frontmatter since Astro uses the frontmatter title.
        
        with open(lang_filepath, 'w', encoding='utf-8') as f:
            f.write(lang_content)
            
        print(f"  [{lang}] Updated to: {new_title}")

