from google.adk.agents import Agent


root_agent = Agent(
    name="vision_safety_agent",
    model="gemini-2.5-flash",        # or gemini-pro-vision
    instruction="Spot safety hazards in construction images."
)

import requests

response_img = requests.get("https://www.leavitt.com/dA/b23b96683d/featuredImage/blog-construction.jpg/1200w/webp/50q")
img_bytes = response_img.content

response = root_agent.run(
    parts=[
        TextPart(text="Identify PPE violations."),
        Part.from_bytes(img_bytes, mime_type="image/jpeg")
    ]
)
print(response.text)
