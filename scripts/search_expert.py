import os
import requests
import json
import re
import concurrent.futures
from google import genai
from dotenv import load_dotenv
import sys

# crawler.py에서 본문 추출 함수 가져오기
from crawler import fetch_content

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

load_dotenv()

def probe_url(r, index):
    """
    개별 URL에 접속하여 실제 본문 데이터가 있는지 확인하고 미리보기를 추출합니다.
    """
    url = r.get('link')
    if not url:
        return None
    
    try:
        # crawler.py의 fetch_content 재사용
        content = fetch_content(url)
        if content and content.get('body'):
            body_len = len(content['body'])
            if body_len > 50:
                # 본문이 유효한 경우만 반환 (앞부분 1200자 추출)
                preview = content['body'][:1200].replace("\n", " ")
                return {
                    "index": index,
                    "title": content['title'],
                    "link": url,
                    "preview": preview,
                    "original_snippet": r.get('snippet', '')
                }
    except Exception:
        pass
    return None

def deep_search_and_filter(keyword, num_results=100):
    """
    키워드로 웹 검색을 수행하고(최대 100개), Gemini를 통해 가장 가치 있는 10개를 선별합니다.
    """
    api_key = os.getenv("SERPER_API_KEY")
    if not api_key:
        print("⚠️ SERPER_API_KEY가 .env에 없습니다. 검색을 건너뛰고 빈 리스트를 반환합니다.")
        return []

    print(f"🔍 '{keyword}'에 대한 광범위 웹 검색을 시작합니다 (목표: {num_results}개)...")

    # 1. Serper API를 이용한 검색
    url = "https://google.serper.dev/search"
    payload = json.dumps({
        "q": keyword,
        "num": num_results
    })
    headers = {
        'X-API-KEY': api_key,
        'Content-Type': 'application/json'
    }

    try:
        response = requests.post(url, headers=headers, data=payload)
        response.raise_for_status()
        results = response.json().get('organic', [])
    except Exception as e:
        print(f"❌ 검색 중 오류 발생: {e}")
        return []

    # [강화된 블랙리스트] 기술 분석이 불가능하거나 부적합한 소스 사전 필터링
    EXCLUDED_DOMAINS = [
        "youtube.com", "youtu.be", "vimeo.com", "dailymotion.com", # 동영상
        "blog.naver.com", "m.blog.naver.com", "cafe.naver.com", "m.cafe.naver.com", # 네이버 프레임 구조
        "threads.net", "facebook.com", "instagram.com", "tiktok.com", # SNS
        "twitter.com", "x.com", "linkedin.com", "pinterest.com",
        "reddit.com", "quora.com", # 커뮤니티 (JS 의존성 높음)
        "amazon.com", "ebay.com", "coupang.com", # 커머스
        "play.google.com", "apps.apple.com" # 앱스토어
    ]

    EXCLUDED_EXTENSIONS = [
        ".pdf", ".zip", ".doc", ".docx", ".xls", ".xlsx", 
        ".ppt", ".pptx", ".exe", ".dmg", ".mp4", ".mov", ".png", ".jpg", ".jpeg"
    ]
    
    filtered_results = []
    domain_count = 0
    ext_count = 0

    for r in results:
        link = r.get('link', '').lower()
        
        # 1. 도메인 체크
        if any(domain in link for domain in EXCLUDED_DOMAINS):
            domain_count += 1
            continue
            
        # 2. 확장자 체크
        if any(link.endswith(ext) for ext in EXCLUDED_EXTENSIONS):
            ext_count += 1
            continue
            
        filtered_results.append(r)
    
    if domain_count > 0:
        print(f"🚫 부적합 도메인(SNS, 동영상 등) {domain_count}개를 필터링했습니다.")
    if ext_count > 0:
        print(f"📎 실행/문서 파일(PDF, ZIP 등) {ext_count}개를 필터링했습니다.")
    
    results = filtered_results

    if not results:
        print("❌ 필터링 후 남은 검색 결과가 없습니다.")
        return []

    # [DeepSearch 2.0] 모든 사이트 직접 방문 및 본문 검증 (멀티스레딩)
    print(f"🌐 [Stage 1] {len(results)}개 사이트 직접 방문 및 본문 검증 중 (잠시만 기다려 주세요)...")
    
    probed_results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        # 각 결과에 대해 probe_url 실행
        future_to_url = {executor.submit(probe_url, r, i): i for i, r in enumerate(results)}
        for future in concurrent.futures.as_completed(future_to_url):
            res = future.result()
            if res:
                probed_results.append(res)
    
    if not probed_results:
        print("❌ 직접 방문 결과, 유효한 본문 데이터가 있는 사이트를 찾지 못했습니다.")
        # 만약 크롤링이 다 실패했다면 snippet 기반이라도 사용하기 위해 원본 results 사용 (폴백)
        final_candidates = results[:20] 
        use_preview = False
    else:
        # 성공적으로 크롤링된 데이터들만 사용
        # 인덱스 순서대로 정렬 (원본 검색 순서 유지)
        probed_results.sort(key=lambda x: x['index'])
        final_candidates = probed_results
        use_preview = True
        print(f"✅ {len(final_candidates)}개 사이트에서 실제 본문 데이터를 확보했습니다.")

    # 2. AI(Gemini)에게 10개 엄선 시키기
    gemini_key = os.getenv("GEMINI_API_KEY")
    client = genai.Client(api_key=gemini_key)

    # 분석을 위한 데이터 요약 (본문 미리보기 데이터 활용)
    results_summary = ""
    for i, r in enumerate(final_candidates):
        content_source = r.get('preview') if use_preview else r.get('snippet')
        results_summary += f"[{i}] 제목: {r.get('title')}\n본문 미리보기: {content_source[:600]}...\n링크: {r.get('link')}\n\n"

    prompt = f"""
당신은 IT 기술 문서 전문 큐레이터입니다. 
아래 {len(final_candidates)}개의 기술 사이트 '실제 본문 데이터'를 분석하여, '{keyword}' 주제로 고품질 B2B 기술 블로그를 작성하기 위해 가장 가치 있는 소스 10개만 엄선하세요.

[검색 결과 리스트 (실제 본문 기반)]
{results_summary}

🎯 선정 기준:
1. '본문 미리보기'를 보고 실제 기술적 내용(코드, 아키텍처, 실무 가이드)이 풍부한지 확인하세요.
2. 제목만 그럴듯하고 본문 알맹이가 없는 '낚시성' 글은 가차 없이 버리세요.
3. 공식 도큐먼트, 벤더 공식 블로그, 대규모 엔지니어링 리포트를 최우선 순위로 둡니다.
4. 다양한 관점(보안, 성능, 비용, 운영)을 아우를 수 있도록 소스를 조합하세요.

📝 출력 형식:
선정된 항목의 인덱스 번호만 콤마(,)로 구분해서 정확히 출력하세요. (예: 1, 3, 7...)
인덱스 번호 외에 다른 말은 절대 하지 마세요.
"""

    try:
        # 모델명은 프로젝트 통합을 위해 gemini-3-flash-preview 사용
        response = client.models.generate_content(
            model='models/gemini-3-flash-preview',
            contents=prompt
        )
        
        selection_text = response.text.strip()
        # 숫자만 추출
        indices = [int(idx.strip()) for idx in re.findall(r'\d+', selection_text)]
        
        selected_urls = []
        for idx in indices:
            if 0 <= idx < len(final_candidates):
                selected_urls.append(final_candidates[idx]['link'])
        
        # 중복 제거 및 상위 10개 제한
        top_10_urls = list(dict.fromkeys(selected_urls))[:10]
        
        print(f"✨ AI가 최적의 소스 {len(top_10_urls)}개를 선별했습니다.")
        
        # 결과 기록을 위해 source/url/{keyword}.txt 에 저장
        save_urls_to_file(top_10_urls, keyword)
        
        return top_10_urls

    except Exception as e:
        print(f"⚠️ AI 필터링 중 오류 발생: {e}")
        # 오류 발생 시 검색 결과의 상위 10개 반환
        return [r['link'] for r in results[:10]]

