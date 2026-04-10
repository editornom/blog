import os
import sys
from headline_crawler import generate_daily_headlines_file
from trend_catcher import get_daily_topic_from_file
from search_expert import deep_search_and_filter

def test_up_to_search():
    print("🚀 [TEST] Running pipeline up to SearchExpert...")
    
    # 1. RSS Crawl
    daily_file = generate_daily_headlines_file("list.txt")
    if not daily_file:
        print("❌ Headline crawling failed.")
        return

    # 2. Trend Catching
    keyword = get_daily_topic_from_file(daily_file)
    if not keyword:
        print("❌ Trend catching failed.")
        return
    
    print(f"✨ Selected Keyword: {keyword}")

    # 3. Deep Search & Filter
    top_urls = deep_search_and_filter(keyword, num_results=100)
    
    if top_urls:
        print("\n" + "="*50)
        print("🏆 Final Selected 10 URLs for Blogging:")
        print("="*50)
        for i, url in enumerate(top_urls):
            print(f"[{i+1}] {url}")
        print("="*50)
    else:
        print("❌ No URLs selected.")

if __name__ == "__main__":
    # Ensure UTF-8 for Windows
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding='utf-8')
    test_up_to_search()
