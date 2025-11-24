from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from ..prompts.nsfw_agent_prompt import NSFW_PROMPT
from ..config import retry_config
nsfw_detector = Agent(
    model=Gemini(model="gemini-2.5-flash",retry_options=retry_config),
    name="nsfw_checker_agent",
    description="Agent to detect if an image is NSFW.",
    instruction=NSFW_PROMPT,
    output_key="nsfw_detector"
    
)


