import os
import json
import logging
from google import genai
from dotenv import load_dotenv

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("GlossaryExpert")

load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GLOSSARY_DIR = os.path.join(BASE_DIR, "src", "data", "blog", "ko", "glossary")

def get_existing_glossary_terms():
    """기존에 작성된 용어 사전 파일 목록을 가져옵니다 (중복 방지용)."""
    if not os.path.exists(GLOSSARY_DIR):
        return []
    
    # 파일명에서 슬러그만 추출 (예: what-is-llm.md -> what-is-llm)
    files = [f.replace(".md", "") for f in os.listdir(GLOSSARY_DIR) if f.endswith(".md")]
    return files

def pick_daily_glossary_keyword():
    """Gemini를 사용하여 오늘 작성할 새로운 IT/보안/네트워크/AI 용어를 선정합니다."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        logger.error("GEMINI_API_KEY not found.")
        return None

    client = genai.Client(api_key=api_key)
    existing_terms = get_existing_glossary_terms()
    
    prompt = f"""
당신은 IT 테크 블로그의 수석 에디터입니다. 오늘의 'IT 용어 사전(Glossary)' 포스팅을 위한 핵심 키워드를 하나 선정해 주세요.

### 🎯 선정 기준 (필수):
1. **도메인 제약**: 반드시 **IT, 사이버 보안(Security), 네트워크 인프라, AI/머신러닝** 분야 중 하나여야 합니다. 이외의 일반 상식이나 경제 용어 등은 엄격히 배제하세요.
2. **비즈니스 가치**: 일반 독자부터 실무자까지 흥미를 가질 만하고, 기술적 깊이가 있는 용어를 우선순위로 둡니다.
3. **중복 금지**: 아래 리스트에 포함된 용어는 이미 작성되었으므로 절대 다시 선정하지 마세요.
   - 기존 용어: {", ".join(existing_terms)}

### 📝 출력 형식:
반드시 아래 JSON 형식으로만 응답하세요.
{{
  "keyword": "선정된 키워드 (한글 또는 영문 약어)",
  "reason": "이 용어를 선정한 이유 (1문장)",
  "category": "분야 (IT/보안/네트워크/AI 중 택1)"
}}
"""

    try:
        response = client.models.generate_content(
            model='models/gemini-3-flash-preview',
            contents=prompt,
            config={
                'response_mime_type': 'application/json'
            }
        )
        
        data = json.loads(response.text)
        keyword = data.get("keyword")
        reason = data.get("reason")
        category = data.get("category")
        
        if keyword:
            logger.info(f"🎯 오늘의 용어 선정: {keyword} ({category}) - {reason}")
            return keyword
        return None
        
    except Exception as e:
        logger.error(f"Error picking glossary keyword: {e}")
        return None

if __name__ == "__main__":
    keyword = pick_daily_glossary_keyword()
    if keyword:
        print(f"Selected Keyword: {keyword}")
    else:
        print("Failed to select keyword.")
