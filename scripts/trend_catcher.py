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

def get_topic_for_schedule(schedule_type, filename=None):
    """
    스케줄 타입에 맞춰서 주제를 선정합니다.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ GEMINI_API_KEY가 .env 파일에 없습니다.")
        return None
        
    client = genai.Client(api_key=api_key)
    recent_history = load_recent_keywords()
    
    if schedule_type == "09_tech_news":
        system_instruction = "당신은 IT 전문 블로그의 수석 편집장입니다.\n제공된 72시간 이내의 최신 뉴스 헤드라인을 분석하여 오늘 심층 칼럼으로 작성할 주제 1개를 선정하세요.\n[주의] 이 시간대에는 '인공지능(AI)' 관련 주제는 제외하고, 전반적인 IT, 테크, 사이버보안, 인프라, 앱개발 등의 일반 기술 트렌드에서 선정하세요."
    elif schedule_type == "15_ai_news":
        system_instruction = "당신은 AI/Tech 전문 블로그의 수석 편집장입니다.\n제공된 72시간 이내의 최신 뉴스 헤드라인을 분석하여 오늘 심층 칼럼으로 작성할 주제 1개를 선정하세요.\n[주의] 이 시간대에는 반드시 '인공지능(AI), 머신러닝, LLM' 등 AI와 직접적으로 관련된 최신 동향을 주제로 선정하세요."
    elif schedule_type == "12_tech_feature":
        system_instruction = "당신은 IT 전문 블로그의 수석 편집장입니다.\n역사상(all-time) IT, 테크, 사이버보안, 소프트웨어 개발 분야에서 있었던 '기념비적인 사건, 개발, 발견' 중 하나를 특집 기사 주제로 선정하세요.\n[주의] '인공지능(AI)' 관련 주제는 절대 제외하세요. 반드시 그 사건/발견이 이후 IT 생태계에 어떤 파장과 영향력을 미쳤는지 서술할 수 있는 심도 있는 주제여야 합니다."
    elif schedule_type == "18_ai_feature":
        system_instruction = "당신은 AI/Tech 전문 블로그의 수석 편집장입니다.\n역사상(all-time) '인공지능(AI)' 분야에서 있었던 '기념비적인 사건, 개발, 발견, 논문 발표' 중 하나를 특집 기사 주제로 선정하세요.\n반드시 그 사건/발견이 이후 AI 산업과 인류에 어떤 파장과 영향력을 미쳤는지 서술할 수 있는 심도 있는 주제여야 합니다."
    else:
        system_instruction = "당신은 IT 전문 블로그의 수석 편집장입니다."

    # 뉴스 기반일 경우 헤드라인 첨부
    headlines_text = ""
    if "news" in schedule_type:
        if not filename or not os.path.exists(filename):
            print(f"❌ '{filename}' 파일을 찾을 수 없어 분석을 종료합니다.")
            return None
        with open(filename, "r", encoding="utf-8") as f:
            headlines_text = "".join(f.readlines())

    prompt = f"""{system_instruction}

선정 시 아래 4가지 지표(각 10점 만점)를 평가하여 총점이 가장 높은 것을 고르세요.
1. 화제성/시의성: 사람들의 관심을 끌 만한가? (역사적 사건의 경우 오늘날 다시 조명할 가치가 있는가?)
2. 기술적 깊이: 단순한 현상 전달을 넘어 프로토콜, 아키텍처, 알고리즘 등을 심층 분석할 여지가 있는가?
3. 파급력(Impact): IT 생태계 전체나 개발자/기획자들의 업무 방식에 큰 영향을 미치는가(미쳤는가)?
4. 실용성/인사이트: 독자들이 실무적으로 대비하거나 적용할 만한 인사이트를 도출할 수 있는가?

[최근 과거에 다룬 주제 리스트] (중복 방지용)
- {recent_history}

반드시 위 과거 주제들과 의미론적으로 겹치지 않는 새로운 주제여야 합니다.
"""
    if "news" in schedule_type:
        prompt += f"\n[최신 뉴스 헤드라인]\n{headlines_text}\n"

    prompt += """
출력은 반드시 아래 JSON 형식을 엄격히 지켜주세요. 다른 인사말은 필요 없습니다.
{
  "selected_headline": "기사 제목 또는 특집 주제 명",
  "derived_keyword": "가장 핵심이 되는 검색용 키워드 1개 (예: 멀티모달 AI, WebAssembly)",
  "evaluation": {
    "timeliness": 9,
    "depth": 8,
    "impact": 9,
    "practicality": 7,
    "total_score": 33
  },
  "reason": "이 주제를 선정한 이유와 (특집기사인 경우) 이 이슈로 인해 이후 어떤 파장이 일어났는지 영향력을 2문장으로 요약"
}
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
    # 테스트용
    print(get_topic_for_schedule("18_ai_feature"))
