import os
import requests
import json
import re
from google import genai
from dotenv import load_dotenv
import sys

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

load_dotenv()

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

    if not results:
        print("❌ 검색 결과가 없습니다.")
        return []

    print(f"✅ {len(results)}개의 검색 결과를 찾았습니다. AI 기반 필터링을 시작합니다...")

    # 2. AI(Gemini)에게 10개 엄선 시키기
    gemini_key = os.getenv("GEMINI_API_KEY")
    client = genai.Client(api_key=gemini_key)

    # 분석을 위한 데이터 요약 (토큰 절약을 위해 제목과 스니펫만 전달)
    results_summary = ""
    for i, r in enumerate(results):
        results_summary += f"[{i}] 제목: {r.get('title')}\n요약: {r.get('snippet')}\n링크: {r.get('link')}\n\n"

    prompt = f"""
당신은 IT 기술 문서 전문 큐레이터입니다. 
아래 {len(results)}개의 검색 결과 중에서, '{keyword}'라는 주제로 깊이 있는 B2B 기술 블로그를 작성하기 위해 '가장 기술적 가치가 높고 신뢰할 수 있는 소스' 10개만 엄선하세요.

[검색 결과 리스트]
{results_summary}

🎯 선정 기준:
1. 광고성 글, 단순 뉴스 보도보다는 기술 백서, 공식 문서, 심층 분석 리포트, 유명 기술 블로그(예: AWS Blog, Netflix Tech Blog)를 우선합니다.
2. 정보의 중복을 피하고 다양한 관점(인프라, 보안, 실무 적용, 트러블슈팅 등)을 포함하세요.
3. 링크가 유효하고 본문 내용이 풍부할 것으로 예상되는 것을 고르세요.

📝 출력 형식:
선정된 항목의 인덱스 번호만 콤마(,)로 구분해서 정확히 출력하세요. 다른 설명은 일절 배제하세요.
예시: 1, 5, 12, 24, 33, 45, 50, 62, 77, 89
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
            if 0 <= idx < len(results):
                selected_urls.append(results[idx]['link'])
        
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

if __name__ == "__main__":
    # 테스트용
    test_keyword = "Model Context Protocol"
    deep_search_and_filter(test_keyword)
