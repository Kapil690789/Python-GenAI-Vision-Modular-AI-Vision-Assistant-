import os
import logging
import time
from dotenv import load_dotenv
from huggingface_hub import InferenceClient  # Official Library

# Setup Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class HuggingFaceGenerator:
    def __init__(self):
        load_dotenv()
        self.api_token = os.getenv("HF_TOKEN")
        if not self.api_token:
            logger.error("Hugging Face Token is missing!")
            raise ValueError("HF_TOKEN not found in .env file")

        # Initialize the Official Client
        # We use Stable Diffusion XL (SDXL) as it is reliable and free via API
        self.model_id = "stabilityai/stable-diffusion-xl-base-1.0"
        self.client = InferenceClient(model=self.model_id, token=self.api_token)

    def generate_image(self, prompt: str) -> str:
        """
        Generates an image using the official Hugging Face InferenceClient.
        """
        try:
            logger.info(f"Sending prompt to Hugging Face ({self.model_id}): {prompt}")
            
            # The Magic Line: Generates image directly
            image = self.client.text_to_image(prompt)
            
            # Save locally with timestamp
            timestamp = int(time.time())
            output_file = f"hf_generated_{timestamp}.png"
            
            # Save the PIL image
            image.save(output_file)
            
            logger.info(f"Image saved successfully: {output_file}")
            return output_file
            
        except Exception as e:
            logger.error(f"Generation Failed: {e}")
            return None