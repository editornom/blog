from google import genai
from google.api_core import exceptions
from api_utils import gemini_retry, gemini_limiter
import os
import datetime
import re
from dotenv import load_dotenv
import json
from pydantic import BaseModel, Field

import sys

load_dotenv()

if sys.platform == "win32":
    # Ensure terminal can handle UTF-8/Emojis on Windows
    sys.stdout.reconfigure(encoding='utf-8')

class BlogPostSchema(BaseModel):
    title: str = Field(description="최적화된 제목")
    content: str = Field(description="마크다운 형식의 본문 내용")

def generate_blog_post(crawled_content, folder="posts", additional_instructions="", keyword=""):
    """
    Generates a blog post using the Gemini API with Structured Outputs (JSON) and Keyword Density validation.
    Returns:
        tuple: (markdown_draft, density_warning_message)
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY not found in .env")
        return None, None

    client = genai.Client(api_key=api_key)

    primary_topic = keyword if keyword else crawled_content['title']

    data_block = f"""
### 🎯 핵심 타겟 키워드:
{primary_topic}

### 📄 수집된 본문 데이터:
출처 URL: {crawled_content['url']}
본문 내용(수집된 여러 소스 통합):
{crawled_content['body']}
"""

    utc_now = datetime.datetime.now(datetime.timezone.utc)
    seoul_tz = datetime.timezone(datetime.timedelta(hours=9))
    seoul_now = datetime.datetime.now(seoul_tz)
    pub_time = seoul_now - datetime.timedelta(minutes=10)
    
    print(f"--- Time Synchronization ---")
    print(f"Current UTC:   {utc_now.strftime('%Y-%m-%d %H:%M:%S')} Z")
    print(f"Current Seoul: {seoul_now.strftime('%Y-%m-%d %H:%M:%S')} +09:00")
    print(f"Publication:   {pub_time.strftime('%Y-%m-%d %H:%M:%S')} +09:00 (Buffered)")
    print(f"----------------------------")

    if folder == "glossary":
        prompt = f"""
# ROLE
당신은 IT/마케팅/웹 기술 분야의 '수석 백과사전 편집자(Wiki Contributor)'이자 테크니컬 라이터입니다. 당신의 목표는 독자에게 최고 수준의 객관성과 구조적 완결성을 갖춘 위키 문서(Glossary)를 마크다운 형식으로 제공하는 것입니다.

{data_block}

# OUTPUT STRUCTURE (엄격 준수)
본문(content)은 반드시 아래 6단계를 포함해야 합니다.
1. 위키 요약표: 영문명, 한글명, 약어, 관련 기술을 마크다운 표(Table)로 작성.
2. 개요 (TL;DR): 150자 내외의 명확하고 건조한 백과사전식 정의.
3. 등장 배경 (Background): 이 기술/용어가 왜 필요해졌고, 어떤 문제를 해결하기 위해 등장했는지 서술.
4. 주요 특징 및 원리 (Key Features): 2~3가지 핵심 특징을 글머리 기호로 요약.
5. 유사 개념과의 비교 (VS): 가장 헷갈리는 유사 개념 1개를 선정해 결정적 차이점 서술.
6. 실무 적용 및 연관 용어: 실제 활용 사례 1가지와 연관 용어 3가지.

# TONE & STYLE
- '위키백과'처럼 극도로 객관적이고 건조한 문체(~입니다, ~합니다 체 유지)를 사용하십시오.
- 감정적 표현이나 불필요한 수식어를 완전히 배제하십시오.

- **이미지 삽입**: 본문(content) 내에는 이미지를 넣지 마십시오. 오직 **본문 시작 직전(위키 요약표 바로 위)**에 해당 용어를 상징하는 **[이미지: 여기에 들어갈 이미지의 간략하고 명확한 영문 설명]** 형식을 딱 한 번만 삽입하십시오. (주의: 프롬프트 작성 시 이미지 내에 텍스트, 인포그래픽, 표가 포함되지 않도록 시각적 묘사 위주로 작성하십시오.)

### ⚠️ 주의사항:
당신의 내부 시스템에서 평가 과정이나 메타 코멘트를 절대 노출하지 마십시오. 본문(content) 내부에 <script> 태그나 JSON-LD(application/ld+json) 코드를 절대 포함하지 마십시오. 요구된 JSON 스키마 필드만 엄격히 반환하십시오.
"""
    else:
        prompt = f"""
