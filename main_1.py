import os 
from PIL import Image
output_folder = "output_images"
input_folder = "input_images" 

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

print("Processing started...")

for filename in os.listdir(input_folder):

    if filename.endswith(("jpg","png","jpeg")):
        try:
            image_path = os.path.join(input_folder, filename)

            with Image.open(image_path) as img:

                img = img.resize((800,800))

                if img.mode in ("RGBA", "P"):
                    img = img.convert("RGB")
                
                new_filename = os.path.splitext(filename)[0] + ".jpg" 
                save_path = os.path.join(output_folder, new_filename)

                img.save(save_path, "JPEG", quality=80)
                print(f"✅ Success: {filename} -> {new_filename}")


        except Exception as e:
            print(f"❌ Error processing {filename}: {e}") 

print("All done! Check the output_images folder.")