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

def prepare_faq_data(draft, faqs):
    """
    Cleans up any legacy FAQ blocks in the draft and returns the cleaned draft 
    along with the FAQ data list for frontmatter insertion.
    """
    if not faqs:
        return draft, []
    
    # 1. 중복 삽입 방지: 기존 레거시 FAQ 블록(HTML 방식) 제거
    # 정적 HTML 삽입 방식에서 프런트매터 방식으로 전환하므로 기존 본문에 남은 찌꺼기를 제거합니다.
    existing_faq_pattern = re.compile(r'\n*## ✅ 자주 묻는 질문 \(FAQ\).*$', re.DOTALL)
    if existing_faq_pattern.search(draft):
        draft = existing_faq_pattern.sub("", draft)
        
    return draft.strip(), faqs

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
