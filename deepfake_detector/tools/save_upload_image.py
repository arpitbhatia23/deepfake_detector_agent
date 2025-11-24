from google.adk.tools.tool_context import ToolContext
from google.genai import types
from datetime import datetime

from ..logger.logger import logger

async def save_uploaded_image(tool_context: ToolContext) -> str:

    logger.info("🔍 Searching session history for image...")

    session = tool_context.session
    image_data = None
    mime_type=None

    # 1. Reverse loop to find the LATEST upload
    for event in reversed(session.events):
        
        # 2. Safety Check: Ignore system events or events without content
        if not event.content or not event.content.parts:
            continue

        # 4. Loop through the parts of the message
        for part in event.content.parts:
            
            # 5. Check for inline_data (The Python SDK uses snake_case)
            # In the JSON it is 'inlineData', but in Python code it is 'inline_data'
            if part.inline_data and part.inline_data.data:
                logger.info("✅ Found Inline Data in Event!")
                image_data = part.inline_data.data
                mime_type=part.inline_data.mime_type
                break # Stop looking through parts
        
        if image_data:
            break # Stop looking through events

    if not image_data:
        logger.info("❌ DEBUG: No image found. Printing last event to help debug:")
        if session.events:
            logger.info(session.events[-1])
        return "Error: No image data found in the event history."

    # --- If we are here, we have the data ---
    logger.info(f"🔥 RAW BYTES EXTRACTED: {len(image_data)} bytes")
    
    # Proceed to save...
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"upload_{timestamp}" 
    image_part = types.Part(
    inline_data=types.Blob(
        data=image_data,
        mime_type=mime_type
    )
    )   
    await tool_context.save_artifact(filename, image_part)
    
    return f"Image saved as {filename}"
