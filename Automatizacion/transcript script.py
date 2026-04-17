import os
import base64
from openai import OpenAI

# --- SET YOUR FOLDERS HERE ---
input_folder = r"C:\Users\YOUR_PATH_HERE\input"
output_folder = r"C:\Users\YOUR_PATH_HERE\input"

# Point the program to LM Studio's Local Server
client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

def encode_image(image_path):
    """Converts the image into a format the AI can read."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Create output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Get a list of all images in the folder
valid_extensions = ('.png', '.jpg', '.jpeg')
files = [f for f in os.listdir(input_folder) if f.lower().endswith(valid_extensions)]

print(f"Found {len(files)} images. Starting transcription...")

# Loop through every image file
for filename in files:
    print(f"\nProcessing: {filename}...")
    image_path = os.path.join(input_folder, filename)
    
    # 1. Convert image to base64
    base64_image = encode_image(image_path)
    
    # 2. Send to LM Studio
    try:
        response = client.chat.completions.create(
            model="local-model", # LM Studio automatically uses whatever model you have loaded
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text", 
                            "text": "Transcribe el texto de esta imagen a solo texto, no resumas nada, dame el texto literal"
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            temperature=0.0, # Keeps the AI focused and less "creative"
        )
        
        # 3. Get the text the AI replied with
        transcription = response.choices[0].message.content
        
        # 4. Save to a text file with the same name
        name_without_extension = os.path.splitext(filename)[0]
        text_filename = f"{name_without_extension}.txt"
        text_filepath = os.path.join(output_folder, text_filename)
        
        with open(text_filepath, "w", encoding="utf-8") as text_file:
            text_file.write(transcription)
            
        print(f"Success! Saved to {text_filename}")

    except Exception as e:
        print(f"Error processing {filename}: {e}")

print("\nAll done! You can now turn off the server in LM Studio.")