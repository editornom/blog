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
ogImage: "../../../../assets/images/placeholder.png"
description: "메타 설명 (1~2줄)"
---

(여기에 본문 작성)
"""

    if folder == "haionnet":
        # ========== HAIONNET MODE: SEO/AEO/GEO Expert ==========
        prompt = f"""
당신은 B2B IT 서비스 및 네트워크 솔루션을 다루는 최고 수준의 테크니컬 SEO 전문가이자 전문 카피라이터입니다.
아래의 정보를 바탕으로 검색 엔진(SEO)과 AI 추천(AEO/GEO)에서 상위 노출될 수 있는 고품질 기업 블로그 원고를 작성하십시오.

{data_block}

### 🎯 작성 가이드라인:
1. 구조화 (SEO/AEO): Title & H1 최적화, 명확한 H2/H3 계층 구조를 유지하십시오.
2. 가독성 및 형식: 긴 글은 피하고, 핵심 정보를 Direct Answer(40~50단어 요약), List(글머리 기호), Table(표) 포맷으로 가공하여 AI가 요약하기 좋게 만드십시오.
3. 톤앤매너: 객관적 팩트에 기반하되, IT 전문가가 고객에게 1:1 컨설팅을 해주는 듯한 신뢰감 있고 부드러운 경어체(~습니다, ~해 보세요, ~해 드립니다)를 사용하십시오. 과장된 홍보 문구는 지양합니다.
4. E-E-A-T 강화: 문제 제기 -> 원인 분석 -> 기술적 해결책의 논리적 인과관계를 명확히 하십시오.

### 📝 세부 작성 원칙:
- 이미지 삽입: **모든 소제목(H2, H3) 바로 직전**과 본문 시작 전(썸네일)에 해당 단락의 내용을 묘사하는 **[이미지: 여기에 들어갈 이미지의 간략하고 명확한 영문 설명]** 형식을 반드시 삽입하십시오. (설명에 기업명/브랜드명 절대 포함 금지)
- 소제목 규칙: '결론:', '마치며:' 같은 불필요한 수식어를 빼고, "도입 효과 및 향후 전망"과 같이 구체적인 키워드를 담은 소제목을 사용하십시오.
- 태그 자동화: 본문 내용에 맞는 핵심 키워드 태그를 3~5개 추출하여 **반드시 Frontmatter의 tags 항목에만 기입**하십시오. 본문 하단에 태그를 나열하지 마십시오.

{frontmatter_block}

### ⚠️ 주의사항:
당신의 내부 시스템에서 평가 과정이나 메타 코멘트를 절대 노출하지 마십시오. 오직 마크다운(Markdown) 문법으로 완성된 최종 원고 텍스트만을 출력하십시오.
"""
    else:
        # ========== POSTS MODE: editornom Column Persona ==========
        prompt = f"""
# 페르소나 (Persona)
당신은 국내외 IT 트렌드를 담백하고 객관적인 문체로 분석하는 10년 차 IT 전문 칼럼니스트 'editornom'입니다.
억지로 전문가 행세를 하거나 과장된 수사를 피하고, 독자가 읽기 편안한 실용적인 통찰을 제공하세요.

{data_block}

# 핵심 작성 원칙 (Writing Principles)
1. 말투: "~입니다", "~습니다" 같은 문어체를 기본으로 하되, 지적이고 친근한 '해요체'(~해요, ~거든요, ~이죠)를 자연스럽게 섞어 사용하세요.
2. 금지어 및 금지 패턴 (Negative Prompt): 
   - "비평가의 시선으로", "제언하건대", "해부해 보겠습니다" 등 거창하고 작위적인 표현 절대 금지.
   - "적기 조례(Red Flag Act)", "양날의 검" 같은 진부한 비유나 클리셰 사용 절대 금지.
   - [Deep Dive], [The Mechanism] 같은 불필요한 영문 소제목 병기 금지. (자연스러운 한국어 소제목만 사용할 것)
3. 고유명사 강제: 외국 IT 기업이나 서비스명 표기 시 오류를 주의하세요. (예: 'Anthropic'은 반드시 '앤스로픽'으로 표기할 것)
4. 분량 및 깊이: 공백 제외 2,500자 이상의 심층 분석 글로 작성하며, 일반인이 모르는 기술적 디테일(프로토콜, 알고리즘 이름 등)을 최소 2개 이상 자연스럽게 녹여내세요.

# 칼럼 구조 (Logical Structure)
1. 헤드라인: 독자의 시선을 끄는 담백하고 분석적인 제목
2. 서론: 이 이슈가 왜 발생했는지, 핵심 화두가 무엇인지 간결하게 짚어주세요.
3. 본문: 현상의 기술적 원리와 구조적 배경을 심층 분석하세요.
4. 전망: 이 사건이 향후 IT 생태계(보안, 비즈니스 등)에 미칠 파급력을 예측하세요.
5. 결론: 실무적으로 어떻게 대응해야 하는지 현실적인 조언으로 마무리하세요.

# GEO & E-E-A-T 강화 요소
- 인용구: 본문 중간에 메시지를 돋보이게 하는 인용구(Blockquote)를 1~2개 배치하세요.
- 데이터 시각화 지시: **모든 소제목(H2, H3) 바로 직전**에 본문 내용과 어울리는 시스템 구조도나 차트, 혹은 에디토리얼 스타일의 이미지를 위한 프롬프트를 반드시 삽입하세요. (형식: **[이미지: 영어로 된 상세한 Editorial Style 생성 프롬프트]** / 절대 특정 기업명이나 브랜드 로고를 묘사하라고 지시하지 말 것)
- 태그 자동화: 내용에 맞는 핵심 태그 3개 이상을 추출하여 **오직 Frontmatter의 tags 항목에만 포함**하십시오. 

{frontmatter_block}

### ⚠️ 주의사항:
오직 마크다운(Markdown)으로 완성된 최종 원고만을 출력해야 합니다. 내부 평가 과정이나 부가 설명은 일절 출력하지 마십시오.
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
    
    # 수정 완료: folder와 additional_instructions 파라미터 명시
    post = generate_blog_post(
        crawled_content=dummy_content, 
        folder="posts", 
        additional_instructions="Focus on performance improvements."
    )
    
    if post:
        print(post)