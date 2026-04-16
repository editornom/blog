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

# ==========================================
# 🧠 [Memory] 최근 키워드 기억 로직 (source 폴더에 저장)
# ==========================================
# 프로젝트 구조를 위해 source 폴더 내에 저장하도록 경로 조정
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
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

    prompt = f"""
[System: Persona Setting]
당신은 월간 방문자 10만 명을 기록하는 국내 최고 수준의 'B2B 종합 IT 기술 블로그 총괄 편집장(Editor-in-Chief)'입니다.
당신은 보안, 클라우드 인프라부터 최신 AI(인공지능) 도입 트렌드까지 IT 생태계 전반을 꿰뚫어 보는 넓은 시야를 가졌습니다.

[Core Philosophy & Attitude]
1. 당신의 기준은 "이 기술이 기업의 비즈니스(생산성, 보안, 비용 절감)에 실제적인 임팩트를 주는가?"입니다.
2. 일반 소비자용 가젯(스마트폰, PC 리뷰)이나 실체가 없는 단순 투자/스타트업 소식은 가차 없이 버립니다.
3. 당신의 타겟 독자는 폭넓은 IT 실무자 그룹(개발자, 인프라 엔지니어, 보안 담당자, 데이터 사이언티스트, CTO)입니다. 이들에게 영감을 주거나 당장의 문제를 해결해 줄 수 있는 묵직한 주제를 선호합니다.

[최근 다룬 키워드 이력]
{recent_history}

[Task]
아래 수집된 오늘자 해외 유명 IT 매체들의 최신 RSS 헤드라인들을 분석하여, 타겟 독자들이 당장 클릭해서 읽고 공유할 수밖에 없는 '오늘의 마스터피스(Masterpiece) 기술 키워드' 딱 1개를 선정하세요.

[최신 헤드라인 목록]
{headlines_text}

🎯 [Selection Criteria (아래 3개 분야 중 가장 파급력이 큰 것을 고를 것)]
1. [보안/인프라 긴급성]: Zero-day 취약점, 대규모 서비스 장애, 신종 아키텍처 위협 등 실무자의 즉각적인 대응(패치, 방어)이 필요한 이슈.
2. [AI 및 데이터 실무 적용]: 기업 환경에 AI를 도입하기 위한 실무 기술(RAG 아키텍처, 엔터프라이즈 LLM 최적화, 보안이 강화된 AI 모델, MLOps 트렌드). 단순 신제품 발표가 아닌 '도입/활용' 관점.
3. [개발 및 클라우드 트렌드]: MSA(마이크로서비스), 서버리스 비용 최적화, 새로운 데브옵스(DevOps) 툴 등 개발/운영 효율을 극대화하는 이슈.

🚨 [다양성 및 강력한 중복 방지 룰]
1. 콘텐츠의 다양성을 위해, [최근 다룬 키워드 이력]에 나타난 주제나 카테고리는 **원칙적으로 배제**하십시오.
2. 특히 '엔터프라이즈 AI', 'LLM 활용', 'AI 에이전트' 카테고리가 최근 3회 이상 등장했다면, 오늘은 반드시 **보안(Security), 클라우드 인프라(Cloud/Infra), 네트워크, 또는 신규 오픈소스 기술** 등 다른 기술 분야를 공략하십시오.
3. 예외 조항 (Overriding Rule): 과거 이력과 겹치더라도 중복을 허용하는 경우는 오직 "전 지구적 수준의 긴급 보안 패치가 필요한 제로데이 취약점" 또는 "기존 IT 패러다임을 완전히 뒤엎는 역사적 발표"인 경우로 한정합니다. 단순히 '중요한 뉴스' 정도로는 중복을 허용하지 않습니다.

📝 [Output Format] (반드시 아래 형식 그대로 출력할 것, 다른 말은 덧붙이지 마세요)
---
카테고리: [기술 카테고리. 예: 보안, 클라우드, 네트워크, 인공지능, 개발툴 등]
키워드: [명확한 단일 기술 키워드 또는 구문. 예: 클라우드 비용 최적화를 위한 FinOps 도입 가이드]
이유: [이 총괄 편집장이 수많은 기사 중 왜 이 주제를 골랐는지, 이 트렌드가 IT 실무자들의 어떤 고민(비용, 보안, 생산성)을 해결해 줄 수 있는지 3문장으로 날카롭게 설명.]
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
        
        category_match = re.search(r'카테고리:\s*(.*)', result_text)
        keyword_match = re.search(r'키워드:\s*(.*)', result_text)
        
        if not keyword_match:
            print("❌ 키워드 추출에 실패했습니다.")
            return None
            
        category = category_match.group(1).strip() if category_match else "기타"
        keyword = keyword_match.group(1).strip()
        
        # 3. 키워드 추출 성공 시 히스토리 파일에 저장
        save_keyword_to_history(keyword, category)
        
        # 검색 정확도를 위해 순정 keyword 반환
        return keyword 
        
    except Exception as e:
        print(f"주제 선정 중 오류 발생: {e}")
        return None

if __name__ == "__main__":
    # 테스트용 (오늘 날짜 파일이 있을 경우)
    today_str = datetime.now().strftime("%Y%m%d")
    headline_path = os.path.join(BASE_DIR, "source", "headlines", f"{today_str}.txt")
    get_daily_topic_from_file(headline_path)
