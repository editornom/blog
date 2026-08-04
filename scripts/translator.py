from google import genai
import models
import os
import re
import datetime
from dotenv import load_dotenv
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import api_utils

load_dotenv()

LANGUAGES = {
    "en": "English",
    "cn": "Simplified Chinese (简体中文)",
    "jp": "Japanese (日本語)",
}

def translate_post(korean_markdown, target_lang, slug=None):
    """
    Translates a Korean blog post markdown into the target language using Gemini.
    Preserves frontmatter structure and markdown formatting.
    
    Args:
        korean_markdown: The full markdown content (with frontmatter) in Korean.
        target_lang: Language code ('en', 'cn', 'jp').
        slug: The original Korean post slug.
    
    Returns:
        Translated markdown string, or None on failure.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY not found in .env")
        return None

    lang_name = LANGUAGES.get(target_lang, target_lang)
    client = genai.Client(api_key=api_key)

    slug_info = f"'{slug}'" if slug else "원본 한국어 원고의 slug"

    prompt = f"""
당신은 전문 기술 번역가입니다. 아래의 한국어 블로그 원고를 {lang_name}로 번역하십시오.

### 번역 규칙:
1. **Frontmatter 유지**: YAML frontmatter(--- 사이의 영역)의 구조는 그대로 유지하되, title 과 description 항목을 각 언어에 맞게 번역하십시오.
   - 🚨 **[중요]**: 번역된 title and description의 값은 반드시 큰따옴표(" ")로 감싸야 하며, 문자열 내부에는 절대 큰따옴표나 줄바꿈을 넣지 마십시오. (필요시 홑따옴표 사용)
   - 🚨 **[참고 문헌 유지]**: `references` 항목은 외부 URL 리스트이므로 절대 번역하거나 수정하지 말고 그대로 유지하십시오.
   - 🚨 **[날짜 형식 엄수]**: `pubDatetime` 및 `modDatetime` 값에는 절대 큰따옴표(" ")나 홑따옴표(' ')를 붙이지 마십시오. 반드시 YAML 날짜 형식(예: 2024-04-22 17:00:00+09:00)을 유지해야 합니다.
