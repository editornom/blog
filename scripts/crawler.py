import requests
from bs4 import BeautifulSoup
import re

def fetch_content(url):
    """
    Fetches the content from a given URL and extracts the title and main body text.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10, verify=False)
        response.raise_for_status()
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Remove unwanted elements
    for script_or_style in soup(["script", "style", "header", "footer", "nav", "aside"]):
        script_or_style.decompose()

    # Get title
    title = soup.title.string if soup.title else "No Title"
    
    # Extract main text (Heuristic approach: looking for article or div with many p tags)
    # This is a basic implementation and can be tuned for specific sites.
    main_text = ""
    
    # Try common article tags
    article = soup.find(['article', 'main', 'section'])
    if article:
        main_text = article.get_text(separator='\n', strip=True)
    else:
        # Fallback 1: combine all paragraph texts
        paragraphs = soup.find_all('p')
        main_text = "\n\n".join([p.get_text(strip=True) for p in paragraphs if len(p.get_text(strip=True)) > 20])
        
        # Fallback 2: If still empty or very short, try to find the largest div with a content-related class
        if len(main_text) < 200:
            divs = soup.find_all('div', class_=re.compile(r'content|body|post|article|inner|main', re.I))
            if divs:
                # Get the div with the most text
                main_text = max([d.get_text(separator='\n', strip=True) for d in divs], key=len)

    return {
        "url": url,
        "title": title.strip(),
        "body": main_text.strip(),
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
