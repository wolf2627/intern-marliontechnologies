from google.adk.models.lite_llm import LiteLlm
from google.adk.agents import Agent
from .util import load_instruction_from_file

# For getting current date and time in a specified timezone : get_current_datetime tool.
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
import datetime
import requests

from PIL import Image
from io import BytesIO

import base64

# tool 1 : # Get current date and time in a specified timezone
def get_current_datetime(timezone: str = "Asia/Kolkata") -> dict:
    """Gives Current Date, time and timezone information.
    
    Args:
        timezone (str): The timezone to get the current date and time for. Default is "Asia/Kolkata".
    
    Returns:
        dict: A dictionary containing the current date, time, and timezone.
              Includes a 'status' key ('success' or 'error').
              If 'success', includes 'date', 'time', and 'timezone' keys.
              If 'error', includes an 'error_message' key.
    """
    try:
        tz = ZoneInfo(timezone)
        now = datetime.datetime.now(tz)
        return {
            "current_time": now.strftime("%H:%M:%S"),
            "current_date": now.strftime("%Y-%m-%d"),
            "timezone_name": now.astimezone().tzname(),
            "timezone_offset": now.strftime("%z"),
            "full_datetime": now.strftime("%Y-%m-%d %H:%M:%S %Z%z")
        }
    except ZoneInfoNotFoundError:
        return {
            "error": f"Invalid timezone: {timezone}. Please provide a valid IANA timezone string."
        }
    except Exception as e:
        return {
            "error": f"An unexpected error occurred: {str(e)}"
        }


#subagent 1: Project Details fetcher
# project_explainer = Agent(
#     name="project_explainer",
#     model=LiteLlm(model="openai/gpt-4.1-nano"),
#     description="Provides detailed information about the construction project.",
#     instruction=load_instruction_from_file('project_explainer.txt'),
#     output_key="project_overview"
# )

# subagent 2: Project Timeline and Milestones
# timeline_explainer = Agent(
#     name="timeline_explainer",
#     model=LiteLlm(model="openai/gpt-4.1-nano"),
#     description="Explains the timeline and milestones of the construction project.",
#     instruction=load_instruction_from_file('timeline_explainer.txt'),
#     output_key="project_timeline"
# )

# Tool that returns image from a URL
def fetch_image_from_url(url: str) -> dict:
    """
    Fetches an image from the given URL and returns its binary content and metadata.
    Args:
        url (str): The URL of the image to fetch.
    Returns:
        dict: Contains 'status', 'content', 'content_type', and 'url' if successful, or 'error' if failed.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        content_type = response.headers.get('Content-Type', '')
        if not content_type.startswith('image/'):
            return {"error": f"URL does not point to an image. Content-Type: {content_type}"}
        print(f"Fetched image from {url} with content type {content_type}")
        image_bytes = response.content
        image_base64 = base64.b64encode(image_bytes).decode('utf-8')
        return {
            "status": "success",
            "image_base64": image_base64,
            "content_type": content_type,
            "url": url
        }
    except Exception as e:
        return {"error": str(e)}

supervisor = Agent(
    name="supervisor",
    # model=LiteLlm(model="openai/gpt-4.1-nano"),
    model="gemini-2.5-flash",
    description="Provides up-to-date information from the internet (using GPT-4.1-nano).",
    instruction=load_instruction_from_file('supervisor.txt'),
    tools=[get_current_datetime, fetch_image_from_url],
    # sub_agents=[project_explainer, timeline_explainer],
) 

root_agent = supervisor