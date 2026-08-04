import models
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

# [폐지] get_topic_for_schedule
#   72시간 뉴스 헤드라인에서 화제성 점수가 가장 높은 것을 고르던 함수입니다.
#   화제성 기준 선정 때문에 914편이 서로 무관한 낱개 글로 흩어졌습니다.
#   topics.select_topic() 이 토픽 클러스터 기반 선정으로 대체합니다.

if __name__ == "__main__":
    print("상시 키워드:", len(get_evergreen_keywords()), "개")
    print("최근 이력:\n" + load_recent_keywords())
