from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from ..prompts.advisor_agent_prompt import ADVISOR_PROMPT
from ..config import retry_config
advisor_agent = Agent(
    model=Gemini(model="gemini-2.5-flash",retry_options=retry_config),
    name="advisor_agent",
    description="Agent to give advise",
    instruction=ADVISOR_PROMPT,
    output_key="advisor_agent_output"
    
)


