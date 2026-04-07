from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

LANGUAGES = {
    "en": "English",
    "cn": "Simplified Chinese (简体中文)",
    "jp": "Japanese (日本語)",
}

def translate_post(korean_markdown, target_lang):
    """
    Translates a Korean blog post markdown into the target language using Gemini.
    Preserves frontmatter structure and markdown formatting.
    
    Args:
        korean_markdown: The full markdown content (with frontmatter) in Korean.
        target_lang: Language code ('en', 'cn', 'jp').
    
    Returns:
        Translated markdown string, or None on failure.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY not found in .env")
        return None

    lang_name = LANGUAGES.get(target_lang, target_lang)
    client = genai.Client(api_key=api_key)

    prompt = f"""
당신은 전문 기술 번역가입니다. 아래의 한국어 블로그 원고를 {lang_name}로 번역하십시오.

### 번역 규칙:
1. **Frontmatter 유지**: YAML frontmatter(--- 사이의 영역)의 구조는 그대로 유지하되, title과 description만 번역하십시오.
2. **slug 유지**: slug 값은 절대 변경하지 마십시오.
3. **이미지 경로 유지**: 이미지 경로(../../../../assets/images/...)는 절대 변경하지 마십시오.
4. **마크다운 문법 유지**: 헤더(#, ##, ###), 볼드(**), 리스트(-), 인용(>), 코드블록(```) 등 마크다운 문법을 그대로 유지하십시오.
5. **자연스러운 번역**: 직역이 아닌, {lang_name} 원어민이 읽었을 때 자연스럽고 전문적인 기술 칼럼처럼 느껴지도록 의역하십시오.
6. **기술 용어**: 프로토콜명, 기술 약어 등은 원문 그대로 사용하십시오. (예: VPN, UTM, API, SSL 등)
7. **이미지 알트태그 번역**: `![alt text](path)` 형식에서 `alt text` 부분을 대상 언어로 자연스럽게 번역하십시오.

### 원본 한국어 원고:
{korean_markdown}

### ⚠️ 주의사항:
- 오직 번역된 마크다운만 출력하십시오.
- 메타 설명, 코멘트, 번역 과정 설명 등은 일절 출력하지 마십시오.
- 마크다운 코드 펜스(```markdown 등)로 감싸지 마십시오.
"""

    try:
        response = client.models.generate_content(
            model='models/gemini-3-flash-preview',
            contents=prompt
        )
        return response.text
    except Exception as e:
        print(f"Error translating to {lang_name}: {e}")
        return None

def translate_text(text, target_lang):
    """
    Translates a short piece of text into the target language.
    Useful for alt tags or short phrases.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return text

    lang_name = LANGUAGES.get(target_lang, target_lang)
    client = genai.Client(api_key=api_key)

    prompt = f"Translate the following text into {lang_name}. Output only the translated text, nothing else:\n\n{text}"

    try:
        response = client.models.generate_content(
            model='models/gemini-3-flash-preview',
            contents=prompt
        )
        return response.text.strip()
    except Exception as e:
        print(f"Error translating text to {lang_name}: {e}")
        return text


def translate_and_save(korean_draft, slug, folder, target_langs=None):
    """
    Translates the Korean draft into EN, CN, JP and saves each to the correct folder.
    
    Args:
        target_langs: Optional list of language codes to filter (e.g. ['en']).
    
    Returns:
        Dictionary of { 'lang_code': {'success': bool, 'path': str or None, 'error': str or None} }
    """
    results = {}
    
    for lang_code, lang_name in LANGUAGES.items():
        if target_langs and lang_code not in target_langs:
            continue
            
        try:
            try:
                print(f"\n--- Translating to {lang_name} ({lang_code}) ---")
            except UnicodeEncodeError:
                print(f"\n--- Translating to {lang_code} ---")
            
            max_retries = 1
            translated = None
            
            for attempt in range(max_retries + 1):
                try:
                    translated = translate_post(korean_draft, lang_code)
                    if translated:
                        break
                except Exception as e:
                    import time
                    if "503" in str(e) and attempt < max_retries:
                        print(f"  [WAIT] 503 Unavailable, retrying in 10s... (Attempt {attempt+1}/{max_retries})")
                        time.sleep(10)
                        continue
                    else:
                        raise e

            if not translated:
                print(f"  [FAIL] Failed to translate to {lang_name}")
                results[lang_code] = {"success": False, "path": None, "error": "Empty response or translation failed"}
                continue
            
            # Clean potential markdown code fence wrapping
            if translated.strip().startswith("```"):
                lines = translated.strip().split("\n")
                if lines[0].strip().startswith("```"):
                    lines = lines[1:]
                if lines and lines[-1].strip() == "```":
                    lines = lines[:-1]
                translated = "\n".join(lines).strip()
            
            # Save to the correct language folder
            target_dir = os.path.join("src", "data", "blog", lang_code, folder)
            os.makedirs(target_dir, exist_ok=True)
            target_path = os.path.join(target_dir, f"{slug}.md")
            
            with open(target_path, "w", encoding="utf-8") as f:
                f.write(translated)
            
            print(f"  [PASS] Saved to {target_path}")
            results[lang_code] = {"success": True, "path": target_path, "error": None}
            
        except Exception as e:
            print(f"  [FAIL] Error translating to {lang_name}: {e}")
            results[lang_code] = {"success": False, "path": None, "error": str(e)}
    
    return results


if __name__ == "__main__":
    # Test with a sample file
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python translator.py <korean_markdown_file>")
        sys.exit(1)
    
    filepath = sys.argv[1]
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    slug = os.path.splitext(os.path.basename(filepath))[0]
    folder = "posts"  # default
    
    translate_and_save(content, slug, folder)
