import os
import re

def load_faq_content(keyword):
    """
    Reads FAQ from source/accordian/{keyword}.txt.
    Strips 'Q1.', 'A1.', '**', ':', '.' etc. from indices.
    Returns a list of dictionaries with 'q' and 'a' keys.
    """
    faq_path = os.path.join("source", "accordian", f"{keyword}.txt")
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
            
            # If we have a current question and answer started, append intermediate lines to answer
            if current_q and current_a:
                current_a.append(line.rstrip())
                
        # Append the final pair after loop
        if current_q and current_a:
            faqs.append({"q": current_q, "a": "\n".join(current_a).strip()})
            
    return faqs

def append_faq_to_draft(draft, faqs):
    """
    Appends FAQ accordion to the bottom of the draft using standard labels.
    """
    if not faqs:
        return draft
    
    faq_md = "\n\n## ✅ 자주 묻는 질문 (FAQ)\n"
    for faq in faqs:
        # Standard format following 하이온넷 UTM post
        faq_md += f"\n<details>\n  <summary>{faq['q']}</summary>\n  {faq['a']}\n</details>\n"
    
    # Insert before hashtags if any, otherwise at the end
    if " # " in draft:
        parts = draft.rsplit(" # ", 1)
        return parts[0] + faq_md + "\n # " + parts[1]
    else:
        return draft + faq_md

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
