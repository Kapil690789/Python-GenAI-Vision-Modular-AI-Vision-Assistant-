import os
import json
import logging
from typing import Optional, Dict
from dotenv import load_dotenv
from google import genai
from google.genai import types
from PIL import Image
import requests 
import io 

# Logging Setup
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class GeminiProcessor:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("API Key Missing")
        self.client = genai.Client(api_key=self.api_key)
        self.model_name = "gemini-2.0-flash"

    # FUNCTION 1: Img2Text (General Description)--
    def img_to_text(self, image_path: str, prompt: str) -> Optional[str]:
        try:
            image = Image.open(image_path)
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=[image, prompt]
            )
            return response.text
        except Exception as e:
            logger.error(f"Img2Text Error: {e}")
            return None

    def img_to_json(self, image_path: str) -> Optional[Dict]:
        prompt = """
        Analyze image. Return ONLY raw JSON (no backticks):
        {"item": "str", "color": "str", "material": "str", "brand_guess": "str"}
        """
        try:
            image = Image.open(image_path)
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=[image, prompt]
            )
            clean_json = response.text.replace("```json", "").replace("```", "").strip()
            return json.loads(clean_json)
        except Exception as e:
            logger.error(f"Img2Json Error: {e}")
            return None

    
    def text_to_text(self, prompt : str) -> Optional[str]:
        try:
            response = self.client.models.generate_content(
                model = self.model_name,
                contents  = prompt
            )
            return response.text;
        except Exception as e:
            logger.error(f"Text2Text Error: {e}")
            return None

    # def generate_image(self, prompt: str) -> Optional[str]:
    #     """
    #     Generates an image using Google's Imagen model.
    #     Returns the path to the saved image.
    #     """
    #     try:
    #         # Note: Model name might change based on your access (e.g., 'imagen-3.0-generate-001')
    #         # If 'imagen-3.0' doesn't work, try 'imagen-2.0'
    #         target_model = "imagen-2.0-generate-001" 
            
    #         response = self.client.models.generate_image(
    #             model=target_model,
    #             prompt=prompt,
    #             config=types.GenerateImageConfig(
    #                 number_of_images=1,
    #             )
    #         )
            
    #         # Google returns raw bytes, we need to save it
    #         if response.generated_images:
    #             image_bytes = response.generated_images[0].image.image_bytes
                
    #             # Save locally
    #             output_file = "generated_image.png"
    #             with open(output_file, "wb") as f:
    #                 f.write(image_bytes)
    #             return output_file
                
    #         return None
            
    #     except Exception as e:
    #         logger.error(f"Text2Image Error: {e}")
    #         return None

    def generate_image(self, prompt: str) -> Optional[str]:
        """
        Generates an image using Pollinations.ai (No API Key required).
        """
        try:
            # Pollinations URL format: https://image.pollinations.ai/prompt/{your_prompt}
            # We replace spaces with %20 just to be safe, though requests handles it.
            clean_prompt = prompt.replace(" ", "%20")
            url = f"https://image.pollinations.ai/prompt/{clean_prompt}"
            
            logger.info(f"Generating image from: {url}")
            
            # Fetch the image
            response = requests.get(url)
            
            if response.status_code == 200:
                # Save locally
                output_file = "generated_image.png"
                with open(output_file, "wb") as f:
                    f.write(response.content)
                logger.info("Image saved successfully.")
                return output_file
            else:
                logger.error(f"Pollinations Error: {response.status_code}")
                return None
            
        except Exception as e:
            logger.error(f"Text2Image Error: {e}")
            return None