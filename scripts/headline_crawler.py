import os
import feedparser
import concurrent.futures
from datetime import datetime, timedelta, timezone
import time
import sys
import requests

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

def fetch_todays_headlines(rss_url):
    """
    RSS 피드에 접속하여 '최근 72시간 이내'에 발행된 기사 제목과 진짜 링크를 가져옵니다.
    """
    headlines = []
    try:
        # requests를 사용하여 10초 타임아웃 설정으로 데이터 가져오기
        response = requests.get(rss_url, timeout=10)
        response.raise_for_status()
        
        # 가져온 텍스트 데이터를 feedparser로 파싱
        feed = feedparser.parse(response.text)
        now_utc = datetime.now(timezone.utc)
        
        for entry in feed.entries:
            # 기사의 발행일(published_parsed) 확인
            pub_time = None
            if hasattr(entry, 'published_parsed') and entry.published_parsed:
                try:
                    pub_time = datetime.fromtimestamp(time.mktime(entry.published_parsed), timezone.utc)
                except Exception:
                    continue
            
            # 발행일 정보가 없으면 오늘 기사로 간주할지 말지 결정 (여기선 패스)
            if not pub_time:
                continue

            # 핵심 로직: 현재 시간 기준으로 72시간 이내에 발행된 글인지 검증
            if now_utc - pub_time <= timedelta(hours=72):
                # [진짜 본문 URL] 기사 제목 형태
                headlines.append(f"[{entry.link}] {entry.title}")
        
        # 한 사이트당 최대 10개까지 허용 (데이터 다양성 확보)
        return headlines[:10]
    except (requests.exceptions.Timeout, requests.exceptions.RequestException) as e:
        print(f"⚠️ '{rss_url}' 접속 실패 (타임아웃 또는 네트워크 오류): {e}")
        return []
    except Exception as e:
        print(f"❌ '{rss_url}' 수집 중 예기치 못한 오류: {e}")
        return []

def generate_daily_headlines_file(list_filename="list.txt"):
    """
    RSS URL 리스트를 읽어 오늘자 헤드라인만 수집하고 source/headlines/YYYYMMDD.txt 파일로 저장합니다.
    """
    # script 위치(scripts/) 기준으로 list.txt 경로 처리
    current_dir = os.path.dirname(os.path.abspath(__file__))
    list_path = os.path.join(current_dir, list_filename)
    
    # base_dir은 프로젝트 루트로 설정 (source/headlines 저장을 위해)
    base_dir = os.path.dirname(current_dir)
    
    if not os.path.exists(list_path):
        print(f"❌ '{list_path}' 파일이 없습니다.")
        return None

    with open(list_path, "r", encoding="utf-8") as f:
        urls = [line.strip() for line in f if line.strip() and not line.startswith("#")]

    print(f"\n🌐 {len(urls)}개 매체의 RSS 피드에서 '최근 72시간 이내' 최신글을 수집합니다...")
    
    all_headlines = []
    # 병렬 처리로 수십 개 사이트를 순식간에 스캔
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        results = executor.map(fetch_todays_headlines, urls)
        for result in results:
            all_headlines.extend(result)

    if not all_headlines:
        print("❌ 오늘 발행된 새로운 기사가 없거나 수집에 실패했습니다.")
        return None

    # 저장 디렉토리 생성
    output_dir = os.path.join(base_dir, "source", "headlines")
    os.makedirs(output_dir, exist_ok=True)

    # 오늘 날짜로 파일명 생성 (예: 20260409.txt)
    today_str = datetime.now().strftime("%Y%m%d")
    output_filename = f"{today_str}.txt"
    output_path = os.path.join(output_dir, output_filename)
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(all_headlines))
        
    print(f"✅ 수집 완료! 총 {len(all_headlines)}개의 헤드라인이 '{output_path}'에 저장되었습니다.")
    return output_path

if __name__ == "__main__":
    generate_daily_headlines_file("list.txt")
