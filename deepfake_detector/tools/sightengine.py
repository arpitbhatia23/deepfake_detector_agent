import os
import requests
from google.genai import types
from google.adk.tools import ToolContext
from google.adk.agents.callback_context import CallbackContext

from ..logger.logger import logger


async def detect_deepfake(
     filename:str,tool_context:ToolContext
) -> dict:
    """
    Scans an uploaded image (stored as an ADK artifact) to detect deepfake manipulation
    and AI generation.

    Args:
        artifact_filename: The artifact filename used when saving the image.

    Returns:
        A dictionary containing deepfake probability scores or an error.
    """
    try:
        # Load the artifact once
        logger.info("loading artifact")
        part: types.Part = await tool_context.load_artifact(filename=filename)

        if not part or not getattr(part, "inline_data", None):
            return {
                "error": f"Artifact '{filename}' not found or has no inline data",
                "score": 0.0,
            }
        logger.info("convert image into bytes")


        image_bytes = part.inline_data.data
        mime_type = part.inline_data.mime_type
        api_user = os.getenv("api_user")
        api_secret = os.getenv("api_secret")
        data = {
            "models": "deepfake,genai", # Use multiple models for better coverage
            "api_user": api_user,
            "api_secret": api_secret,
        }

        # 2. Define the files dictionary using your extracted data
        # The tuple format is: ('filename_for_api', data_in_bytes, 'mime_type')
        files = {
            "media": ("image", image_bytes, mime_type)
        }
        # Example: send to Sightengine (uncomment and set env vars)
        
        if not api_user or not api_secret:
            return {"error": "Sightengine credentials not configured", "score": 0.0}
        try:
            logger.info("sending image for aigenrated dtection ...")

            response = requests.post(
                "https://api.sightengine.com/1.0/check.json",
                files=files,
                data=data,
                timeout=30,
            )
            result = response.json()
            return {"result": result, "score": result.get("deepfake", {}).get("prob", 0.0)}
        except Exception as err:
            return {"error":f" Failed to load result {err}"}

        

    except Exception as e:
        return {
            "error": f"Failed to load or process artifact '{filename}': {str(e)}",
            "score": 0.0,
        }
