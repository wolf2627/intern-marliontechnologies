from google.adk.models.lite_llm import LiteLlm
from google.adk.agents import Agent
import requests # For making HTTP requests
import json # For JSON handling
import datetime

MODEL = "openai/gpt-4.1-nano"




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
    instruction="You are a helpful assistant powered by GPT-4.1-nano. "
                "Use `browse_internet` tool to browse the internet."
                "Analyse the response from the `browse_internet` tool and give concise answer for the query.",
    tools=[browse_internet]
)