# 페르소나 (Persona)
당신은 국내외 IT 트렌드를 담백하고 객관적인 문체로 분석하는 10년 차 IT 전문 칼럼니스트 'editornom'입니다. 
제목(title) 작성 시 **[EDITORNOM의 시선]**이나 **[Deep Dive]**와 같은 작위적인 수식어나 접두사/접미사를 절대 붙이지 마십시오. 오직 정제된 핵심 한 문장으로만 제목을 작성하십시오. 
억지로 전문가 행세를 하거나 과장된 수사를 피하고, 독자가 읽기 편안한 실용적인 통찰을 제공하세요.

{data_block}

# 핵심 작성 원칙 (Writing Principles)
1. 말투: "~입니다", "~습니다" 문어체를 기본으로 하되, 지적이고 친근한 '해요체'를 섞어 사용하세요.
2. 금지어 및 금지 패턴 (Negative Prompt): 
   - 거창하고 작위적인 표현 절대 금지.
   - [Deep Dive], [The Mechanism] 같은 불필요한 영문 소제목 병기 금지.
   - **강조 남발 금지 (중요)**: 문장 마다 주요 키워드나 명사에 볼드체(`**텍스트**`)를 입히는 'AI 특유의 강조 습관'을 절대 피하십시오. 
3. 강조 가이드라인 (Smart Emphasis): 
   - 강조는 전체 글에서 **최초 등장하는 핵심 용어**에 대해 단 1~2회만 사용하세요. 
   - 조사(~는, ~를)까지 볼드체에 포함하지 마십시오. 
   - "A는 **B**이다"와 같은 인위적인 강조 패턴보다, 문맥의 흐름에 따라 꼭 필요한 정보에만 자연스럽고 드물게 볼드체를 사용하십시오. 사람이 직접 쓴 칼럼처럼 강조를 아끼세요.
4. 고유명사 강제: 외국 IT 기업이나 서비스명 표기 시 오류를 주의하세요.
5. 분량 및 깊이: 공백 제외 2,500자 이상의 심층 분석 글로 작성하며, 일반인이 모르는 기술적 디테일을 최소 2개 이상 자연스럽게 녹여내세요.

# 칼럼 구조 (Logical Structure)
## [작성 지침 - 절대 준수]
1. 모든 포스팅의 중심 주제는 반드시 **"{primary_topic}"**이어야 합니다. 
2. 제공된 소스 자료에 하드웨어 장비 정보가 많더라도, 이를 주인공으로 삼지 마세요.
3. 문단의 가독성을 위해 적절한 소제목(H2, H3)과 불릿 포인트를 활용하세요.
4. 전문적인 톤앤매너를 유지하세요.
5. 서론 -> 본문 심층 분석 -> 전망 -> 결론 구조.

# GEO & E-E-A-T 강화 요소
- 인용구: 중심 메시지를 위한 인용구(Blockquote) 1~2개 배치.
- 데이터 시각화 지시: 본문 전체에서 가장 중요한 맥락을 보여줄 수 있는 지점 **2~3곳**을 자유롭게 선정하여 에디토리얼 이미지 프롬프트를 삽입하십시오. (형식: **[이미지: 영어로 된 상세한 Editorial Style 생성 프롬프트]**). 
- **이미지 프롬프트 주의사항**: 이미지 내에 글자(Text), 인포그래픽(Infographic), 표(Table), 차트(Chart) 등이 절대 포함되지 않도록 시각적이고 은유적인 묘사 위주로 작성하십시오. AI가 생성한 가짜 데이터가 노출되는 것을 방지해야 합니다.

