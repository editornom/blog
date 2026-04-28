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

def enhance_image_prompt(base_prompt, client, context=None):
    """
    기호나 짧은 단어로 이루어진 초기 프롬프트를 고품질 이미지 생성을 위한 상세 영문 프롬프트로 증강합니다.
    context가 제공되면 해당 포스팅의 제목/키워드를 참고하여 맥락에 맞는 이미지를 구상합니다.
    """
    try:
        context_str = f"\n[현재 포스팅 문맥(제목/키워드)]: {context}" if context else ""
        enhance_prompt = f"""
당신은 DALL-E, Midjourney, Imagen 같은 AI 이미지 제너레이터 프롬프트 작성 전문가입니다.
사용자가 IT 테크 블로그에 삽입할 이미지의 간략한 상황 설명이나 키워드를 줄 것입니다.

[지침]:
1. 최고 품질의 이미지를 생성할 수 있는 매우 상세한 영문 프롬프트(Prompt)로 확장해주세요.
2. 반드시 영어로만 출력하며, 뻔한 스톡 사진(Cinematic, Photorealistic) 느낌을 철저히 배제하십시오.
3. **핵심 규칙**: 모든 이미지는 반드시 "Modern IT Tech Illustration" 컨셉을 유지해야 합니다. 
   - **어떠한 경우에도 사람(인물, 캐릭터, 신체 부위 등)을 절대 그리지 마십시오.** (Strictly NO humans, NO characters, NO people)
   - 절대 오토바이, 음식(햄버거 등), 무관한 사물, 평범한 자연 풍경 등을 그리지 마십시오.
   - 대신 "High-quality modern tech illustration, engaging editorial style, conceptual flat design, clean background" 스타일을 사용하십시오.
4. AI 텍스트 렌더링 오류를 막기 위해 "no text, no letters, no labels, no complex charts"라는 부정 프롬프트를 융합하십시오.{context_str}

[이미지 플레이스홀더 설명]: {base_prompt}
"""
        response = client.models.generate_content(
            model='models/gemini-3-flash-preview',
            contents=enhance_prompt
        )
        enhanced = response.text.strip()
        print(f"✨ 프롬프트 증강 완료 (문맥반영: {'O' if context else 'X'}): {enhanced[:80]}...")
        return enhanced
    except Exception as e:
        print(f"⚠️ 프롬프트 증강 실패, 원본을 사용합니다: {e}")
        return base_prompt

def generate_image(prompt, output_filename, context=None):
    """
    Imagen 모델들을 순차적으로 시도하여 이미지를 생성하고 지정된 포맷으로 저장합니다.
    context(제목/키워드)를 받아 이미지의 맥락을 강화합니다.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ GEMINI_API_KEY가 .env 파일에 없습니다.")
        return None, "API Key Missing"

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
                'person_generation': 'DONT_ALLOW'
            }
        )

    # 1. 프롬프트 증강 (Prompt Enhancement - 문맥 반영)
    enhanced_prompt = enhance_image_prompt(prompt, client, context=context)

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
                return output_filename, None
            else:
                last_error = f"{model_name}: No image generated (Safety filter?)"
                print(f"⚠️ {last_error}. 다음 모델로 넘어갑니다.")
                
        except exceptions.NotFound:
            last_error = f"{model_name}: Not Found (404)"
            print(f"ℹ️ {last_error}")
        except exceptions.ResourceExhausted:
            last_error = f"{model_name}: Rate Limit (429)"
            print(f"⏳ {last_error}")
        except Exception as e:
            last_error = f"{model_name}: {str(e)[:100]}"
            print(f"⚠️ {last_error}...")
            
        # 다음 모델 시도 환경 조성
        continue

    print(f"❌ 모든 Imagen 모델 시도가 실패했습니다. 마지막 에러: {last_error}")
    return None, last_error

if __name__ == "__main__":
    # 단독 테스트용
    test_outfile = "test_fallback_imagen.png"
    generate_image("A highly detailed futuristic data center with neon lights, isometric view, cinematic lighting", test_outfile)
