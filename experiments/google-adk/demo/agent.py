from google.adk.agents import Agent

def addition(a:str, b:str)->str:
    """Returns the sum of two numbers."""
    print(f"Adding {a} and {b}")
    return str(int(a)+int(b))

root_agent = Agent(
    name="calci_agent",
    model="gemini-2.0-flash-lite",
    description="This agent can perform basic arithmetic calculations like addition, subtraction, multiplication, and division. ",
    instruction="You are a calculator agent. you can only perform addition. you have to use the addition tool to perform addition. Before using the tool, you have to ask the user a confirmation of the two numbers to be added.",
    tools=[addition],
)