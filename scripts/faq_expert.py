import os
import re
from google import genai
from google.api_core import exceptions
from api_utils import gemini_retry, gemini_limiter
from dotenv import load_dotenv
import sys

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

load_dotenv()

def generate_faq(draft, keyword):
    """
    블로그 원고 내용을 기반으로 기초 5개, 심화 5개 등 총 10개의 FAQ를 생성합니다.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ GEMINI_API_KEY가 .env에 없습니다.")
        return False

    client = genai.Client(api_key=api_key)

    print(f"🧠 '{keyword}' 주제에 대한 자동 FAQ 생성을 시작합니다 (총 10항목)...")

    prompt = f"""
당신은 IT 전문 블로그의 테크니컬 에디터입니다. 
제공된 블로그 원고 내용을 바탕으로, 독자들이 궁금해할 만한 핵심 FAQ 10개를 작성하세요.

[블로그 원고]
{draft}

[작성 가이드라인]
1. 총 10개의 문답(Q&A)을 작성하세요.
2. 처음 5개(Q1~Q5)는 주제에 대한 '기초적인 질문'으로 구성하세요. (예: ~이란 무엇인가요?, 주요 특징은?, 왜 중요한가요? 등)
3. 나머지 5개(Q6~Q10)는 실제 실무나 심화된 내용을 다루는 '발전된 질문'으로 구성하세요. (예: 도입 시 고려사항은?, 기존 방식과의 차이점은?, 보안상 유의점은? 등)
4. 답변은 원고의 내용을 바탕으로 하되, 2~3문장 내외로 명확하고 친절하게 작성하세요.
5. 출력 형식은 아래 형식을 정확히 따르세요.

[출력 형식 예시]
Q1: 질문 내용
A1: 답변 내용

Q2: 질문 내용
A2: 답변 내용
...

선택된 언어(한국어)로 작성하세요. 다른 메타 코멘트는 일절 배제하세요.
"""

    @gemini_retry
    def call_api():
        gemini_limiter.consume()
        return client.models.generate_content(
            model='models/gemini-3-flash-preview',
            contents=prompt
        )

    try:
        response = call_api()
        faq_text = response.text.strip()
        
        if not faq_text:
            print("❌ FAQ 생성 결과가 비어있습니다.")
            return False

        # 저장 디렉토리 및 파일 경로 설정
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        accordian_dir = os.path.join(base_dir, "source", "accordian")
        os.makedirs(accordian_dir, exist_ok=True)
        
        safe_keyword = re.sub(r'[\\/*?:"<>|]', "", keyword).replace(" ", "_")
        faq_file_path = os.path.join(accordian_dir, f"{safe_keyword}.txt")
        
        with open(faq_file_path, "w", encoding="utf-8") as f:
            f.write(faq_text)
            
        print(f"✅ 총 10개의 FAQ가 생성되어 '{faq_file_path}'에 저장되었습니다.")
        return True

    except Exception as e:
        print(f"⚠️ FAQ 생성 중 최종 실패: {e}")
        return False

if __name__ == "__main__":
    # 테스트용
    test_draft = "MCP(Model Context Protocol)는 AI 에이전트와 데이터 소스 간의 연결을 표준화하는 오픈 소스 프로토콜입니다..."
    test_keyword = "MCP"
    generate_faq(test_draft, test_keyword)
