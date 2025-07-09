import google.generativeai as genai
import requests
from PIL import Image
from io import BytesIO

# Replace with your own API key
GEMINI_API_KEY = "AIzaSyClPSy6TVz8LkZF7boQm2T3TT571TUjNKE"

# Initialize Gemini API
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")

# Image link (assumed uploaded on your server)
image_url = "https://www.pnkconstructions.co.in/assets/images/project/a8.jpg"
# image_url = "http://192.168.1.8:8000/photos/c2.jpg"
# Prompt to analyze the image
prompt = """You are acting as a human supervisor for a construction site. You are given an image of an active construction area. Based on this image, perform the following tasks:

1. *Count the total number of workers visible in the image.*
2. *Determine how many workers appear to be actively working or engaged in tasks (e.g., handling tools, operating machinery, performing labor).*
3. *Assess the current stage of construction (e.g., foundation, framing, roofing, finishing).*
4. *Evaluate how many workers are wearing helmets or hard hats, as a key safety compliance metric.*

Provide your response in the following format:


No of Workers: <workers count>
No of workers working properly: <count>
Current stage: <brief description>
Workers wearing helmet: <count>


Be as accurate as possible based on the visual evidence in the image.

if the image is not relevant to construction, just say "I can only analyse construction sites"
"""

# Download image
response = requests.get(image_url)
if response.status_code != 200:
    print("Failed to download image")
    exit()

image = Image.open(BytesIO(response.content))

print("Image Loaded Successfully..Analyzing...")

# Send image + prompt to Gemini
response = model.generate_content(
    [prompt, image],
    stream=False,
)

# Output the result
#print("\n--- Gemini Output ---\n")
print(response.text)
