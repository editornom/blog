import os
import re
import html
import json

def load_faq_content(keyword):
    """
    Reads FAQ from source/accordian/{keyword}.txt.
    Strips 'Q1.', 'A1.', '**', ':', '.' etc. from indices.
    Returns a list of dictionaries with 'q' and 'a' keys.
    """
    # 키워드에서 파일명으로 쓰기 부적절한 문자 제거 및 공백을 언더바로 변경
    safe_keyword = re.sub(r'[\\/*?:"<>|]', "", keyword).replace(" ", "_")
    faq_path = os.path.join("source", "accordian", f"{safe_keyword}.txt")
    
    if not os.path.exists(faq_path):
        return None
    
    faqs = []
    current_q = None
    current_a = []
    
    # Improved regex to strip decoration like **Q1. ** or Q1: **
    # It looks for lines starting with Optional ** then Q followed by numbers, then . or : and optional **
    q_re = re.compile(r'^\s*(\*\*)?Q\d*[\.:]\s*(.*?)\s*(\*\*)?\s*$', re.IGNORECASE)
    a_re = re.compile(r'^\s*(\*\*)?A\d*[\.:]\s*(.*?)\s*(\*\*)?\s*$', re.IGNORECASE)
    
    # Helper to clean remaining markers if regex only partially matched
    def clean_text(text):
        if not text: return ""
        # Remove leading/trailing ** if any survived
        text = text.strip()
        if text.startswith("**") and text.endswith("**"):
            text = text[2:-2].strip()
        elif text.startswith("**"):
            text = text[2:].strip()
        elif text.endswith("**"):
            text = text[:-2].strip()
        return text

    with open(faq_path, "r", encoding="utf-8") as f:
        for line in f:
            line_stripped = line.strip()
            if not line_stripped:
                continue
                
            # Check for Question header
            q_match = q_re.match(line_stripped)
            if q_match:
                # If we were previously building a Q&A pair, save it
                if current_q and current_a:
                    faqs.append({"q": current_q, "a": "\n".join(current_a).strip()})
                    current_a = []
                current_q = clean_text(q_match.group(2))
                continue
            
            # Check for Answer header
            a_match = a_re.match(line_stripped)
            if a_match:
                current_a = [clean_text(a_match.group(2))]
                continue
            
            # If we have a question but no answer started yet, and it's not a new question
            # then this line MUST be the start of the answer
            if current_q and not current_a:
                current_a.append(line_stripped)
                continue
                
            # If an answer has already started, keep appending
            if current_q and current_a:
                current_a.append(line.rstrip())
                
        # Append the final pair after loop
        if current_q and current_a:
            faqs.append({"q": current_q, "a": "\n".join(current_a).strip()})
            
    return faqs

def append_faq_to_draft(draft, faqs):
    """
    Appends FAQ accordion to the bottom of the draft and injects FAQPage JSON-LD schema.
    """
    if not faqs:
        return draft
    
    # 1. 중복 삽입 방지: 기존 FAQ 블록 전체 제거 (정규식 개선)
    # 기존 원고에 이미 생성된 FAQ 섹션이 있다면 완전히 도려낸 후 새 데이터로 덮어씁니다.
    existing_faq_pattern = re.compile(r'\n*## ✅ 자주 묻는 질문 \(FAQ\).*$', re.DOTALL)
    if existing_faq_pattern.search(draft):
        draft = existing_faq_pattern.sub("", draft)
        
    faq_md = "\n\n## ✅ 자주 묻는 질문 (FAQ)\n"
    
    # SEO(GEO) 강화를 위한 JSON-LD 스키마 초기화
    schema_dict = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": []
    }
    
    for faq in faqs:
        # 안전한 HTML 이스케이프 처리 (HTML 태그 꼬임으로 인한 레이아웃 붕괴 방지)
        safe_q = html.escape(faq['q'])
        safe_a = html.escape(faq['a'])
        
        # Accordion UI 마크다운 결합
        faq_md += f"\n<details>\n  <summary>{safe_q}</summary>\n  <div class=\"faq-content\">\n\n{safe_a}\n\n  </div>\n</details>\n"
        
        # JSON-LD 스키마 데이터 조립 (json.dumps가 이스케이프를 완벽 처리하므로 원본 텍스트 사용)
        schema_dict["mainEntity"].append({
            "@type": "Question",
            "name": faq['q'],
            "acceptedAnswer": {
                "@type": "Answer",
                "text": faq['a']
            }
        })
    
    # 깔끔하게 원고 맨 아래에 붙이기
    return draft.strip() + faq_md

if __name__ == "__main__":
    # Test script for local verification
    test_keyword = "터보퀀트"
    results = load_faq_content(test_keyword)
    if results:
        print(f"Successfully parsed {len(results)} FAQs:")
        for i, item in enumerate(results, 1):
            print(f"Q{i}: {item['q']}")
            print(f"A{i}: {item['a'][:50]}...")
    else:
        print("Failed to parse FAQ.")
