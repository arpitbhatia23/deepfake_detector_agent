import logging

logging.basicConfig(
    level=logging.DEBUG,
    format=' %(levelname)s  - %(message)s'
)


from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from google.adk.runners import Runner
from google.adk.artifacts import InMemoryArtifactService
from google.adk.tools.function_tool import FunctionTool
from google.adk.sessions import InMemorySessionService
from google.adk.tools.agent_tool import AgentTool

from .tools.sightengine import detect_deepfake
from .tools.save_upload_image import save_uploaded_image

from .subagents.nsfw_agent import nsfw_detector
from .subagents.advisor_agent import advisor_agent

from .prompts.root_agent_prompt import SYSTEM_PROMPT

from .config import retry_config
model = Gemini(
    model_name="gemini-1.5-flash",
    retry_options=retry_config
)

# Ensure this directory exists
artifact_service = InMemoryArtifactService()








# 3. Create Agent
root_agent = Agent(
    name="deepfake_guard",
    model=model,
    # Tool requires NO arguments from LLM
    tools=[FunctionTool(save_uploaded_image),FunctionTool(detect_deepfake),AgentTool(nsfw_detector), AgentTool(advisor_agent)],
    instruction=SYSTEM_PROMPT,
)

print("✅ Artifact Service Ready")

runner = Runner(
    app_name="deepfake_detector",
    agent=root_agent,
    session_service=InMemorySessionService(),
    artifact_service=artifact_service,
)