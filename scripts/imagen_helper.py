from google import genai
from google.api_core import exceptions
from api_utils import gemini_retry, gemini_limiter
from dotenv import load_dotenv
import os
import sys
from PIL import Image
import io

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

load_dotenv()

def enhance_image_prompt(base_prompt, client):
    """
    기호나 짧은 단어로 이루어진 초기 프롬프트를 고품질 이미지 생성을 위한 상세 영문 프롬프트로 증강합니다.
    """
    try:
        enhance_prompt = f"""
당신은 DALL-E, Midjourney, Imagen 같은 AI 이미지 제너레이터 프롬프트 작성 전문가입니다.
사용자가 블로그에 삽입할 이미지의 간략한 상황 설명이나 키워드를 줄 것입니다.
이를 바탕으로 최고 품질의 이미지를 생성할 수 있는 매우 상세한 영문 프롬프트(Prompt)로 확장해주세요.
반드시 영어로만 출력하며, "Cinematic lighting, 8k resolution, highly detailed, photorealistic, isometric 3d render" 등의 수식어를 적절히 혼합하여 쉼표로 연결된 1~2줄의 문구만 출력하십시오. 
특히, 이미지 내에 텍스트(Text), 인포그래픽(Infographic), 표(Table), 차트(Chart) 등이 절대 포함되지 않도록 "no text, no infographics, no tables, no charts, no labels"와 같은 부정 프롬프트를 적절히 융합하여 프롬프트를 구성하십시오.

[원본 설명]: {base_prompt}
"""
        response = client.models.generate_content(
            model='models/gemini-3-flash-preview',
            contents=enhance_prompt
        )
        enhanced = response.text.strip()
        print(f"✨ 프롬프트 증강 완료: {enhanced[:80]}...")
        return enhanced
    except Exception as e:
        print(f"⚠️ 프롬프트 증강 실패, 원본을 사용합니다: {e}")
        return base_prompt

def generate_image(prompt, output_filename):
    """
    Imagen 모델들을 순차적으로 시도하여 이미지를 생성하고 지정된 포맷으로 저장합니다.
    최신(4.0)부터 안정성(3.0) 순으로 폴백 로직을 가동합니다.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ GEMINI_API_KEY가 .env 파일에 없습니다.")
        return None

    # 시도할 모델 후보 리스트 (최신 4.0부터 가장 안정적인 3.0까지)
    MODELS_TO_TRY = [
        'imagen-4.0-generate-001',
        'imagen-4-fast-generate-001',
        'imagen-3.1-generate-001',
        'imagen-3.0-generate-001'
    ]

    client = genai.Client(api_key=api_key)

    @gemini_retry
    def call_imagen(m_name, target_prompt):
        gemini_limiter.consume()
        return client.models.generate_images(
            model=m_name,
            prompt=target_prompt,
            config={
                'number_of_images': 1,
                'aspect_ratio': '1:1',
                'safety_filter_level': 'BLOCK_LOW_AND_ABOVE',
                'person_generation': 'ALLOW_ADULT'
            }
        )

    # 1. 프롬프트 증강 (Prompt Enhancement)
    enhanced_prompt = enhance_image_prompt(prompt, client)

    # 2. 이미지 생성 시도 루프
    for model_name in MODELS_TO_TRY:
        try:
            print(f"🎨 {model_name} 모델로 이미지 생성을 시도합니다...")
            response = call_imagen(model_name, enhanced_prompt)
            
            if response.generated_images:
                # [수정된 부분] SDK 객체에서 바이트(Bytes)를 직접 꺼내 PIL로 변환 후 저장
                img_bytes = response.generated_images[0].image.image_bytes
                pil_img = Image.open(io.BytesIO(img_bytes))
                
                # 포맷 최적화: .webp로 강제 변환 및 저장
                if output_filename.endswith('.png'):
                    output_filename = output_filename.replace('.png', '.webp')
                
                # PIL 객체의 save를 사용하므로 format='WEBP'가 정상 작동합니다.
                pil_img.save(output_filename, format='WEBP')
                
                # 비용 추적기 업데이트
                try:
                    from api_utils import gemini_tracker
                    gemini_tracker.add_image_usage()
                except Exception:
                    pass
                
                print(f"✅ {model_name}을(를) 사용하여 이미지 WebP 포맷 최적화 저장 완료: {output_filename}")
                return output_filename
            else:
                print(f"⚠️ {model_name} 결과가 없습니다. 다음 모델로 넘어갑니다.")
                
        except exceptions.NotFound:
            print(f"ℹ️ {model_name}은 현재 계정에서 사용할 수 없거나 지원하지 않습니다. (404)")
        except exceptions.ResourceExhausted:
            print(f"⏳ {model_name}의 속도 제한(Rate Limit)에 걸렸으나 재시도 후에도 실패했습니다.")
        except Exception as e:
            print(f"⚠️ {model_name} 오류 발생: {str(e)[:100]}...")
            
        # 다음 모델 시도 환경 조성
        continue

    print("❌ 모든 Imagen 모델 시도가 실패했습니다.")
    return None

if __name__ == "__main__":
    # 단독 테스트용
    test_outfile = "test_fallback_imagen.png"
    generate_image("A highly detailed futuristic data center with neon lights, isometric view, cinematic lighting", test_outfile)
