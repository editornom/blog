from google import genai
from google.api_core import exceptions
from api_utils import gemini_retry, gemini_limiter, gemini_tracker
import os
import re
from dotenv import load_dotenv

load_dotenv()

def review_manuscript(draft, folder="posts"):
    """
    Sends the generated blog post draft to Gemini for final inspection and refinement.
    
    Args:
        draft: The markdown content generated.
        folder: Target content category.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY not found in .env")
        return draft

    client = genai.Client(api_key=api_key)

    # 🌟 [개선] Frontmatter 분리 로직 (Action Plan 5)
    # YAML 영역을 AI에게 보내지 않고 보호하여 Astro 빌드 에러를 원천 차단합니다.
    yaml_match = re.match(r'^(---\s*\n.*?\n---\s*\n)', draft, re.DOTALL)
    if yaml_match:
        frontmatter = yaml_match.group(1)
        body_content = draft[len(frontmatter):]
    else:
        frontmatter = ""
        body_content = draft

    # 경쟁사 텍스트 파일 로드 (Negative Prompt 활용)
    competitors_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "competitors.txt")
    competitor_list_str = ""
    if os.path.exists(competitors_file):
        try:
            with open(competitors_file, "r", encoding="utf-8") as f:
                # 도메인 확장자 제거하고 브랜드명만 추출
                competitors = [line.strip().split('.')[0] for line in f if line.strip() and not line.startswith("#")]
                if competitors:
                    competitor_list_str = f"자사 마케팅 목적에 위배되는 다음 경쟁사 브랜드({', '.join(competitors)})는 본문에서 철저히 배제 및 삭제하십시오."
        except Exception:
            pass

    # ---------------------------------------------------------
    # 📝 B2B IT 전문 에디터의 '범용 디톡스' 프롬프트
    # ---------------------------------------------------------
    prompt = f"""
당신은 15년 차 B2B IT 전문 에디터이자 테크 콘텐츠 윤문(Review & Edit) 전문가입니다.
주어진 초안은 AI가 1차적으로 작성하여 기계적인 패턴, 과장된 수식어, 진부한 표현(소위 'AI 냄새')이 묻어나는 상태입니다. 
당신의 임무는 원본의 기술적 팩트, 정보량, 마크다운 구조는 100% 유지하되, 실제 업계 실무자가 직접 쓴 것처럼 자연스럽고 담백한 글로 전면 재작성(Rewriting)하는 것입니다.

아래의 [AI 냄새 제거 5대 원칙]을 엄격하게 준수하여 원고를 수정하십시오.

1. AI 특유의 진부한 클리셰 및 금지어 제거 (Negative Constraints)
- 도입부: "급변하는 IT 환경 속에서", "단순한 ~을 넘어", "~에 대해 알아보겠습니다", "비평가의 시선으로 해부해보겠습니다" 등 상투적인 시작을 절대 금지합니다. 핵심 화두로 바로 진입하십시오.
- 결론부: "결론적으로", "요약하자면", "마치며" 같은 기계적인 접속사나 소제목을 지우고, 실무적인 제언이나 자연스러운 마무리로 대체하십시오.
- 과장된 수사: "완벽한", "전례 없는", "혁신적인", "처절한" 등 지나치게 감정적이거나 드라마틱한 형용사를 제거하고 담백한 팩트 위주로 서술하십시오.
- {competitor_list_str}
- (가), (나), (다) 또는 **가**, **나** 와 같이 AI가 주로 억지로 사용하는 문서 넘버링이나 기호들은 작위적인 느낌이 들지 않도록 자연스러운 불릿 포인트(-)나 문장으로 다듬으십시오.

2. 작위적인 페르소나 및 화법 제거
- 글쓴이를 스스로 "전문가로서", "필자는" 등으로 지칭하며 과도하게 권위를 부여하는 표현을 모두 삭제하십시오. 
- 영어 단어를 불필요하게 섞어 쓰는 것을 지양하되, IT 업계 표준 용어(API, 클라우드, 온프레미스, 오픈소스 등)는 자연스럽게 사용하십시오.

3. 자연스러운 문체와 리듬감 (Tone & Manner)
- '~습니다', '~합니다' 형태의 깔끔한 문어체를 기본으로 하십시오.
- 단, 문단이 전환되거나 특정 사실을 가볍게 짚어줄 때 '~해요', '~거든요', '~이죠' 같은 부드러운 화법을 아주 가끔 섞어 글의 호흡과 가독성을 높이십시오.
- 문장이 불필요하게 길어지는 번역투 문장("~초래할 것이라고 경고했습니다", "~시사하는 바가 큽니다")을 한국어 어순에 맞는 간결한 문장으로 쪼개고 다듬으십시오.
- 🚨 [키워드 스터핑 정제]: 초안에 특정 명사(타겟 키워드)가 비정상적으로 빽빽하게 반복되어 있다면, 과감하게 '이 기술', '해당 서비스', '이러한 접근법' 등 자연스러운 대명사로 대체하거나 아예 생략하여 글의 피로도를 낮추십시오.

4. 구조 및 소제목 정제
- 'Deep Dive:', 'The Mechanism:', '핵심 요약' 등 억지로 붙인 듯한 태그형 소제목을 삭제하고, 해당 문단의 핵심 내용을 직관적으로 보여주는 매끄러운 한국어 소제목으로 변경하십시오.

5. 마크다운 및 원본 요소 보존 (CRITICAL)
- 원본에 포함된 이미지 태그(`![이미지](...)` 또는 `[이미지: ...]`), 코드 블록, 인용구(>), 굵은 글씨(**) 등은 절대 누락하거나 훼손하지 마십시오.
- 어떠한 메타 코멘트(예: "수정된 원고입니다", "요청하신 대로 윤문했습니다")도 출력하지 마십시오. 
- 오직 마크다운 문법으로 완성된 '최종 수정 원고 텍스트'만 출력해야 합니다.

---
[초안 텍스트]
{body_content}
"""
    # ---------------------------------------------------------

    @gemini_retry
    def call_api():
        gemini_limiter.consume()
        return client.models.generate_content(
            model='models/gemini-3-flash-preview', 
            contents=prompt
        )

    try:
        print("Gemini가 원고를 검수(디톡스) 중입니다...")
        response = call_api()
        gemini_tracker.add_text_usage(response)
        result_text = response.text
        
        # 🛡️ 파이썬 기반 마크다운 문법 안정성 검사 (Action Plan 적용)
        # 1. 코드 블록(```) 닫기 누락 검사 및 자동 복구
        if result_text.count("```") % 2 != 0:
            print("  ⚠️ [Detox] 마크다운 코드 블록 닫기(```) 누락 감지. 파이썬 단에서 자동 추가합니다.")
            result_text += "\n```\n"
            
        # 2. 표(Table) 문법 기본 점검 (헤더 구분선 |---| 누락 감지)
        if "|" in result_text and "\n|---" not in result_text and "\n| ---" not in result_text.replace(" ", ""):
            print("  ⚠️ [Detox] 마크다운 표 문법이 불안전할 수 있습니다. 수동 점검이 필요할 수 있습니다.")

        # 🌟 Frontmatter 재결합
        return frontmatter + result_text

    except Exception as e:
        print(f"❌ Gemini 디톡스 중 오류 발생: {e}")
        # 오류 발생 시 원본(frontmatter + body_content = draft) 유지하여 파이프라인 중단 방지
        return draft