def save_urls_to_file(urls, keyword):
    """
    선별된 URL들을 source/url/{keyword}.txt 파일로 저장합니다.
    """
    try:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        url_dir = os.path.join(base_dir, "source", "url")
        os.makedirs(url_dir, exist_ok=True)
        
        safe_keyword = re.sub(r'[\\/*?:"<>|]', "", keyword).replace(" ", "_")
        url_file_path = os.path.join(url_dir, f"{safe_keyword}.txt")
        
        with open(url_file_path, "w", encoding="utf-8") as f:
            f.write("\n".join(urls))
        
        print(f"💾 선별된 URL 리스트가 '{url_file_path}'에 저장되었습니다.")
    except Exception as e:
        print(f"⚠️ URL 파일 저장 중 오류 발생: {e}")

def select_best_from_list(urls, keyword):
    """
    [NEW] 제공된 URL 리스트 중에서 키워드에 가장 적합한 10개를 직접 방문하여 선별합니다.
    """
    if not urls:
        return []

    print(f"🌐 [Selection] {len(urls)}개의 수동 URL 중 '{keyword}' 최적 소스 선별 중...")
    
    # 1. 본문 검증 및 미리보기 추출 (DeepSearch 2.0 엔진 사용)
    probed_results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        # probe_url 함수를 사용하여 본문 데이터 확보
        # probe_url 기대 형식: {"link": url}
        future_to_url = {executor.submit(probe_url, {"link": url}, i): i for i, url in enumerate(urls)}
        for future in concurrent.futures.as_completed(future_to_url):
            res = future.result()
            if res:
                probed_results.append(res)
    
    if not probed_results:
        print("❌ 유효한 본문을 가진 사이트가 없습니다. 원본 리스트를 사용합니다.")
        return urls[:10]

    # 인덱스 순 정렬
    probed_results.sort(key=lambda x: x['index'])
    
    # 2. AI(Gemini)에게 선별 시키기
    gemini_key = os.getenv("GEMINI_API_KEY")
    client = genai.Client(api_key=gemini_key)

    results_summary = ""
    for i, r in enumerate(probed_results):
        results_summary += f"[{i}] 제목: {r.get('title')}\n본문 미리보기: {r.get('preview')[:600]}...\n링크: {r.get('link')}\n\n"

    prompt = f"""
당신은 IT 기술 문서 전문 큐레이터입니다. 
아래 {len(probed_results)}개의 수동 수집 사이트 본문 데이터를 분석하여, '{keyword}' 주제로 고품질 홍보 포스팅을 작성하기 위해 가장 가치 있는 소스 10개만 엄선하세요.

[수동 수집 리스트 (본문 기반)]
{results_summary}

🎯 선정 기준:
1. '{keyword}'의 특징과 장점을 가장 잘 설명할 수 있는 본문 내용을 가진 사이트를 우선합니다.
2. 실제 기술 사양, 서비스 프로세스, 도입 효과가 구체적으로 적힌 소스를 선택하세요.
3. 중복되는 정보보다는 서로 보완적인 정보를 가진 소스들을 조합하세요.

📝 출력 형식:
선정된 항목의 인덱스 번호만 콤마(,)로 구분해서 정확히 출력하세요. (예: 1, 4, 8...)
"""

    try:
        response = client.models.generate_content(
            model='models/gemini-3-flash-preview',
            contents=prompt
        )
        selection_text = response.text.strip()
        indices = [int(idx.strip()) for idx in re.findall(r'\d+', selection_text)]
        
        selected_urls = []
        for idx in indices:
            if 0 <= idx < len(probed_results):
                selected_urls.append(probed_results[idx]['link'])
        
        top_10_urls = list(dict.fromkeys(selected_urls))[:10]
        print(f"✨ 수동 리스트 중 최적의 {len(top_10_urls)}개 소스를 선별했습니다.")
        return top_10_urls

    except Exception as e:
        print(f"⚠️ AI 선별 중 오류 발생: {e}")
        return urls[:10]

if __name__ == "__main__":
    # 테스트용
    test_keyword = "Model Context Protocol"
    deep_search_and_filter(test_keyword)
