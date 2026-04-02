from google import genai
import os
import datetime
from dotenv import load_dotenv

load_dotenv()

def generate_blog_post(crawled_content, additional_instructions=""):
    """
    Generates a blog post in Markdown format using the Gemini API (google-genai SDK).
    Auto-tagging is based on the content of the post.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY not found in .env")
        return None

    client = genai.Client(api_key=api_key)

    prompt = f"""
당신은 최고 수준의 테크니컬 SEO 전문가이자, AEO/GEO 알고리즘 평가자, 그리고 전문 카피라이터입니다.
아래의 정보를 바탕으로 SEO, AEO, GEO 영역에서 각각 70점 이상을 획득할 수 있는 고품질 블로그 원고를 작성하십시오.

### 📄 수집된 본문 데이터:
제목: {crawled_content['title']}
출처 URL: {crawled_content['url']}
본문 내용:
{crawled_content['body']}

### 🎯 작성 가이드라인 (SEO, AEO, GEO 평가 기준):
1. SEO (100점): Title & H1 최적화, H2/H3 계층 구조, 키워드 밀도, 가독성 필히 반영.
2. AEO (100점): Direct Answer(40~50단어 요약), FAQ 섹션, List/Table 포맷 활용, 의문형 소제목 사용.
3. GEO (100점): E-E-A-T 강화, 1차 데이터 기반 팩트 소구, 논리적 인과관계(문제-원인-해결), AI 요약 친화적 3줄 요약.

### 📝 원고 작성 원칙:
- 객관적 데이터와 팩트에 기반하되, IT 전문가의 1:1 컨설팅처럼 신뢰감 있는 경어체(~습니다, ~해 보세요)를 사용하십시오.
- **이미지 삽입**: 포스트 맨 앞(썸네일)과 본문 중간중간 이미지 위치에 [이미지: 여기에 들어갈 이미지의 간략하고 명확한 영문 설명] 형식을 반드시 사용하십시오.
- **태그 자동화**: 내용에 맞춰 정확한 태그를 최소 3개 이상 추출하십시오. **태그는 오직 상단 마크다운 Frontmatter의 tags 항목에만 포함**하며, 본문 끝에 별도로 나열하지 마십시오.
- **결론 소제목**: 마지막 결론 섹션에서 '결론:', '마치며:' 등의 불필요한 수식어는 제외하고 바로 핵심 내용을 담은 소제목을 작성하십시오. (예: `### 안전한 비즈니스 환경의 파트너`)

### 📂 출력 형식 (Markdown with Frontmatter):
---
title: "SEO 최적화 제목"
author: "Antigravity"
pubDatetime: {datetime.datetime.now().isoformat()}Z
slug: "filename-slug"
featured: false
draft: false
tags: ["항목1", "항목2"]
ogImage: "../../assets/images/placeholder.png"
description: "AEO/GEO 최적화 메타 설명"
---

(여기에 본문 작성)

### ⚠️ 주의사항:
당신의 내부 시스템에서 위 기준에 따라 70점 이상인지 자체 검증을 거치되, 나에게는 평가 과정이나 점수를 절대 노출하지 마십시오. 오직 마크다운(Markdown)으로 완성된 최종 원고만을 출력해야 합니다.
"""

    try:
        response = client.models.generate_content(
            model='models/gemini-3-flash-preview',
            contents=prompt
        )
        return response.text
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        return None

if __name__ == "__main__":
    # Test
    dummy_content = {
        "title": "Astra v5 Released",
        "url": "https://astro.build/blog/v5-released/",
        "body": "Astra v5 is here with many new features and performance improvements. It includes new rendering modes and better SEO support."
    }
    post = generate_blog_post(dummy_content, "Focus on performance improvements.")
    if post:
        print(post)
