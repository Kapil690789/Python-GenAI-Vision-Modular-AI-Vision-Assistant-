import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from PIL import Image
load_dotenv()

my_api_key = os.getenv("GOOGLE_API_KEY")

client = genai.Client(api_key = my_api_key)
img_path = "input_images/imola_preview.png"
try:
    image = Image.open(img_path)
except FileNotFoundError:
    print(f"Error: Could not find {image_path}. Please add an image file.")
    pass

sys_instrustion = "You are a Computer Vision Expert. You analyze images and describe them technically."
print("Analyzing image... please wait.")

response = client.models.generate_content(
    model="gemini-2.0-flash",
    config = types.GenerateContentConfig(
        system_instruction=sys_instrustion,
        temperature = 0.5,
    ),
    # contents="Write a function to calculate the factorial of a number."
    contents = [image,"Describe this image in detail."]
)

output_filename = "readme.md"

with open(output_filename, 'w', encoding='utf-8') as f:
    f.write("# Image Analysis Report\n\n")
    f.write("## Analyzed Image\n")
    f.write(f"![Analyzed Image]({img_path})\n\n")
    f.write("## Analysis Result\n\n")
    f.write(response.text)

print(f"Done! Check the file: {output_filename}")
# print(response.text);