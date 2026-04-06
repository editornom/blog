import re
import os

def load_faq_content_test(faq_path):
    faqs = []
    current_q = None
    current_a = []
    
    q_re = re.compile(r'^Q\d*[\.:]\s*(.*)', re.IGNORECASE)
    a_re = re.compile(r'^A\d*[\.:]\s*(.*)', re.IGNORECASE)
    
    with open(faq_path, "r", encoding="utf-8") as f:
        for line in f:
            line_stripped = line.strip()
            q_match = q_re.match(line_stripped)
            if q_match:
                if current_q and current_a:
                    faqs.append({"q": current_q, "a": "\n".join(current_a).strip()})
                    current_a = []
                current_q = q_match.group(1).strip()
                continue
            
            a_match = a_re.match(line_stripped)
            if a_match:
                current_a = [a_match.group(1).strip()]
                continue
            
            if current_q and current_a:
                current_a.append(line.rstrip())
                
        if current_q and current_a:
            faqs.append({"q": current_q, "a": "\n".join(current_a).strip()})
            
    return faqs

test_path = r"c:\Users\haionnet\Desktop\editornom\source\accordian\UTM.txt"
results = load_faq_content_test(test_path)
print(f"Total FAQs found: {len(results)}")
for i, faq in enumerate(results):
    print(f"[{i+1}] Q: {faq['q'][:50]}...")
    print(f"    A: {faq['a'][:50]}...")
