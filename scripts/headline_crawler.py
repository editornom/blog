import os
import feedparser
import concurrent.futures
from datetime import datetime, timedelta, timezone
import time
import sys
import requests
import re
from functools import partial

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

def fetch_todays_headlines(rss_url, last_run_time=None):
    """
    RSS 피드에 접속하여 '최근 72시간 이내'에 발행된 기사 제목, 링크, 요약문을 가져옵니다.
    last_run_time이 주어지면 그 시간 이후에 발행된 기사만 가져와 중복을 방지합니다.
    """
    headlines = []
    try:
        # 브라우저인 것처럼 헤더 추가 (Action Plan 2)
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        }
        # requests를 사용하여 10초 타임아웃 설정으로 데이터 가져오기
        response = requests.get(rss_url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # 가져온 텍스트 데이터를 feedparser로 파싱
        feed = feedparser.parse(response.text)
        now_utc = datetime.now(timezone.utc)
        
        # RSS 피드 유효성 검사 보강 (Action Plan 4)
        if getattr(feed, 'bozo', 0) == 1:
            print(f"⚠️ '{rss_url}' 피드 파싱 오류(bozo): 형식이 깨진 피드일 수 있으나 추출을 시도합니다.")
            
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
                # 중복 수집 방지 (Action Plan 1)
                if last_run_time and pub_time <= last_run_time:
                    continue

                # 데이터 구조 확장: 요약문(Description) 포함 (Action Plan 3)
                summary = getattr(entry, 'summary', getattr(entry, 'description', ''))
                clean_summary = re.sub(r'<[^>]+>', '', summary).strip()
                if clean_summary:
                    # 요약문이 너무 길면 자름, 줄바꿈 제거
                    clean_summary = clean_summary.replace('\n', ' ').replace('\r', '')
                    clean_summary = ' - ' + clean_summary[:200] + ('...' if len(clean_summary) > 200 else '')
                else:
                    clean_summary = ''

                # [진짜 본문 URL] 기사 제목 - 요약문 형태
                headlines.append(f"[{entry.link}] {entry.title}{clean_summary}")
        
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

    # 중복 수집 방지를 위한 마지막 실행 시간 읽기 (Action Plan 1)
    last_run_path = os.path.join(base_dir, "source", "headlines", "last_run.txt")
    last_run_time = None
    if os.path.exists(last_run_path):
        try:
            with open(last_run_path, "r", encoding="utf-8") as f:
                last_run_time = datetime.fromisoformat(f.read().strip())
        except Exception:
            pass

    print(f"\n🌐 {len(urls)}개 매체의 RSS 피드에서 '최근 72시간 이내' 최신글을 수집합니다...")
    if last_run_time:
         print(f"🕒 마지막 성공 수집: {last_run_time.strftime('%Y-%m-%d %H:%M:%S UTC')} 이후의 글만 가져옵니다.")
         
    all_headlines = []
    # 병렬 처리로 수십 개 사이트를 순식간에 스캔
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        fetch_func = partial(fetch_todays_headlines, last_run_time=last_run_time)
        results = executor.map(fetch_func, urls)
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
        
    # 성공적으로 수집을 완료했으므로 last_run.txt 갱신 (Action Plan 1)
    try:
        with open(last_run_path, "w", encoding="utf-8") as f:
            f.write(datetime.now(timezone.utc).isoformat())
    except Exception as e:
        print(f"⚠️ 마지막 수집 시간(last_run) 갱신 실패: {e}")
        
    print(f"✅ 수집 완료! 총 {len(all_headlines)}개의 헤드라인이 '{output_path}'에 저장되었습니다.")
    return output_path

if __name__ == "__main__":
    generate_daily_headlines_file("list.txt")
