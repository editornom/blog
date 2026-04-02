import os
from google.cloud import aiplatform
from vertexai.preview.vision_models import ImageGenerationModel
from dotenv import load_dotenv
import requests

load_dotenv()

def generate_image(prompt, output_filename):
    """
    Generates an image using Imagen 3 via Google Cloud Vertex AI and saves it to the specified path.
    Requires: GCP_PROJECT_ID and GOOGLE_APPLICATION_CREDENTIALS set in environment.
    """
    project_id = os.getenv("GCP_PROJECT_ID")
    if not project_id:
        print("Error: GCP_PROJECT_ID not found in .env")
        return None

    try:
        aiplatform.init(project=project_id, location="us-central1")
        # Load Imagen 3 model (official name in Vertex AI)
        model = ImageGenerationModel.from_pretrained("imagen-3.0-generate-001")
        
        print(f"Generating image for prompt: {prompt[:100]}...")
        
        response = model.generate_images(
            prompt=prompt,
            number_of_images=1,
            language="en",
            aspect_ratio="1:1" # Standard for bento grid
        )
        
        # Save the first image
        response.images[0].save(location=output_filename, include_generation_parameters=False)
        print(f"Image saved to {output_filename}")
        return output_filename
        
    except Exception as e:
        print(f"Error generating image: {e}")
        # Return none or potentially an error code
        return None

if __name__ == "__main__":
    # Test (requires GCP auth)
    test_outfile = "test_image.png"
    generate_image("A futuristic 3D workspace with soft synthwave lighting, high quality, 8k", test_outfile)
