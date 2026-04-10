import os
import sys
from translator import translate_and_save

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

def retry_jp_translation():
    # 1. 원본 한국어 파일 경로
    slug = "enterprise-ai-agent-orchestration-strategy"
    ko_path = os.path.join("src", "data", "blog", "ko", "posts", f"{slug}.md")
    
    if not os.path.exists(ko_path):
        print(f"❌ {ko_path} 파일을 찾을 수 없습니다.")
        return

    with open(ko_path, "r", encoding="utf-8") as f:
        korean_draft = f.read()

    # 2. 일본어만 번역 시도 (새로운 재시도 로직 적용됨)
    print(f"🚀 [RETRY] '{slug}' 포스팅의 일본어 번역을 다시 시도합니다...")
    results = translate_and_save(korean_draft, slug, "posts", target_langs=["jp"])
    
    if results.get("jp", {}).get("success"):
        print("\n✨ 일본어 번역 및 저장이 성공적으로 완료되었습니다!")
    else:
        print("\n❌ 일본어 번역에 다시 실패했습니다. 사유:", results.get("jp", {}).get("error"))

if __name__ == "__main__":
    retry_jp_translation()
