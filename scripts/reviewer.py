from google import genai
from google.api_core import exceptions
from api_utils import gemini_retry, gemini_limiter, gemini_tracker
import os
import re
import yaml
from dotenv import load_dotenv

load_dotenv()

def review_manuscript(draft_data, folder="posts"):
    """
    Sends the generated blog post draft to Gemini for final inspection and refinement.
    
    Args:
        draft_data: Dictionary containing 'title' and 'content'.
        folder: Target content category.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY not found in .env")
        return draft_data

    client = genai.Client(api_key=api_key)

    current_title = draft_data.get('title', '')
    body_content = draft_data.get('content', '')

    # 경쟁사 텍스트 파일 로드 (Negative Prompt 활용)
    competitors_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "competitors.txt")
    competitor_list_str = ""
    # ... (Keep competitor logic unchanged) ...
    if os.path.exists(competitors_file):
        try:
            with open(competitors_file, "r", encoding="utf-8") as f:
                competitors = [line.strip().split('.')[0] for line in f if line.strip() and not line.startswith("#")]
                if competitors:
                    competitor_list_str = f"자사 마케팅 목적에 위배되는 다음 경쟁사 브랜드({', '.join(competitors)})는 본문에서 철저히 배제 및 삭제하십시오."
        except Exception:
            pass

    # ... (Prompt remains similar but assumes title/content separation) ...
    if folder == "glossary":
        prompt = f"""
당신은 IT/테크 분야의 '수석 백과사전 편집자'입니다.
주어진 초안은 용어 사전(Glossary)의 문서입니다. 
당신의 임무는 원본의 정확한 기술적 데이터와 구조(사전적 정의, 실무 사용 예시, 관련 단어 등)를 엄격히 보전하면서, 어색한 기계적 문장이나 번역투를 자연스럽게 교정(Detox)하는 것입니다.

아래 원칙을 엄격하게 준수하십시오:
1. 제목: 절대로 거창한 수식어나 부제를 붙이지 마십시오. "{current_title}"의 핵심 용어를 파악하여 반드시 "용어명" 또는 "용어명이란?" 과 같이 가장 단순하고 직관적인 형태로만 작성하십시오.
2. 어조: '~입니다', '~합니다' 형태의 건조하고 객관적인 백과사전식 문체를 완벽히 유지하십시오. 칼럼니스트처럼 주관적인 통찰이나 비평을 절대 덧붙이지 마십시오.
3. {competitor_list_str}
4. 마크다운 보존: 굵은 글씨(**텍스트**)가 너무 기계적으로 남발되어 있다면 꼭 필요한 1~2개만 남기고 정리하십시오.
5. 어떠한 메타 코멘트(예: "수정된 원고입니다")도 출력하지 마십시오.

---
[초안 제목]
{current_title}

[초안 본문]
{body_content}

# 최종 출력 형식 (지시사항 - 절대 준수)
1. 첫 번째 줄에는 반드시 '다듬어진 단순한 제목'만 작성하십시오.
2. 두 번째 줄은 비워두십시오.
3. 세 번째 줄부터 '다듬어진 본문(마크다운)'을 작성하십시오.
"""
    else:
        prompt = f"""
당신은 IT 트렌드, 보안, 인공지능(AI), 차세대 소프트웨어 기술을 아우르는 15년 차 '수석 기술 전문 칼럼니스트'입니다. 당신의 글은 기술적 깊이를 놓치지 않으면서도, 현업 전문가부터 기술에 관심 있는 일반 독자들까지 매료시킬 수 있는 통찰력 넘치는 '테크 매거진 칼럼' 스타일이어야 합니다.
주어진 초안은 데이터 중심의 팩트 나열로 인해 딱딱한 보고서 느낌이 들거나, AI가 작성하여 기계적인 패턴과 상투적인 표현이 섞여 있습니다.
당신의 임무는 원본의 정확한 기술적 데이터는 보전하되, 독자가 끝까지 읽고 싶어질 만큼 세련되고 전문적인 '테크 매거진 칼럼'으로 전면 재작성(Rewriting)하는 것입니다.

아래의 [AI 냄새 제거 5대 원칙]을 엄격하게 준수하여 원고를 수정하십시오.

1. AI 특유의 진부한 클리셰 및 금지어 제거 (Negative Constraints)
- 도입부: "급변하는 IT 환경 속에서", "단순한 ~을 넘어", "~에 대해 알아보겠습니다", "비평가의 시선으로 해부해보겠습니다" 등 상투적인 시작을 절대 금지합니다. 핵심 화두로 바로 진입하십시오.
- 결론부: "결론적으로", "요약하자면", "마치며" 같은 기계적인 접속사나 소제목을 지우고, 실무적인 제언이나 자연스러운 마무리로 대체하십시오.
- 드라마틱 톤 제거: "엑소더스", "치명적인", "폭발 반경", "무력화", "배신", "완벽한", "전례 없는", "혁신적인" 등 문학적/영화적 비유나 지나치게 감정적인 형용사를 철저히 배제하십시오. 대신 "데이터 유출 위협 증가", "연쇄적 보안 침해", "시스템 무력화 시도", "권한 탈취" 와 같이 드라이하고 전문적인 IT 실무 용어로 교체하십시오.
- {competitor_list_str}
- (가), (나), (다) 또는 **가**, **나** 와 같이 AI가 주로 억지로 사용하는 문서 넘버링이나 기호들은 작위적인 느낌이 들지 않도록 자연스러운 불릿 포인트(-)나 문장으로 다듬으십시오.

