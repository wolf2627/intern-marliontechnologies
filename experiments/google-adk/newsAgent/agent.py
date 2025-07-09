from google.adk.models.lite_llm import LiteLlm
from google.adk.agents import Agent
import requests # For making HTTP requests
import json # For JSON handling
import datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
from .util import load_instruction_from_file

MODEL = "openai/gpt-4.1-nano"

def get_current_datetime(timezone: str = "Asia/Kolkata")->dict:
    """Gives Current Date, time and timezone information.
    Args:
        timezone (str): The timezone to get the current date and time for. Default is "Asia/Kolkata".
    Returns:
        dict: A dictionary containing the current date, time, and timezone.
              Includes a 'status' key ('success' or 'error').
              If 'success', includes 'date', 'time', and 'timezone' keys.
              If 'error', includes an 'error_message' key.
    """
    print(f"--- Tool: get_current_datetime called with timezone: {timezone} ---")

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

def browse_internet(query: str) -> dict:
    """Retrieves information from the internet based on a query.

    Args:
        query (str): The search query to retrieve information for.

    Returns:
        dict: A dictionary containing the search results.
              Includes a 'status' key ('success' or 'error').
              If 'success', includes a 'results' key with search results.
              If 'error', includes an 'error_message' key.
    """
    print(f"--- Tool: browse_internet called with query: {query} ---")  # Log tool execution

    try:
        response = requests.post(
            url="https://api.langsearch.com/v1/web-search",
            headers={
                'Content-Type': 'application/json',
                'Authorization': 'Bearer sk-47e8adcb9c3d4823a41180fa8773a69b',
            },
            data=json.dumps({
                "query": query,
                "freshness": "noLimit",
                "summary": True,
                "count": 5
            })
        )
        
        if response.status_code == 200:
            return {
                "status": "success",
                "results": response.json()
            }
        else:
            return {
                "status": "error",
                "error_message": f"Failed to retrieve data: {response.status_code}"
            }
    except Exception as e:
        return {
            "status": "error",
            "error_message": str(e)
        }
    

root_agent = Agent(
    name="uptodate_agent",
    model=LiteLlm(model=MODEL),
    description="Provides up-to-date information from the internet (using GPT-4.1-nano).",
    instruction=load_instruction_from_file('uptodate.txt'),
    tools=[browse_internet, get_current_datetime],
)