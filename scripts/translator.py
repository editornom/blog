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
1. **Frontmatter 유지**: YAML frontmatter(--- 사이의 영역)의 구조는 그대로 유지하되, title, description, 그리고 faqs(배열 내의 q와 a) 항목을 각 언어에 맞게 번역하십시오.
   - 🚨 **[중요]**: 번역된 title과 description의 값은 반드시 큰따옴표(" ")로 감싸야 하며, 문자열 내부에는 절대 큰따옴표나 줄바꿈을 넣지 마십시오. (필요시 홑따옴표 사용)
   - 🚨 **[FAQ 번역]**: faqs 배열 내부의 각 객체에서 `q`와 `a`의 모든 텍스트를 대상 언어의 뉘앙스에 맞게 자연스럽게 번역하십시오. YAML 문법(하이픈 `-` 및 들여쓰기)을 엄수하십시오.
2. **Slug 현지화 (SEO 최적화)**: slug 값은 기존 영어 slug를 복사하지 마세요. 번역된 {lang_name} 원문에서의 핵심 키워드를 기반으로 해당 국가의 SEO에 가장 유리한 형태의 영문 단어 조합(소문자와 하이픈만 사용, 알파벳 표기 또는 직관적 의미역)으로 완전히 새롭게 창작하여 부여하십시오.
3. **이미지 경로 유지**: 이미지 경로(../../../../assets/images/... 또는 ../../../../../source/...)는 절대 변경하지 마십시오. UUID가 포함된 경로는 오타처럼 보여도 절대로 수정해서는 안 됩니다.
4. **마크다운 문법 유지**: 헤더(#, ##, ###), 볼드(**), 리스트(-), 인용(>), 코드블록(```) 등 마크다운 문법을 그대로 유지하십시오.
   - 🚨 **[Glossary 표 번역 주의]**: 원문 표에 있는 `| **한글명** | ... |` 등의 항목은 다른 국가의 독자에게 불필요하므로, 표 번역 시 해당 행(Row)은 아예 삭제하십시오.
   - 🚨 **[배열 기호 엄수]**: tags 항목의 대괄호 [ ] 안의 항목들을 구분할 때는 반드시 영문 반각 쉼표(,)만 사용하십시오. 절대 중국어/일본어 전각 쉼표(， 또는 、)를 쓰지 마십시오.
5. **자연스러운 번역**: 직역이 아닌, {lang_name} 원어민이 읽었을 때 자연스럽고 전문적인 기술 칼럼처럼 느껴지도록 의역하십시오.
6. **고유명사 보호 (Glossary Enforcement)**: 다음 목록의 브랜드명과 IT 솔루션 전문 용어들은 엉뚱한 현지어로 직역하지 말고 반드시 영문 스펠링을 그대로 유지하거나 업계 표준 표기를 가장 우선시하십시오.
   - [보호 사전]: Haionnet(하이온넷), Editornom, VPN, UTM, API, SSL, B2B, AI, LLM, RAG, NVIDIA, CDN, SD-WAN, Playwright, Cloud, On-Premise, Node, React, Next.js
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
        # 에러를 무조건 None으로 반환하지 않고 호출자에게 던져서 재시도 로직이 작동하게 함
        raise e

def translate_text(text, target_lang):
    """
    Translates a short piece of text into the target language with retries.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return text

    lang_name = LANGUAGES.get(target_lang, target_lang)
    client = genai.Client(api_key=api_key)
    prompt = f"Translate the following text into {lang_name}. Output only the translated text, nothing else:\n\n{text}"

    max_retries = 3
    for attempt in range(max_retries + 1):
        try:
            response = client.models.generate_content(
                model='models/gemini-3-flash-preview',
                contents=prompt
            )
            return response.text.strip()
        except Exception as e:
            import time
            error_msg = str(e)
            if ("503" in error_msg or "429" in error_msg or "UNAVAILABLE" in error_msg) and attempt < max_retries:
                wait_time = (attempt + 1) * 5 # 짧은 텍스트는 좀 더 짧게 대기 (5s, 10s...)
                print(f"  [TEXT-RETRY] {lang_name} 번역 중 오류... {wait_time}초 후 재시도 ({attempt+1}/{max_retries})")
                time.sleep(wait_time)
                continue
            else:
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
            
            max_retries = 3
            translated = None
            
            for attempt in range(max_retries + 1):
                try:
                    translated = translate_post(korean_draft, lang_code)
                    if translated:
                        break
                    else:
                        print(f"  [RETRY] Translation returned empty, retrying... ({attempt+1}/{max_retries})")
                except Exception as e:
                    import time
                    error_msg = str(e)
                    # 503(High Demand) 또는 429(Rate Limit) 등의 일시적 오류인 경우 재시도
                    if ("503" in error_msg or "429" in error_msg or "UNAVAILABLE" in error_msg) and attempt < max_retries:
                        wait_time = (attempt + 1) * 15 # 15s, 30s, 45s...
                        print(f"  [WAIT] {error_msg[:50]}... {wait_time}s 후 재시도합니다. (Attempt {attempt+1}/{max_retries})")
                        time.sleep(wait_time)
                        continue
                    else:
                        # 더 이상 재시도할 수 없는 치명적 오류인 경우
                        raise e

            if not translated:
                print(f"  [FAIL] {lang_name} 번역에 최종적으로 실패했습니다.")
                results[lang_code] = {"success": False, "path": None, "error": "Max retries reached or empty response"}
                continue
            
            # Clean potential markdown code fence wrapping
            if translated.strip().startswith("```"):
                lines = translated.strip().split("\n")
                if lines[0].strip().startswith("```"):
                    lines = lines[1:]
                if lines and lines[-1].strip() == "```":
                    lines = lines[:-1]
                translated = "\n".join(lines).strip()
            
            # Apply regex to fix potentially broken tags array specifically
            # Ensure the last item ends with a quote before the closing bracket
            import re
            def fix_tags_array(txt):
                match = re.search(r'(tags:\s*\[)(.*?)(\])', txt)
                if not match: return txt
                inner = match.group(2).strip()
                if inner and inner[-1] not in ['"', "'"]:
                    inner += '"'
                return txt[:match.start()] + match.group(1) + inner + match.group(3) + txt[match.end():]
            translated = fix_tags_array(translated)
            
            # 신규 생성된 다국어 맞춤형 Slug 추출 (정규식 활용)
            new_slug_match = re.search(r'slug:\s*["\'](.*?)["\']', translated)
            
            # 강제로 원본 한국어 slug를 사용하도록 고정 (언어 전환 시 url 매핑을 위해)
            target_slug = slug
            
            # Save to the correct language folder
            target_dir = os.path.join("src", "data", "blog", lang_code, folder)
            os.makedirs(target_dir, exist_ok=True)
            target_path = os.path.join(target_dir, f"{target_slug}.md")
            
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
