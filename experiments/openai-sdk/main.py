from dotenv import load_dotenv
from agents import Agent, Runner

load_dotenv()

agent = Agent(name="Assistant", instructions="You are a helpful assistant", model="gpt-4.1-nano")

result = Runner.run_sync(agent, "who is the founder of OpenAI?")
print(result.final_output)