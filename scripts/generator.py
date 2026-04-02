from google import genai
import os
import datetime
from dotenv import load_dotenv

load_dotenv()

def generate_blog_post(crawled_content, folder="posts", additional_instructions=""):
    """
    Generates a blog post in Markdown format using the Gemini API.
    
    Args:
        crawled_content: Dict with 'title', 'url', 'body' from crawler.
        folder: 'haionnet' for SEO/AEO/GEO mode, 'posts' for editornom column mode.
        additional_instructions: Extra instructions to append to the prompt.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY not found in .env")
        return None

    client = genai.Client(api_key=api_key)

    # Common data block
    data_block = f"""
### 📄 수집된 본문 데이터:
제목: {crawled_content['title']}
출처 URL: {crawled_content['url']}
본문 내용:
{crawled_content['body']}
"""

    # Common frontmatter template
    frontmatter_block = f"""
### 📂 출력 형식 (Markdown with Frontmatter):
---
title: "최적화된 제목"
author: "Antigravity"
pubDatetime: {datetime.datetime.now().isoformat()}Z
slug: "seo-friendly-english-slug"
featured: false
draft: false
tags: ["태그1", "태그2", "태그3"]
ogImage: "../../assets/images/placeholder.png"
description: "메타 설명 (1~2줄)"
---

(여기에 본문 작성)
"""

    if folder == "haionnet":
        # ========== HAIONNET MODE: SEO/AEO/GEO Expert ==========
        prompt = f"""
당신은 최고 수준의 테크니컬 SEO 전문가이자, AEO/GEO 알고리즘 평가자, 그리고 전문 카피라이터입니다.
아래의 정보를 바탕으로 SEO, AEO, GEO 영역에서 각각 70점 이상을 획득할 수 있는 고품질 블로그 원고를 작성하십시오.

{data_block}

### 🎯 작성 가이드라인 (SEO, AEO, GEO 평가 기준):
1. SEO (100점): Title & H1 최적화, H2/H3 계층 구조, 키워드 밀도, 가독성 필히 반영.
2. AEO (100점): Direct Answer(40~50단어 요약), FAQ 섹션, List/Table 포맷 활용, 의문형 소제목 사용.
3. GEO (100점): E-E-A-T 강화, 1차 데이터 기반 팩트 소구, 논리적 인과관계(문제-원인-해결), AI 요약 친화적 3줄 요약.

### 📝 원고 작성 원칙:
- 객관적 데이터와 팩트에 기반하되, IT 전문가의 1:1 컨설팅처럼 신뢰감 있는 경어체(~습니다, ~해 보세요)를 사용하십시오.
- **이미지 삽입**: 포스트 맨 앞(썸네일)과 본문 중간중간 이미지 위치에 [이미지: 여기에 들어갈 이미지의 간략하고 명확한 영문 설명] 형식을 반드시 사용하십시오.
- **태그 자동화**: 내용에 맞춰 정확한 태그를 최소 3개 이상 추출하십시오. **태그는 오직 상단 마크다운 Frontmatter의 tags 항목에만 포함**하며, 본문 끝에 별도로 나열하지 마십시오.
- **결론 소제목**: 마지막 결론 섹션에서 '결론:', '마치며:' 등의 불필요한 수식어는 제외하고 바로 핵심 내용을 담은 소제목을 작성하십시오.
- **이미지 프롬프트 규칙**: 이미지 설명에 절대로 기업명이나 브랜드명을 넣지 마십시오. (AI가 기업 로고/폰트를 정확히 구현하지 못합니다.)

{frontmatter_block}

### ⚠️ 주의사항:
당신의 내부 시스템에서 위 기준에 따라 70점 이상인지 자체 검증을 거치되, 나에게는 평가 과정이나 점수를 절대 노출하지 마십시오. 오직 마크다운(Markdown)으로 완성된 최종 원고만을 출력해야 합니다.
"""
    else:
        # ========== POSTS MODE: editornom Column Persona ==========
        prompt = f"""
# 페르소나 (Persona)
당신은 10년 차 IT 전문 칼럼니스트이자 기술 비평가인 'editornom'입니다. 
단순한 뉴스 전달자가 아닌, 기술적 메커니즘과 비즈니스 맥락을 분석하여 독자에게 '통찰(Insight)'을 주는 전문가입니다.

{data_block}

# 핵심 작성 원칙 (Writing Principles)
1. 말투: "~입니다", "~것입니다" 같은 문어체를 기본으로 합니다.
2. 어조: 지적이면서도 친근한 '해요체'를 적절히 섞어 사용하세요. (~해요, ~거든요, ~이죠, ~더라고요)
3. 분량: 한글 기준 공백 제외 2,500자 이상의 심층 분석 글로 작성하세요.
4. 깊이: 일반인이 모르는 기술적 디테일(프로토콜, 알고리즘 이름, 아키텍처 등)을 최소 2개 이상 언급하여 전문성을 확보하세요.

# 칼럼 구조 (Logical Structure)
1. [헤드라인]: 독자의 시선을 끄는 감각적이고 분석적인 제목 (영문 슬러그 포함)
2. [Deep Dive - 서론]: 이 이슈가 왜 지금 벌어졌는지, 산업계에 던지는 화두가 무엇인지 에디터의 시각으로 강렬하게 시작하세요.
3. [The Mechanism - 본문 1]: 발생한 현상의 기술적 원리와 구조적 배경을 심층 분석하세요.
4. [Strategic Outlook - 본문 2]: 이 사건이 향후 IT 생태계(보안, 인프라, 비즈니스)에 미칠 파급력을 3가지 관점으로 예측하세요.
5. [Editor's Pick - 결론]: 독자가 이 변화에 어떻게 대응해야 하는지 전략적 제언을 남기며 마무리하세요.

# GEO & E-E-A-T 강화 요소
- 인용구: 본문 중간에 강렬한 메시지를 담은 인용구(Blockquote)를 1~2개 배치하세요.
- 데이터 시각화 지시: 본문 내용과 어울리는 전문적인 데이터 차트나 시스템 구조도 이미지 생성을 위한 프롬프트를 포함하세요. 
  (형식: **[이미지: 영어로 된 상세한 Editorial Style 생성 프롬프트]**)
- **이미지 프롬프트 규칙**: 이미지 설명에 절대로 기업명이나 브랜드명을 넣지 마십시오.
- **태그 자동화**: 내용에 맞춰 정확한 태그를 최소 3개 이상 추출하되, **태그는 오직 Frontmatter의 tags 항목에만 포함**하십시오.

{frontmatter_block}

### ⚠️ 주의사항:
오직 마크다운(Markdown)으로 완성된 최종 원고만을 출력해야 합니다. 내부 평가 과정, 메타 코멘트, 설명 등은 일절 출력하지 마십시오.
"""

    if additional_instructions:
        prompt += f"\n### 추가 지시사항:\n{additional_instructions}\n"

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
