import os
import re
import datetime
from datetime import datetime
from google import genai
from dotenv import load_dotenv
import sys

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

load_dotenv()

import json
import random

# 공통 디렉토리 설정
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ==========================================
# [Fallback] 상시(Evergreen) 키워드 풀
# ==========================================
EVERGREEN_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "evergreen_keywords.txt")

def get_evergreen_keywords():
    """상시(Evergreen) 키워드 텍스트 파일에서 리스트를 불러옵니다."""
    try:
        if os.path.exists(EVERGREEN_FILE):
            with open(EVERGREEN_FILE, "r", encoding="utf-8") as f:
                keywords = [line.strip() for line in f if line.strip() and not line.startswith("#")]
            if keywords:
                return keywords
    except Exception as e:
        print(f"⚠️ 상시 키워드 파일을 읽지 못했습니다: {e}")
    # 파일이 없거나 오류 발생 시 기본값
    return ["안전한 하이브리드 클라우드 아키텍처", "엔터프라이즈 제로트러스트 가이드"]

# ==========================================
# 🧠 [Memory] 최근 키워드 기억 로직 (source 폴더에 저장)
# ==========================================
HISTORY_FILE = os.path.join(BASE_DIR, "source", "keyword_history.txt")

def load_recent_keywords():
    """최근 사용된 키워드 이력을 불러옵니다."""
    if not os.path.exists(HISTORY_FILE):
        return "최근 발행 이력이 없습니다."
    
    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()
        # 최근 10개 정도로 넉넉하게 불러오기
        return "".join(lines[-10:]) 

def save_keyword_to_history(keyword, category="기타"):
    """오늘 선정된 키워드와 카테고리를 역사에 기록합니다."""
    today = datetime.now().strftime("%Y-%m-%d")
    with open(HISTORY_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{today}] [{category}] {keyword}\n")
# ==========================================

def get_daily_topic_from_file(filename):
    """
    저장된 YYYYMMDD.txt 파일을 읽어 Gemini를 통해 핵심 키워드를 추출합니다.
    """
    if not filename or not os.path.exists(filename):
        print(f"❌ '{filename}' 파일을 찾을 수 없어 분석을 종료합니다.")
        return None

    print(f"\n🧠 '{os.path.basename(filename)}' 파일의 데이터를 읽어 AI 분석을 시작합니다...")

    with open(filename, "r", encoding="utf-8") as f:
        headlines_raw = f.readlines()
    
    headlines_text = "".join(headlines_raw)

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ GEMINI_API_KEY가 .env 파일에 없습니다.")
        return None
        
    client = genai.Client(api_key=api_key)

    # 1. AI에게 보여줄 과거 이력 불러오기
    recent_history = load_recent_keywords()

    prompt = f"""당신은 IT 전문 블로그의 수석 편집장입니다. 
아래 제공된 최근 72시간 이내의 뉴스 헤드라인 목록을 분석하여, 오늘 심층 칼럼으로 작성하기 가장 완벽한 주제 1개를 선정하세요.

선정 시 아래 4가지 지표(각 10점 만점)를 평가하여 총점이 가장 높은 것을 고르세요.
1. 시의성(Timeliness): 지금 당장 화제가 되고 검색량이 폭증할 만한가?
2. 기술적 깊이(Depth): 단순한 현상 전달을 넘어 프로토콜, 아키텍처, 알고리즘 등을 심층 분석할 여지가 있는가?
3. 파급력(Impact): IT 생태계 전체나 개발자/기획자들의 업무 방식에 큰 영향을 미치는가?
4. 실용성(Practicality): 독자들이 실무적으로 대비하거나 적용할 만한 인사이트를 도출할 수 있는가?

[최근 과거에 다룬 주제 리스트] (중복 방지용)
- {recent_history}

반드시 위 과거 주제들과 의미론적으로 겹치지 않는 새로운 주제여야 합니다.

[최신 뉴스 헤드라인]
{headlines_text}

출력은 반드시 아래 JSON 형식을 엄격히 지켜주세요. 다른 인사말은 필요 없습니다.
{{
  "selected_headline": "[원문 URL] 기사 제목",
  "derived_keyword": "가장 핵심이 되는 검색용 키워드 1개 (예: 멀티모달 AI, WebAssembly)",
  "evaluation": {{
    "timeliness": 9,
    "depth": 8,
    "impact": 9,
    "practicality": 7,
    "total_score": 33
  }},
  "reason": "이 주제를 선정한 이유를 2문장으로 요약"
}}
"""

    try:
        response = client.models.generate_content(
            model='models/gemini-3-flash-preview', 
            contents=prompt
        )
        
        result_text = response.text.strip()
        print("\n" + "="*40)
        print("🎯 [AI 수석 에디터의 오늘의 픽]")
        print("="*40)
        print(result_text)
        print("="*40 + "\n")
        
        # JSON 블록 추출 로직
        json_str = result_text
        if "```json" in json_str:
            json_str = json_str.split("```json")[1].split("```")[0].strip()
        elif "```" in json_str:
            json_str = json_str.split("```")[1].split("```")[0].strip()
            
        data = json.loads(json_str)
        keyword = data.get("derived_keyword")
        
        if not keyword:
            raise ValueError("❌ JSON에서 derived_keyword를 찾을 수 없습니다.")
            
        # 3. 키워드 추출 성공 시 히스토리 파일에 저장 (카테고리 대신 점수로 기록)
        score = data.get("evaluation", {}).get("total_score", 0)
        save_keyword_to_history(keyword, f"AI추천_{score}점")
        
        # 검색 정확도를 위해 순정 keyword 반환
        return keyword 
        
    except Exception as e:
        print(f"⚠️ 주제 선정 중 오류 발생: {e}")
        # Fallback 로직 작동
        evergreen_pool = get_evergreen_keywords()
        fallback_keyword = random.choice(evergreen_pool)
        print(f"🔄 대비책(Fallback) 가동: 상시 키워드 풀에서 '{fallback_keyword}'(을)를 선택합니다.")
        save_keyword_to_history(fallback_keyword, "Fallback")
        return fallback_keyword

if __name__ == "__main__":
    # 테스트용 (오늘 날짜 파일이 있을 경우)
    today_str = datetime.now().strftime("%Y%m%d")
    headline_path = os.path.join(BASE_DIR, "source", "headlines", f"{today_str}.txt")
    get_daily_topic_from_file(headline_path)
