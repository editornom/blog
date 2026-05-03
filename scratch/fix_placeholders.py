import os
import re

def fix_placeholders(project_root):
    blog_dir = os.path.join(project_root, "src/data/blog")
    
    replacements = [
        # Latent Space Reasoning
        {
            'pattern': r'\[(이미지|Image|画像|图片):\s*A side-by-side comparison visualization:.*?\]',
            'replacement': '![잠재 공간 추론 (Latent Space Reasoning) - 명시적 추론(Explicit CoT)과 잠재 공간 추론의 구조적 차이를 비교한 그림입니다.](../../../../../source/posts/잠재_공간_추론_%28Latent_Space_Reasoning%29/c15c5eca-1.webp)',
            'alt_pattern': r'!\[A side-by-side comparison visualization:.*?\]\(.*?\)' # In case it was half-fixed
        },
        # PQC
        {
            'pattern': r'\[(이미지|Image|画像|图片):\s*A realistic 3D infographic showing a secure tunnel.*?\]',
            'replacement': '![PQC (Post-Quantum Cryptography) - 기존 보안 방식과 양자 내성 암호 방식 간의 보안 격차를 나타낸 인포그래픽입니다.](../../../../../source/posts/PQC_%28Post-Quantum_Cryptography%29/745212b3-1.webp)',
            'alt_pattern': r'!\[A realistic 3D infographic showing a secure tunnel.*?\]\(.*?\)'
        },
        # MAS Security
        {
            'pattern': r'\[(이미지|Image|画像|图片):\s*A high-tech security operations center.*?\]',
            'replacement': '![Multi-Agent System Security - 에이전트 간 통신 로그 및 상호작용 그래프를 분석하는 SOC 대시보드 화면입니다.](../../../../../source/posts/Multi-Agent_System_%28MAS%29_Security/audit-viz-2.png)',
            'alt_pattern': r'!\[A high-tech security operations center.*?\]\(.*?\)'
        }
    ]

    for root, dirs, files in os.walk(blog_dir):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                new_content = content
                for r in replacements:
                    # Replace text placeholders
                    new_content = re.sub(r['pattern'], r['replacement'], new_content)
                    # Replace half-fixed markdown images
                    new_content = re.sub(r['alt_pattern'], r['replacement'], new_content)
                
                if new_content != content:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"Fixed image placeholders in {file_path}")

if __name__ == "__main__":
    fix_placeholders(os.getcwd())
