import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

def generate_image(prompt, output_filename):
    """
    Generates an image using Imagen via Gemini API (Google AI Studio).
    Requires: GEMINI_API_KEY set in environment.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY not found in .env")
        return None

    try:
        client = genai.Client(api_key=api_key)
        
        print(f"Generating image with Imagen for prompt: {prompt[:100]}...")
        
        # Try Imagen 3.0 first as it's the requested version
        model_name = 'imagen-4-fast-generate-001'
        
        # Note: In the new SDK, it is plural 'generate_images' and config can be a dict
        response = client.models.generate_images(
            model=model_name,
            prompt=prompt,
            config={
                'number_of_images': 1,
                'aspect_ratio': '1:1'
            }
        )
        
        # Save the first image from the response
        if response.generated_images:
            response.generated_images[0].image.save(output_filename)
            print(f"Image saved to {output_filename}")
            return output_filename
        else:
            print(f"Error: No images generated in response.")
            return None
            
    except Exception as e:
        print(f"Error generating image with Imagen 3.0: {e}")
        # If 404, try Imagen 4.0 as a fallback
        if "404" in str(e):
            try:
                print("Imagen 3.0 not found, trying Imagen 4.0...")
                model_name = 'imagen-4.0-generate-001'
                response = client.models.generate_images(
                    model=model_name,
                    prompt=prompt,
                    config={
                        'number_of_images': 1,
                        'aspect_ratio': '1:1'
                    }
                )
                if response.generated_images:
                    response.generated_images[0].image.save(output_filename)
                    print(f"Image saved via Imagen 4.0 to {output_filename}")
                    return output_filename
            except Exception as e2:
                print(f"Error in Imagen 4.0 fallback: {e2}")
        return None

if __name__ == "__main__":
    # Test
    test_outfile = "test_image.png"
    generate_image("A futuristic 3D workspace with soft synthwave lighting, high quality, 8k", test_outfile)
