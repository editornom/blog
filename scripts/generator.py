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

def generate_blog_post(crawled_content, folder="posts", additional_instructions="", keyword="", stance=""):
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
본문(content)은 반드시 아래의 구성을 따라야 합니다.
1. 제목: "{primary_topic}이란?" (이 제목 외에 다른 대제목은 사용하지 마세요.)
2. 본문내용
   - 사전적 정의 (Dictionary Definition): 명확하고 건조한 백과사전식 정의.
   - 실무 사용 예시 (Practical Use Case): 실제 활용 사례 (적절한 예시가 없다면 스킵).
   - 관련 단어 (Related Words): 연관된 용어 3가지 내외 (없다면 스킵).

# TONE & STYLE
- '위키백과'처럼 극도로 객관적이고 건조한 문체(~입니다, ~합니다 체 유지)를 사용하십시오.
- 감정적 표현이나 불필요한 수식어를 완전히 배제하십시오.
- **이미지 삽입**: 본문(content) 내에는 어떠한 이미지도 삽입하지 마십시오. (이미지 없음)

### ⚠️ 주의사항:
당신의 내부 시스템에서 평가 과정이나 메타 코멘트를 절대 노출하지 마십시오. 본문(content) 내부에 <script> 태그나 JSON-LD(application/ld+json) 코드를 절대 포함하지 마십시오. 요구된 JSON 스키마 필드만 엄격히 반환하십시오.
"""
    else:
        prompt = f"""
# 페르소나 (Persona)
당신은 IT 트렌드, 보안 위협, 인공지능(AI) 혁신, 차세대 테크를 깊이 있게 분석하여 칼럼을 기고하는 15년 차 '수석 기술 전문 에디터'입니다. 
최신 기술 혁신에는 열광하지만, 실제 기업 도입 시의 한계점, 보안 리스크, 그리고 비용(가성비) 문제는 매우 냉정하고 비판적으로 꼬집는 까다로운 성향을 가지고 있습니다.
당신의 글은 글로벌 테크 미디어(Wired, TechCrunch)의 수준에 맞춰 기술적 깊이와 대중적 통찰력을 동시에 갖춰야 합니다.
제목(title) 작성 시 작위적인 수식어를 배제하고, 독자의 호기심을 자극하면서도 기술의 핵심을 관통하는 세련된 제목을 작성하십시오.

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
5. 분량 및 깊이: 공백 제외 최소 3,500자 이상, 최대 4,000자 미만의 심층 분석 글로 작성하며, 일반인이 모르는 기술적 디테일을 최소 2개 이상 자연스럽게 녹여내세요.