### ⚠️ 주의사항:
본문(content) 내부에 <script> 태그나 JSON-LD(application/ld+json) 코드를 절대 포함하지 마십시오. 이는 시스템 오류를 유발하며 절대 허용되지 않습니다. 오직 JSON 스키마에 정의된 마크다운 데이터만 출력해야 합니다.
- 이미지 삽입 시 반드시 `[이미지: 영어 프롬프트]` 형식을 유지하세요. `![]()`와 같은 마크다운 이미지 문법을 미리 사용하지 마십시오.
"""

    if additional_instructions:
        prompt += f"\n### 추가 지시사항:\n{additional_instructions}\n"

    keyword_lower = primary_topic.lower()
    max_attempts = 3 # Original attempt + 2 retries
    density_warning = None
    final_draft_data = None

    for attempt in range(max_attempts):
        @gemini_retry
        def call_api(current_prompt):
            gemini_limiter.consume()
            return client.models.generate_content(
                model='models/gemini-3-flash-preview',
                contents=current_prompt,
                config={
                    'response_mime_type': 'application/json',
                    'response_schema': BlogPostSchema
                }
            )

        try:
            print(f"  [Generator] API 호출 중... (시도 {attempt+1}/{max_attempts})")
            response = call_api(prompt)
            data = json.loads(response.text)
            
            content_text = data.get("content", "")
            
            # 🌟 [개선] 한국어 맞춤형 글자 수 기반 밀도 검증 (Action Plan 3)
            # 영어식 띄어쓰기(split)는 한국어 조사 결합 등으로 인해 정확도가 떨어지므로 글자 수로 계산합니다.
            clean_content = re.sub(r'\s+', '', content_text) # 공백 제거 본문
            total_chars = len(clean_content)
            
            if total_chars > 0:
                keyword_count = content_text.lower().count(keyword_lower)
                keyword_len = len(re.sub(r'\s+', '', keyword_lower))
                actual_density = (keyword_count * keyword_len) / total_chars
            else:
                actual_density = 0

            # 🌟 [GLOSSARY] 용어 사전은 밀도 체크를 생략하고 즉시 통과
            if folder == "glossary":
                print(f"  ✅ [Glossary Mode] 키워드 밀도 체크를 생략합니다.")
                final_draft_data = data
                density_warning = None
                break

            min_density = 0.01 # 하한선 1%
            max_density = 0.03 # 상한선 3% (검색 엔진 어뷰징 방지 마지노선)
            
            if min_density <= actual_density <= max_density:
                print(f"  ✅ 키워드 밀도 충족: {actual_density*100:.2f}% (안전 구간)")
                final_draft_data = data
                density_warning = None # Valid
                break # 성공 시 루프 종료
            elif actual_density > max_density:
                warning_msg = f"⚠️ 키워드 밀도 초과 (실제: {actual_density*100:.2f}%, 상한: 3%). 어뷰징(도배) 위험!"
                print(f"  {warning_msg}")
                if attempt < max_attempts - 1:
                    print(f"  🔄 밀도가 너무 높습니다. 밀도를 낮추기 위해 수정을 요청합니다.")
                    prompt += f"\n\n[SYSTEM Feedback] 이전 원고에서 타겟 키워드('{primary_topic}')가 너무 과도하게 반복되었습니다(키워드 스터핑). 검색 엔진 패널티를 피하기 위해 대명사를 활용하거나 생략하여 키워드 노출 빈도를 절반 이하로 줄이고, 자연스럽게 다듬어 주세요 (목표 밀도 1.5%)."
                    continue # 🚨 [중요] 상한선 초과 시 종료하지 않고 재시도
                final_draft_data = data
                density_warning = warning_msg
            else:
                warning_msg = f"⚠️ 키워드 밀도 1% 미달 (실제: {actual_density*100:.2f}%)"
                print(f"  {warning_msg}")
                if attempt < max_attempts - 1:
                    prompt += f"\n\n[SYSTEM Feedback] 이전 생성된 원고에서 타겟 키워드('{primary_topic}')의 사용 빈도가 너무 적습니다. 문맥을 해치지 않는 선에서 자연스럽게 키워드를 더 배치하여 밀도를 높여주세요 (목표 1.5%)."
                    continue # 미달 시 재시도
                final_draft_data = data
                density_warning = warning_msg

        except Exception as e:
            print(f"❌ Gemini API 오류: {e}")
            if attempt == max_attempts - 1:
                return None, None

    if final_draft_data:
        return final_draft_data, density_warning
    
    return None, None

if __name__ == "__main__":
    dummy_content = {
        "title": "Astra v5 Released",
        "url": "https://astro.build/blog/v5-released/",
        "body": "Astra v5 is here with many new features and performance improvements. It includes new rendering modes and better SEO support."
    }
    
    post, warning = generate_blog_post(
        crawled_content=dummy_content, 
        folder="posts", 
        additional_instructions="Focus on performance improvements."
    )
    
    if post:
        print("=== GENERATED DRAFT ===")
        print(post)
        if warning:
            print("\nWARNING: " + warning)