2. **Slug 동일성 유지**: frontmatter의 `slug` 값은 기존 영어 slug를 복사하거나 번역하지 말고, 반드시 **{slug_info} 값을 한 글자도 바꾸지 말고 그대로 유지**하십시오. (언어 전환 시 URL 매핑과 내부 링크 무결성을 보장하기 위함)
3. **이미지 경로 유지**: 이미지 경로(../../../../assets/images/... 또는 ../../../../../source/...)는 절대 변경하지 마십시오. UUID가 포함된 경로는 오타처럼 보여도 절대로 수정해서는 안 됩니다.
4. **마크다운 문법 유지**: 헤더(#, ##, ###), 볼드(**), 리스트(-), 인용(>), 코드블록(```) 등 마크다운 문법을 그대로 유지하십시오.
   - 🚨 **[Glossary 표 번역 주의]**: 원문 표에 있는 `| **한글명** | ... |` 등의 항목은 다른 국가의 독자에게 불필요하므로, 표 번역 시 해당 행(Row)은 아예 삭제하십시오.
   - 🚨 **[배열 기호 엄수]**: tags 항목의 대괄호 [ ] 안의 항목들을 구분할 때는 반드시 영문 반각 쉼표(,)만 사용하십시오. 절대 중국어/일본어 전각 쉼표(， 또는 、)를 쓰지 마십시오.
5. **자연스러운 번역**: 직역이 아닌, {lang_name} 원어민이 읽었을 때 자연스럽고 전문적인 기술 칼럼처럼 느껴지도록 의역하십시오.
6. **고유명사 보호 (Glossary Enforcement)**: 다음 목록의 브랜드명과 IT 솔루션 전문 용어들은 엉뚱한 현지어로 직역하지 말고 반드시 영문 스펠링을 그대로 유지하거나 업계 표준 표기를 가장 우선시하십시오.
   - [보호 사전]: Editornom, VPN, UTM, API, SSL, B2B, AI, LLM, RAG, NVIDIA, CDN, SD-WAN, Playwright, Cloud, On-Premise, Node, React, Next.js
7. **이미지 알트태그 번역**: `![alt text](path)` 형식에서 `alt text` 부분을 대상 언어로 자연스럽게 번역하십시오.
8. **내부 링크 경로 및 슬러그 보존**: 원고 본문 중 `[텍스트](/ko/posts/슬러그)` 형식의 내부 링크가 있다면, 국가 코드 부분만 대상 국가 코드(예: `en`, `cn`, `jp`)로 변경하고, 슬러그 부분은 절대로 번역하거나 임의로 변경하지 마십시오.
   - 예: `/ko/posts/ax-strategy-golden-time` -> `/en/posts/ax-strategy-golden-time`
   - 중국어 번역 시에는 `/zh/posts/`가 아닌 반드시 **/cn/posts/** 형식을 사용하여 번역하십시오! (절대 `/zh/` 경로를 사용하지 마십시오)
9. **도해 블록 보존**: `<figure class="dgm ...">` 로 시작하는 도해 블록을 만나면 아래를 엄수하십시오.
   - `<b class="dgm-label">` 와 `<span class="dgm-desc">` **안쪽 텍스트만** 번역하십시오.
   - 태그 이름, class 속성값(`dgm`, `dgm-flow`, `dgm-stack`, `dgm-cycle`, `dgm-items`, `dgm-item`, `dgm-label`, `dgm-desc`), `role` 속성은 한 글자도 바꾸지 마십시오.
   - `aria-label` 속성값은 도해의 요약이므로 함께 번역하되, 항목 구분 기호 ` → ` 는 그대로 두십시오.
   - 도해 블록 전체를 **한 줄로 유지**하십시오. 태그 사이에 줄바꿈이나 빈 줄을 넣으면 렌더링이 깨집니다.
   - 도해를 이미지(`![...](...)`)나 표로 바꾸지 마십시오.

### 원본 한국어 원고:
{korean_markdown}

### ⚠️ 주의사항:
- 오직 번역된 마크다운만 출력하십시오.
- 메타 설명, 코멘트, 번역 과정 설명 등은 일절 출력하지 마십시오.
- 마크다운 코드 펜스(```markdown 등)로 감싸지 마십시오.
"""

    try:
        response = client.models.generate_content(
            model=models.TRANSLATE,
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
                model=models.TRANSLATE,
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
                    translated = translate_post(korean_draft, lang_code, slug=slug)
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
            def fix_tags_array(txt):
                match = re.search(r'(tags:\s*\[)(.*?)(\])', txt)
                if not match: return txt
                inner = match.group(2).strip()
                if inner and inner[-1] not in ['"', "'"]:
                    inner += '"'
                return txt[:match.start()] + match.group(1) + inner + match.group(3) + txt[match.end():]
            translated = fix_tags_array(translated)
            
            
            # Force the frontmatter slug to match the original Korean slug (enabling unbroken internal links and perfect language switcher mapping)
            translated = re.sub(r'^slug:\s*.*$', f'slug: "{slug}"', translated, flags=re.MULTILINE)
            
            # 강제로 원본 한국어 slug를 사용하도록 고정 (언어 전환 시 url 매핑을 위해)
            target_slug = slug
            
            # Extract pubDatetime for filename prefix (YYMMDD)
            pub_match = re.search(r'pubDatetime: (\d{4})-(\d{2})-(\d{2})', translated)
            if pub_match:
                yy, mm, dd = pub_match.group(1)[2:], pub_match.group(2), pub_match.group(3)
                prefix = f"{yy}{mm}{dd}_"
            else:
                prefix = datetime.datetime.now().strftime("%y%m%d_")
                
            # Save to the correct language folder
            target_dir = os.path.join("src", "data", "blog", lang_code, folder)
            os.makedirs(target_dir, exist_ok=True)
            target_path = os.path.join(target_dir, f"{prefix}{target_slug}.md")
            
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
