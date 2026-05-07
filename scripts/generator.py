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

class PlanningOutput(BaseModel):
    strategy: str = Field(description="페르소나, 목표, 차별화 요소 등 전략 요약")
    outline: str = Field(description="H1~H3 구조의 목차")
    expert_guidelines: str = Field(description="SEO/AEO/GEO 전문가를 위한 개별 지시사항")

class SpecialistOutput(BaseModel):
    seo_part: str = Field(description="SEO 최적화된 제목, 메타 디스크립션, 본문 요소")
    aeo_part: str = Field(description="AEO 최적화된 BLUF, FAQ, 구조화 데이터 요소")
    geo_part: str = Field(description="GEO 최적화된 데이터 밀도, 신뢰 신호, 표 요소")

class BlogPostSchema(BaseModel):
    title: str = Field(description="최종 완성된 제목")
    content: str = Field(description="마크다운 형식의 최종 완성된 본문")

def generate_blog_post_multi_agent(crawled_content, folder="posts", keyword="", stance="", schedule_type=None):
    """
    Generates a blog post using a Multi-Agent Orchestration pipeline:
    1. Planning Director: Strategy & Outline
    2. Specialist Trio (SEO/AEO/GEO): Optimized elements
    3. General Editor: Final consolidation and polishing
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY not found in .env")
        return None
        
    client = genai.Client(api_key=api_key)
    primary_topic = keyword if keyword else crawled_content['title']
    
    data_block = f"""
### 🎯 핵심 타겟 키워드:
{primary_topic}

### 📄 수집된 본문 데이터:
출처 URL: {crawled_content['url']}
본문 내용:
{crawled_content['body']}
"""

    # --- PHASE 1: Planning Director ---
    print(f"\n🏗️ [Phase 1] 기획국장: 전략 수립 및 목차 설계 중... (Schedule: {schedule_type if schedule_type else 'Manual'})")
    
    # Schedule-specific strategy enhancement
    schedule_strategy = ""
    if schedule_type in ["09_tech_news", "15_ai_news"]:
        schedule_strategy = "이 글은 '최신 뉴스 분석'입니다. 현재 발생하는 트렌드와 기술적 이슈가 지금 당장 업계와 사용자에게 미치는 '즉각적인 영향'과 '시의성'에 집중하여 전략을 수립하세요."
    elif schedule_type in ["12_tech_feature", "18_ai_feature"]:
        schedule_strategy = "이 글은 '심층 특집(Feature)' 기사입니다. 이 기술이나 사건이 갖는 '역사적 맥락'과 '기념비적 가치', 그리고 장기적으로 IT 생태계에 미친 '거대한 파장'을 분석하는 거시적인 관점에서 전략을 수립하세요."

    planning_prompt = f"""
너는 블로그 콘텐츠 전략의 사령탑인 '기획국장(Planning Director)'이다. 너의 임무는 단순한 키워드 나열이 아니라, 시장 데이터와 경쟁사 분석을 바탕으로 '필승의 글쓰기 전략'을 수립하는 것이다.

{data_block}

[지시사항]
1. {schedule_strategy if schedule_strategy else '시장 데이터와 페르소나를 분석하여 독보적인 전략을 수립하라.'}
2. H1~H3 구조의 목차를 설계하라.
3. SEO/AEO/GEO 전문가가 반드시 다루어야 할 핵심 논점을 정리하라.
4. 이번 글의 핵심 논조(Stance)는 다음과 같다: "{stance}"
"""
    
    @gemini_retry
    def call_planner():
        gemini_limiter.consume()
        return client.models.generate_content(
            model='models/gemini-3-flash-preview', # Latest flash for planning
            contents=planning_prompt,
            config={'response_mime_type': 'application/json', 'response_schema': PlanningOutput}
        )
    
    plan_resp = call_planner()
    plan_data = json.loads(plan_resp.text)
    print(f"  ✅ 기획 완료: {plan_data['strategy'][:50]}...")

    # --- PHASE 2: Specialist Trio (SEO / AEO / GEO) ---
    print("🔍 [Phase 2] 전문가 3인방: 영역별 최적화 요소 생성 중...")
    specialist_prompt = f"""
너는 'SEO 전문가', 'AEO 전문가', 'GEO 전문가' 3인방의 역할을 동시에 수행하여 기획국장의 오더에 맞춘 최상의 콘텐츠 요소를 생성해야 한다.

[기획국장의 가이드라인]
전략: {plan_data['strategy']}
목차: {plan_data['outline']}
추가 지시: {plan_data['expert_guidelines']}

{data_block}

---
[각 전문가별 페르소나 및 핵심 지침]

🔍 블로그 전담 SEO 전문가
- 목표: 검색 의도 파악, 키워드 전략, 제목 및 메타디스크립션 최적화, H태그 설계, E-E-A-T 강화.
- 구체적 예시와 실무적 판단 기준을 포함하라.
- **주의 (제목 작성 규칙)**: 제목 앞에 `[긴급분석]`, `[Post-Mortem]`, `[심층리뷰]` 등과 같이 대괄호(`[]`)를 사용한 태그나 수식어를 절대 붙이지 마라. 깔끔하고 직관적인 본문 내용 위주의 제목으로 작성하라.

💡 블로그 전담 AEO 전문가
- 목표: 구글 AI 오버뷰, 퍼플렉시티 등이 인용하기 좋은 형태로 최적화.
- BLUF(결론부터) 방식 적용, 질문형 구조 설계, FAQ 섹션 최적화, 신뢰 요소 및 데이터 구조화.

