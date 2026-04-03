import os
from datetime import datetime, timedelta

def generate_posts():
    langs = ["ko", "en", "cn", "jp"]
    categories = ["posts", "haionnet"]
    base_dir = "src/data/blog"
    
    titles = {
        "ko": {"posts": "테스트 포스트 {}: {}", "haionnet": "하이온넷 소식 {}: {}"},
        "en": {"posts": "Test Post {}: {}", "haionnet": "Haionnet News {}: {}"},
        "cn": {"posts": "测试文章 {}: {}", "haionnet": "Haionnet 新闻 {}: {}"},
        "jp": {"posts": "テストポスト {}: {}", "haionnet": "ハイオンネットニュース {}: {}"}
    }
    
    topics = [
        "AI 기술의 미래",
        "사이버 보안 가이드",
        "클라우드 컴퓨팅 트렌드",
        "네트워크 가속화 기술"
    ]
    
    topics_en = ["Future of AI", "Cyber Security Guide", "Cloud Computing Trends", "Network Acceleration"]
    topics_cn = ["AI 技术的未来", "网络安全指南", "云计算趋势", "网络加速技术"]
    topics_jp = ["AI技術の未来", "サイバーセキュリティガイド", "クラウドコンピューティングのトレンド", "ネットワーク加速技術"]
    
    topic_map = {
        "ko": topics,
        "en": topics_en,
        "cn": topics_cn,
        "jp": topics_jp
    }
    
    # Current time in KST (2026-04-03 10:30 approx)
    # Use UTC for frontmatter
    start_time = datetime(2026, 4, 3, 1, 30, 0)
    
    for lang in langs:
        for cat in categories:
            cat_dir = os.path.join(base_dir, lang, cat)
            os.makedirs(cat_dir, exist_ok=True)
            
            for i in range(1, 5):
                topic = topic_map[lang][i-1]
                title = titles[lang][cat].format(i, topic)
                slug = f"test-{lang}-{cat}-{i}"
                pub_time = (start_time - timedelta(hours=i + (langs.index(lang) * 4) + (categories.index(cat) * 16))).strftime("%Y-%m-%dT%H:%M:%S.000Z")
                
                content = f"""---
title: "{title}"
author: "Antigravity"
pubDatetime: {pub_time}
slug: "{slug}"
featured: {str(i == 1).lower()}
draft: false
tags: ["test", "{lang}", "{cat}"]
ogImage: "../../../../assets/images/test-{i}.png"
description: "이것은 {lang} 언어의 {cat} 카테고리에 대한 테스트 포스트 {i}번입니다. {topic}에 대한 내용을 담고 있습니다."
---

## {title}

이 내용은 테스트를 위해 생성된 본문입니다. {lang} 언어로 작성되었으며, 블로그의 레이아웃과 다국어 기능이 정상적으로 작동하는지 확인하기 위한 용도입니다.

### {topic}에 대하여

{topic}은 현대 기술 생태계에서 매우 중요한 위치를 차지하고 있습니다. 본 포스트는 해당 주제에 대한 기초적인 정보를 제공하며, 사이트의 디자인과 네비게이션이 올바르게 구성되었는지 테스트합니다.

![Test Image](../../../../assets/images/test-{i}.png)

---
마침.
"""
                file_path = os.path.join(cat_dir, f"{slug}.md")
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(content)
                print(f"Generated: {file_path}")

if __name__ == "__main__":
    generate_posts()