2. 작위적인 페르소나 및 화법 제거
- 글쓴이를 스스로 "전문가로서", "필자는" 등으로 지칭하며 과도하게 권위를 부여하는 표현을 모두 삭제하십시오. 
- 영어 단어를 불필요하게 섞어 쓰는 것을 지양하되, IT 업계 표준 용어(API, 클라우드, 온프레미스, 오픈소스 등)는 자연스럽게 사용하십시오.

3. 자연스러운 문체와 리듬감 (Tone & Manner)
- '~습니다', '~합니다' 형태의 깔끔한 문어체를 기본으로 하되, 테크 매거진 특유의 매끄럽고 세련된 어조를 유지하십시오.
- 문장 사이의 논리적 연결이 매끄러워야 하며, 단순한 정보 전달을 넘어 "이 기술이 왜 중요한가?"에 대한 에디터의 통찰력이 배어 나오도록 표현하십시오.
- 불필요하게 딱딱한 번역투 문장을 쪼개고, 독자와 직접 대화하는 듯한 읽기 쉬운 문형을 사용하십시오.
- 🚨 [키워드 스터핑 정제]: 초안에 특정 명사가 비정상적으로 반복되어 있다면, 과감하게 대명사로 대체하거나 아예 생략하여 글의 피로도를 낮추십시오.

4. 구조 및 소제목 정제
- 'Feature:', 'Key Insights:', '핵심 요약' 등 AI가 붙이는 뻔하고 작위적인 태그형 소제목을 삭제하십시오.
- 대신 해당 섹션의 주제를 상징하는 짧고 강렬한, 혹은 호기심을 자극하는 '매거진 스타일'의 제목으로 변경하십시오.

5. 마크다운 및 원본 요소 정제 (Refinement)
- 원본에 포함된 이미지 태그, 코드 블록 등은 보존하되, **굵은 글씨(**강조**)**가 남발되어 기계적인 느낌(AI Smell)이 난다면 이를 과감히 삭제하거나 문맥상 꼭 필요한 곳에만 1~2회 남기고 일반 텍스트로 되돌리십시오.
- 어떠한 메타 코멘트(예: "수정된 원고입니다", "요청하신 대로 윤문했습니다")도 출력하지 마십시오. 
- 오직 마크다운 문법으로 완성된 '최종 수정 원고 텍스트'만 출력해야 합니다.

---
[초안 제목]
{current_title}

[초안 본문]
{body_content}

# 최종 출력 형식 (지시사항 - 절대 준수)
1. 첫 번째 줄에는 반드시 '다듬어진 제목'만 작성하십시오. (따옴표나 '제목:' 같은 태그 포함 금지)
2. 두 번째 줄은 비워두십시오.
3. 세 번째 줄부터 '다듬어진 본문(마크다운)'을 작성하십시오.
4. 어떠한 메타 코멘트도 포함하지 마십시오.
"""

    @gemini_retry
    def call_api():
        gemini_limiter.consume()
        return client.models.generate_content(
            model='models/gemini-3-flash-preview', 
            contents=prompt
        )

    try:
        print("Gemini가 원고 및 제목을 검수(디톡스) 중입니다...")
        response = call_api()
        gemini_tracker.add_text_usage(response)
        response_text = response.text.strip()
        
        # 제목과 본문 분리 파싱
        parts = response_text.split("\n", 2)
        if len(parts) >= 3:
            refined_title = parts[0].strip().strip('"').strip("'")
            result_text = parts[2].strip()
        elif len(parts) == 2:
             refined_title = parts[0].strip().strip('"').strip("'")
             result_text = parts[1].strip()
        else:
            refined_title = current_title
            result_text = response_text

        # 🛡️ 파이썬 기반 마크다운 문법 안정성 검사
        if result_text.count("```") % 2 != 0:
            print("  ⚠️ [Detox] 마크다운 코드 블록 닫기(```) 누락 감지. 자동 복구합니다.")
            result_text += "\n```\n"
            
        # 잘못 생성된 이미지 태그(!![...]) 수정
        if "!![" in result_text:
            print("  ⚠️ [Detox] 잘못된 이미지 태그(!![) 감지. 자동 복구합니다.")
            result_text = result_text.replace("!![", "![")

        return {
            "title": refined_title,
            "content": result_text
        }

    except Exception as e:
        print(f"❌ Gemini 디톡스 중 오류 발생: {e}")
        return draft_data

    except Exception as e:
        print(f"❌ Gemini 디톡스 중 오류 발생: {e}")
        return draft_data