🌐 블로그 전담 GEO 전문가
- 목표: 생성형 AI 엔진이 가장 신뢰할 만한 출처로 판단하도록 신뢰도와 문맥 극대화.
- 추상적 일반론 배제(Anti-Fluff), 구체적인 수치/데이터/출처 명시, AI가 요약하기 좋은 논리적 구조 설계.
"""

    @gemini_retry
    def call_specialists():
        gemini_limiter.consume()
        return client.models.generate_content(
            model='models/gemini-3-flash-preview', # Latest pro for specialist expertise
            contents=specialist_prompt,
            config={'response_mime_type': 'application/json', 'response_schema': SpecialistOutput}
        )

    spec_resp = call_specialists()
    spec_data = json.loads(spec_resp.text)
    print(f"  ✅ 전문가 3인방 작업 완료 (SEO/AEO/GEO elements ready)")

    # --- PHASE 3: General Editor ---
    print("🖋️ [Phase 3] 총괄 편집장: 최종 원고 집필 및 윤문 중...")
    editor_prompt = f"""
너는 블로그 자동화 파이프라인의 최종 문지기인 '총괄 편집장(Editor-in-Chief)'이다. 너의 목표는 전문가들이 생성한 정보들을 취합하여, 독자가 읽었을 때 "사람이 쓴 고품질 전문가 칼럼"이라고 느낄 만큼 자연스럽고 유려한 문장으로 완성하는 것이다.

[입력 데이터]
기획국장 전략: {plan_data['strategy']}
SEO 전문가 결과: {spec_data['seo_part']}
AEO 전문가 결과: {spec_data['aeo_part']}
GEO 전문가 결과: {spec_data['geo_part']}

---
[총괄 편집장 핵심 지침]
1. 통합 및 흐름(Flow) 최적화: 3인의 결과물 중 중복 제거 및 논리적 재배치.
2. 톤앤매너 및 윤문: 기계적 문체 탈피, 지적이고 유려한 '해요체' 활용, AI 특유의 상투적 표현(도입부/결론부) 금지.
3. 모바일 가독성 및 스타일 (핵심 지침):
   - 서론 직전에는 반드시 `<div class="bluf"><strong>[BLUF]</strong><p>결론 요약 내용</p></div>` 형태의 HTML 코드를 사용하여 결론을 배치하라. (절대 인라인 스타일 style="" 속성을 추가하지 말 것)
   - 한 문단은 반드시 2~3문장 이내로 짧게 구성하여 모바일에서의 가독성을 극대화하라.
   - 모든 문단의 첫 시작은 반드시 한 칸의 공백(' ')을 삽입하여 들여쓰기를 명확히 적용하라. (텍스트 상에서 한 칸 띄우고 시작)
   - 핵심 주장, 통찰력 있는 결론, 또는 중요한 인용구는 마크다운 인용 블록(`>`)을 사용하여 시각적으로 강렬하게 강조하라.
4. 기술적 요소의 자연스러운 삽입: 표, 인용구 등이 맥락 속에 녹아들게 배치. (**주의: FAQ 섹션은 별도 시스템에서 생성하므로 본문에 직접 작성하지 마십시오.**)
5. [이미지 삽입]: 본문 내 적절한 위치에 **[이미지: 영어로 된 상세한 Editorial Style 생성 프롬프트]** 형식을 2~3곳 삽입하라.
   - **주의**: 아이소메트릭(Isometric) 스타일은 절대 사용하지 마십시오. 대신 추상적이고 예술적인 테크 매거진 스타일(Glassmorphism, Abstract Art, Macro shot 등)을 묘사하십시오.
6. 분량: 공백 제외 3,500자 이상의 심층 분석글.
7. 결과물 형식: HTML 태그와 마크다운이 혼용된 원고 본문만 출력하라. (제목과 프론트매터 제외)
"""

    @gemini_retry
    def call_editor():
        gemini_limiter.consume()
        return client.models.generate_content(
            model='models/gemini-3-flash-preview', # Latest pro for final quality
            contents=editor_prompt,
            config={'response_mime_type': 'application/json', 'response_schema': BlogPostSchema}
        )

    final_resp = call_editor()
    final_data = json.loads(final_resp.text)
    print(f"  ✅ 최종 원고 완성: {final_data['title']}")

    return final_data, None

def generate_blog_post(crawled_content, folder="posts", additional_instructions="", keyword="", stance="", schedule_type=None):
    """
    Original generation function (Legacy/Fallback)
    Now redirects to multi-agent for 'posts' folder.
    """
    if folder == "posts":
        return generate_blog_post_multi_agent(crawled_content, folder, keyword, stance, schedule_type)
    
    # Glossary logic remains same for now as it's a specific simple task
    api_key = os.getenv("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    primary_topic = keyword if keyword else crawled_content['title']
    
    data_block = f"""
### 🎯 핵심 타겟 키워드:
{primary_topic}

### 📄 수집된 본문 데이터:
출처 URL: {crawled_content['url']}
본문 내용:
{crawled_content['body']}
"""

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
        # This part should ideally not be reached if folder is 'posts' due to redirect, 
        # but kept for robustness if other folders are added later.
        prompt = f"Write a professional blog post about {primary_topic} using the following data:\n{data_block}"

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