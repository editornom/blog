import os
import sys

# Add scripts directory to path
sys.path.append(os.path.abspath("scripts"))

from imagen_helper import generate_image

target_dir = r"source\posts\OAuth_Supply_Chain_Security"
os.makedirs(target_dir, exist_ok=True)

prompts = [
    ("OAuth Supply Chain Security - 디지털 네트워크에서 신뢰가 무너지며 빛나던 열쇠들이 어두운 그림자로 변하는 모습.", "img1.webp"),
    ("OAuth Supply Chain Security - 작은 황금색 기어 하나의 파손으로 인해 전체 수정 구조가 일그러지는 복잡한 기어 시스템의 모습.", "img2.webp"),
    ("OAuth Supply Chain Security - 거대한 네트워크망을 비추며 디지털 안개를 가르는 미래형 등대 불빛.", "img3.webp")
]

for prompt, filename in prompts:
    output_path = os.path.join(target_dir, filename)
    print(f"Generating image: {filename}...")
    generate_image(prompt, output_path)

print("Image regeneration complete.")
