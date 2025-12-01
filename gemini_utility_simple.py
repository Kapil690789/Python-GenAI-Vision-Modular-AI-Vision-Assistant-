import os
import logging
from typing import Optional, Union, List  # Type Hinting tools
from dotenv import load_dotenv
from google import genai
from google.genai import types
from PIL import Image

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class GeminiProcessor:
    def __init__(self):
        """
        Initialize the Gemini Client. 
        This is called automatically when you create an instance of the class.
        """
        load_dotenv()
        self.api_key: Optional[str] = os.getenv("GOOGLE_API_KEY")
        
        if not self.api_key:
            logger.error("GOOGLE_API_KEY not found in environment variables!")
            raise ValueError("Missing API Key")
            
        try:
            self.client = genai.Client(api_key=self.api_key)
            logger.info("Gemini Client connected successfully.")
        except Exception as e:
            logger.critical(f"Failed to connect to Google API: {e}")
            raise

    def analyze_image(self, image_path: str, prompt: str = "Describe this image") -> Optional[str]:
        """
        Sends an image to Gemini and returns the text description.
        
        Args:
            image_path (str): The file path to the image.
            prompt (str): The instruction for the model.
            
        Returns:
            Optional[str]: The description text, or None if it fails.
        """

        logger.info(f"Processing image: {image_path}")

        try:
            image = Image.open(image_path)
        except FileNotFoundError:
            logger.error(f"File not found: {image_path}")
            return None
        except Exception as e:
            logger.error(f"Error opening image: {e}")
            return None
        
        try:
            logger.info("Sending request to Gemini model...")
            response = self.client.models.generate_content(
            model = "gemini-2.0-flash",
            config = types.GenerateContentConfig(
                system_instruction="You are a Technical AI Vision Assistant. Be precise.",
                    temperature=0.5,
            ),
            contents=[image, prompt]
            )
            logger.info("Response received successfully.")
            return response.text
        except Exception as e:
            logger.error(f"API Error during generation: {e}")
            return None
    
    def save_to_file(self, text: str, filename: str = "result.md") -> bool:
        """Saves text to a markdown file safely."""
        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(text)
            logger.info(f"Result saved to {filename}")
            return True
        except Exception as e:
            logger.error(f"Failed to save file: {e}")
            return False


if __name__ == "__main__":
    processor = GeminiProcessor()
    
    my_image = "input_images/ferraribadge.png"
    my_prompt = "Describe the lighting and composition of this image."

    result_text = processor.analyze_image(my_image,my_prompt)

    if result_text:
        processor.save_to_file(result_text)
    else:
        logger.warning("No result was generated.")

        