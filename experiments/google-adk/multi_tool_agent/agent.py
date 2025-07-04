from google.adk.agents import LlmAgent, BaseAgent

# Define individual agents
greeter = LlmAgent(name="greeter", model="gemini-2.0-flash-lite")
task_executor = LlmAgent(name="task_executor", model="gemini-2.0-flash-lite")

# Create parent agent and assign children via sub_agents
root_agent = LlmAgent(
    name="Coordinator",
    model="gemini-2.0-flash-lite",
    description="I coordinate greetings and tasks.",
    sub_agents=[ # Assign sub_agents here
        greeter,
        task_executor
    ]
)