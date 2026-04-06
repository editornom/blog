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
    article = soup.find('article')
    if article:
        main_text = article.get_text(separator='\n', strip=True)
    else:
        # Fallback: combine all paragraph texts
        paragraphs = soup.find_all('p')
        main_text = "\n\n".join([p.get_text(strip=True) for p in paragraphs if len(p.get_text(strip=True)) > 20])

    return {
        "url": url,
        "title": title.strip(),
        "body": main_text.strip()
    }

if __name__ == "__main__":
    test_url = "https://example.com"
    content = fetch_content(test_url)
    if content:
        print(f"Title: {content['title']}")
        print(f"Body snippet: {content['body'][:200]}...")
