import requests
from bs4 import BeautifulSoup
import re

def fetch_content(url):
    """
    Fetches the content from a given URL and extracts the title and main body text.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10, verify=False)
        response.raise_for_status()
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

    response.encoding = response.apparent_encoding
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Remove unwanted elements
    for script_or_style in soup(["script", "style", "header", "footer", "nav", "aside"]):
        script_or_style.decompose()

    # Get title
    title = soup.title.string if soup.title else "No Title"
    
    # 본문 추출을 위한 헬퍼 함수
    def extract_text_from_soup(s_obj):
        text = ""
        article = s_obj.find(['article', 'main', 'section','magazine'])
        if article:
            text = article.get_text(separator='\n', strip=True)
        else:
            paragraphs = s_obj.find_all('p')
            text = "\n\n".join([p.get_text(strip=True) for p in paragraphs if len(p.get_text(strip=True)) > 20])
            if len(text) < 200:
                divs = s_obj.find_all('div', class_=re.compile(r'content|body|post|article|inner|main', re.I))
                if divs:
                    text = max([d.get_text(separator='\n', strip=True) for d in divs], key=len)
        return text

    main_text = extract_text_from_soup(soup)

    # 1. SPA/동적 렌더링 대비 Fallback (Action Plan 1)
    if len(main_text) < 100:
        try:
            from playwright.sync_api import sync_playwright
            print(f"🔄 '{url}' 정적 본문 추출 실패. Playwright 헤드리스 브라우저로 재시도합니다...")
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                page.goto(url, timeout=15000)
                try:
                    page.wait_for_load_state("networkidle", timeout=10000)
                except Exception:
                    pass # 타임아웃 무시하고 현재 상태의 DOM이라도 긁어옴
                dyn_content = page.content()
                browser.close()
                
            dyn_soup = BeautifulSoup(dyn_content, 'html.parser')
            for script_or_style in dyn_soup(["script", "style", "header", "footer", "nav", "aside"]):
                script_or_style.decompose()
            main_text = extract_text_from_soup(dyn_soup)
        except ImportError:
            print("💡 [Tip] 동적 페이지(SPA) 처리를 위해 playwright를 설치해주세요: pip install playwright && playwright install")
        except Exception as e:
            print(f"⚠️ Playwright 폴백 실패: {e}")

    # 2. 방해 문구 정규식 제거 (Action Plan 2)
    distractive_patterns = [
        r"(?i)(cookie settings|privacy policy|개인정보\s*처리방침|개인정보\s*보호정책|쿠키\s*설정|terms of service|이용약관|accept cookies|allow cookies).{0,200}",
        r"(?i)(이용에 동의|수집에 동의|마케팅 수신동의).*동의",
        r"(?i)(로그인 후 이용|구독자 전용|결제 후 이용).*"
    ]
    for pattern in distractive_patterns:
        main_text = re.sub(pattern, "", main_text)
    main_text = main_text.strip()

    # 3. Token Safeguard (Action Plan 3)
    # API 한도 초과 방지를 위해 본문 크기를 엄격히 제한
    MAX_CHARS = 12000
    if len(main_text) > MAX_CHARS:
        half_limit = MAX_CHARS // 2
        # 문맥을 덜 잃도록 앞부분과 뒷부분 단락 샘플링
        main_text = main_text[:half_limit] + "\n\n... [중략: Token Safeguard 작동으로 생략됨] ...\n\n" + main_text[-half_limit:]

    return {
        "url": url,
        "title": title.strip(),
        "body": main_text,
        "html_raw": response.text
    }

def extract_related_links(base_url, html_content, max_links=10):
    """
    Extracts internal links from the HTML content that are related to the base URL.
    """
    from urllib.parse import urljoin, urlparse
    soup = BeautifulSoup(html_content, 'html.parser')
    links = set()
    
    parsed_base = urlparse(base_url)
    base_domain = f"{parsed_base.scheme}://{parsed_base.netloc}"
    # Target path for context (e.g., /colocation/)
    base_path_parts = parsed_base.path.strip('/').split('/')
    parent_path = "/" + "/".join(base_path_parts[:-1]) if len(base_path_parts) > 1 else "/"

    for a in soup.find_all('a', href=True):
        href = a['href']
        full_url = urljoin(base_url, href)
        parsed_url = urlparse(full_url)
        
        # Only internal links
        if parsed_url.netloc != parsed_base.netloc:
            continue
            
        # Skip anchors, non-http, and common noise
        if '#' in href or not full_url.startswith('http'):
            continue
        
        # Extensions to skip
        if any(full_url.lower().endswith(ext) for ext in [".png", ".jpg", ".jpeg", ".pdf", ".zip"]):
            continue

        # Prioritize links in the same directory or subdirectories
        if full_url != base_url and (full_url.startswith(base_domain + parent_path) or len(links) < max_links):
            links.add(full_url)
            
        if len(links) >= max_links:
            break
            
    return list(links)

if __name__ == "__main__":
    test_url = "https://haion.net/colocation/gpu.php"
    # To test this manually, we would need real HTML.
    # For now, it's integrated into the main pipeline.
    content = fetch_content(test_url)
    if content:
        print(f"Title: {content['title']}")
        # print(f"Body snippet: {content['body'][:200]}...")