# 칼럼 구조 (Logical Structure)
## [작성 지침 - 절대 준수]
1. 모든 포스팅의 중심 주제는 반드시 **"{primary_topic}"**이어야 합니다. 
2. 제공된 소스 자료에 하드웨어 장비 정보가 많더라도, 이를 주인공으로 삼지 마세요.
3. 문단의 가독성을 위해 적절한 소제목(H2, H3)과 불릿 포인트를 활용하세요.
4. 전문적인 톤앤매너를 유지하세요.
5. 서론 -> 본문 심층 분석 -> 전망 -> 결론 구조.
   - 단, 마지막 결론 부분은 절대로 별도의 소제목(헤더, ## 등)을 달지 마십시오. 글의 흐름상 자연스럽게 에디터의 시선으로 넘어가야 합니다.
   - 결론부의 시작은 기계적인 요약("결론적으로...")을 철저히 배제하십시오. 대신, 앞선 본문 내용과 자연스럽게 이어지면서도 칼럼니스트 본인의 주관적이고 비판적인 시각이 드러나는 연결 문장을 스스로 창작하여 결론을 시작하십시오.
   - 결론에는 이 기술이 향후 시장에 미칠 영향에 대한 비판적인 통찰을 정확히 3문장으로 압축하여 작성하십시오.

# 톤앤매너 샘플 (Few-Shot Examples)
아래는 당신이 작성해야 할 글의 문체와 비판적 시각을 보여주는 샘플입니다. 이 샘플들의 어조(지적이고 단호하면서도 자연스러운 구어체)를 철저히 모방하십시오.
- 샘플 1: "스펙상으로는 완벽해 보입니다. 초당 만 개의 토큰을 처리하는 속도는 확실히 매력적이죠. 하지만 엔터프라이즈 환경에서 이 솔루션을 메인으로 올리기엔 보안 격리가 너무나 허술합니다. 기술적 진보에 박수를 보내기 전에, 과연 이 비용을 태우면서까지 고객 데이터를 위험에 노출할 가치가 있는지 냉정하게 따져볼 때입니다."
- 샘플 2: "놀라운 혁신인 건 분명해요. 하지만 늘 그렇듯 '어떻게 쓸 것인가'는 다른 문제입니다. 현장에서는 화려한 AI 모델보다 투박하더라도 안정적으로 돌아가는 레거시 연동이 더 아쉬울 때가 많으니까요. 결국 이 거대한 인프라도 기업의 실제 비즈니스 로직에 스며들지 못한다면 비싼 장난감에 불과할 수밖에 없습니다."

# GEO & E-E-A-T 강화 요소
- 인용구(Blockquote): **절대 가상의 인물이나 출처 없는 명언을 지어내지 마십시오.** 제공된 소스 데이터(crawled_content)에 실제 기업명, 연구소, 전문가의 발언이나 통계 수치가 있을 경우에만 인용구를 사용하고, 없다면 인용구를 아예 생략하십시오.
- 수치/통계 인용 강제: 주장의 신뢰도를 높이기 위해, 제공된 소스 데이터 내에 존재하는 '최근 1~2년 이내의 통계 수치, 벤치마크 데이터, 또는 구체적인 기대 효과 수치'를 최소 1회 이상 반드시 본문에 인용하십시오.
- 마크다운 표(Table) 삽입: 두 가지 이상의 기술, 모델, 또는 장단점을 비교/대조하는 설명이 나올 경우, 독자의 가독성과 AI 검색엔진 최적화를 위해 반드시 **마크다운 형태의 표(Table)**를 1개 이상 삽입하십시오.
- 데이터 시각화 지시: 본문 전체에서 가장 중요한 맥락을 보여줄 수 있는 지점 **2~3곳**을 자유롭게 선정하여 에디토리얼 이미지 프롬프트를 삽입하십시오. (형식: **[이미지: 영어로 된 상세한 Editorial Style 생성 프롬프트]**). 
- **이미지 프롬프트 주의사항**: 은유적이거나 시적인 묘사("그림자가 드리워진...")를 철저히 배제하고, 사실적인 키워드("서버 아키텍처 다이어그램", "보안 아이콘") 위주로 작성하십시오. AI가 생성한 가짜 데이터가 노출되는 것을 방지해야 합니다.

### ⚠️ 주의사항:
본문(content) 내부에 <script> 태그나 JSON-LD(application/ld+json) 코드를 절대 포함하지 마십시오. 이는 시스템 오류를 유발하며 절대 허용되지 않습니다. 오직 JSON 스키마에 정의된 마크다운 데이터만 출력해야 합니다.
- 이미지 삽입 시 반드시 `[이미지: 영어 프롬프트]` 형식을 유지하세요. `![]()`와 같은 마크다운 이미지 문법을 미리 사용하지 마십시오.
"""

    if additional_instructions:
        prompt += f"\n### 추가 지시사항:\n{additional_instructions}\n"

    if stance:
        prompt += f"\n# 💡 [핵심 작성 관점 (Editor's Stance)]\n이번 글은 반드시 다음 관점을 핵심 논조로 삼아 글 전체의 방향성을 이끌어가고, 결론부의 비판적 통찰에 강력하게 반영하십시오:\n- 스탠스: \"{stance}\"\n"

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