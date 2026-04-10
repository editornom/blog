import os
from google import genai
from dotenv import load_dotenv
import sys

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

load_dotenv()

def generate_image(prompt, output_filename):
    """
    Imagen 모델들을 순차적으로 시도하여 이미지를 생성합니다.
    안정성(3.x)부터 최신성(4.x) 순으로 폴백 로직을 가동합니다.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ GEMINI_API_KEY가 .env 파일에 없습니다.")
        return None

    # 시도할 모델 후보 리스트 (가장 안정적인 3.0부터 최신 4.0까지)
    MODELS_TO_TRY = [
        'imagen-3.0-generate-001',
        'imagen-3.1-generate-001',
        'imagen-4-fast-generate-001',
        'imagen-4.0-generate-001'
    ]

    client = genai.Client(api_key=api_key)

    for model_name in MODELS_TO_TRY:
        try:
            print(f"🎨 {model_name} 모델로 이미지 생성을 시도합니다...")
            
            response = client.models.generate_images(
                model=model_name,
                prompt=prompt,
                config={
                    'number_of_images': 1,
                    'aspect_ratio': '1:1', # 블로그용 1:1 비율
                    'safety_filter_level': 'BLOCK_LOW_AND_ABOVE', # 4.0 모델 권장 설정
                    'person_generation': 'ALLOW_ADULT' 
                }
            )
            
            if response.generated_images:
                response.generated_images[0].image.save(output_filename)
                print(f"✅ {model_name}을(를) 사용하여 이미지 저장 완료: {output_filename}")
                return output_filename
            else:
                print(f"⚠️ {model_name} 결과가 없습니다. 다음 모델로 넘어갑니다.")
                
        except Exception as e:
            error_msg = str(e)
            if "404" in error_msg:
                print(f"ℹ️ {model_name}은 현재 계정에서 사용할 수 없거나 지원하지 않습니다.")
            elif "429" in error_msg:
                print(f"⏳ {model_name}의 속도 제한(Rate Limit)에 걸렸습니다.")
                # 속도 제한인 경우 잠시 쉬었다 가거나 다음 모델 시도
            else:
                print(f"⚠️ {model_name} 오류 발생: {error_msg[:100]}...")
            
            # 다음 모델 시도 환경 조성
            continue

    print("❌ 모든 Imagen 모델 시도가 실패했습니다.")
    return None

if __name__ == "__main__":
    # 단독 테스트용
    test_outfile = "test_fallback_imagen.png"
    generate_image("A highly detailed futuristic data center with neon lights, isometric view, cinematic lighting", test_outfile)
