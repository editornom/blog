import os
import re
import sys
import uuid
import time
import subprocess

# 기존 생성/번역 모듈에 접근하기 위해 경로 추가
sys.path.append(os.path.abspath('scripts'))
from imagen_helper import generate_image
from translator import translate_text

def audit_and_fix():
    print("🔍 한국어(ko) 원본 블로그 파일들을 스캔하여 미처리된 이미지 플레이스홀더를 점검합니다...\n")
    
    # 공백 및 이스케이프까지 완벽하게 잡아내는 최종 정규식
    pattern = re.compile(r'(?:\*\*|\_)?!*\\?\[\s*이미지\s*:\s*([^\]\\]+)\\?\](?:\*\*|\_)?|(?:\*\*|\_)?!*\[이미지\]\(([^)]+)\)(?:\*\*|\_)?')
    
    base_dir = os.path.join("src", "data", "blog", "ko")
    fixed_files = []
    
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith('.md'):
                filepath = os.path.join(root, file)
                
                # 폴더명 (posts 혹은 glossary 등)
                folder = os.path.basename(os.path.dirname(filepath))
                
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        draft = f.read()
                except Exception as e:
                    print(f"⚠️ 파일 읽기 오류 ({filepath}): {e}")
                    continue
                    
                matches = list(pattern.finditer(draft))
                if not matches:
                    continue
                    
                print(f"\n⚠️ 문제 발견: {filepath} (미처리 플레이스홀더 {len(matches)}개)")
                
                # 파일명에서 키워드 추출 (예: 260506_keyword-name.md -> keyword-name)
                filename_without_ext = os.path.splitext(file)[0]
                keyword = re.sub(r'^\d{6}_', '', filename_without_ext)
                
                source_img_dir = os.path.join("source", folder, keyword)
                os.makedirs(source_img_dir, exist_ok=True)
                image_context = f"Post Title: {keyword}"
                
                # 발견된 플레이스홀더별로 이미지 생성 및 치환
                for i, match in enumerate(matches):
                    prompt = (match.group(1) or match.group(2)).strip()
                    full_match_str = match.group(0)
                    
                    img_uuid = str(uuid.uuid4())[:8]
                    img_filename = f"{img_uuid}-{i}.webp"
                    img_path = os.path.join(source_img_dir, img_filename)
                    
                    print(f"  🎨 [{i+1}/{len(matches)}] 이미지 재생성 시도 중: {prompt[:40]}...")
                    generated_path, img_error = generate_image(prompt, img_path, context=image_context)
                    
                    if generated_path:
                        rel_path = f"../../../../../source/{folder}/{keyword}/{img_uuid}-{i}.webp"
                        # 마크다운 링크 파싱 오류 방지를 위한 괄호 인코딩
                        encoded_rel_path = rel_path.replace('(', '%28').replace(')', '%29')
                        
                        alt_clean_prompt = f"다음 이미지 생성용 프롬프트에서 시각적 스타일 키워드(4k, 해상도 등)를 제외하고, 초보자도 이해할 수 있는 핵심 의미만 한 문장으로 요약해서 ko로 번역해줘:\n{prompt}"
                        translated_alt = translate_text(alt_clean_prompt, "ko")
                        
                        md_img_link = f"![{keyword} - {translated_alt}]({encoded_rel_path})"
                        draft = draft.replace(full_match_str, md_img_link)
                        
                        # ogImage 갱신 (첫 번째 발견 이미지 한정)
                        if i == 0:
                            draft = re.sub(r'ogImage:.*', f'ogImage: "{rel_path}"', draft)
                    else:
                        print(f"  ❌ 이미지 생성 실패: {img_error}")
                
                # AI 생성 과정에서 생긴 잘못된 <p> 태그 래핑 제거 및 줄바꿈 보정
                draft = re.sub(r'<p>\s*(!\[.*?\]\(.*?\))\s*</p>', r'\n\n\1\n\n', draft)
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(draft)
                    
                print(f"✅ 로컬 원본 수정 완료: {filepath}")
                fixed_files.append((filepath, folder))

    # EN, CN, JP 다국어 동기화 작업
    if fixed_files:
        print("\n🚀 누락된 이미지가 모두 로컬에 생성/배치되었습니다!")
        print("수정된 파일의 다국어 버전을 동기화하기 위해 번역 파이프라인을 시작합니다...\n")
        
        for filepath, folder in fixed_files:
            print(f"🔄 다국어 동기화 중: {filepath}")
            # scripts/main.py 단일 파일 재실행 모드 호출
            subprocess.run([sys.executable, "scripts/main.py", filepath, folder], check=True)
            
        print("\n🎉 모든 스캔, 복구 및 다국어 번역 동기화 작업이 완벽하게 완료되었습니다!")
    else:
        print("\n🎉 축하합니다! 한국어(ko) 원본 파일 내에 깨진 이미지 플레이스홀더가 하나도 없습니다.")

if __name__ == "__main__":
    audit_and_fix()
