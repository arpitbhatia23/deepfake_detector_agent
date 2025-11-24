# Deepfake Detector - Complete Documentation

## Table of Contents

1. [Overview](#overview)
2. [Problem Statement](#problem-statement)
3. [Solution](#solution)
4. [Architecture](#architecture)
5. [Features](#features)
6. [Setup Instructions](#setup-instructions)
7. [Usage](#usage)
8. [API Documentation](#api-documentation)
9. [Configuration](#configuration)
10. [Troubleshooting](#troubleshooting)
11. [Project Structure](#project-structure)
12. [Security Considerations](#security-considerations)
13. [Performance Metrics](#performance-metrics)
14. [Future Enhancements](#future-enhancements)
15. [Support & Resources](#support--resources)

---

## Overview

**Deepfake Detector** is an intelligent safety analysis system that processes user-uploaded images through a comprehensive five-step security verification pipeline. It detects deepfakes, identifies AI-generated content, flags NSFW material, and provides actionable safety advice to users.

### Key Technologies:

- Google AI (Gemini 2.5-Flash)
- Google ADK (Agent Development Kit)
- Sightengine API for deepfake detection
- Python 3.12+

---

## Problem Statement

### The Challenge

With the rise of AI-generated content and deepfake technology, users face critical risks:

- **Malicious Image Distribution:** Deepfakes used in extortion, harassment, or fraud
- **NSFW Content:** Inappropriate or explicit material requiring detection
- **Authentication Issues:** Users cannot easily verify image authenticity
- **Lack of Guidance:** Victims don't know what actions to take after detection

### Impact

- Victims of image-based abuse lack automated tools for verification
- Manual analysis is time-consuming and unreliable
- No clear pathway for users to respond to threats

---

## Solution

### How It Works

The Deepfake Detector implements a **multi-agent orchestration system** that:

1. **Saves & Extracts** image data from user uploads
2. **Analyzes for Deepfakes** using Sightengine's advanced AI models
3. **Detects NSFW Content** using Gemini's vision capabilities
4. **Interprets Results** and provides compassionate, actionable advice
5. **Returns Guidance** tailored to threat level

### Key Benefits

✅ **Automated Analysis** - No manual intervention needed  
✅ **Multi-Model Detection** - Combines deepfake + NSFW analysis  
✅ **Contextual Advice** - Threat-level-based recommendations  
✅ **Evidence Preservation** - Stores artifacts for user records  
✅ **User-Centric** - Designed with empathy for potential victims

---

## Architecture

### System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    ROOT AGENT (Orchestrator)                │
│              "Safety and Authenticity Analysis Bot"          │
└─────────────────────────────────────────────────────────────┘
                              │
                ┌─────────────┼─────────────┐
                │             │             │
        ┌───────▼────────┐   │   ┌─────────▼────────┐
        │  STEP 1: SAVE  │   │   │ STEP 2: DEEPFAKE │
        │     IMAGE      │   │   │    DETECTION     │
        │                │   │   │                  │
        │ save_uploaded  │   │   │ detect_deepfake  │
        │    _image()    │   │   │   (Sightengine)  │
        └────────────────┘   │   └──────────────────┘
                             │
                ┌────────────┴────────────┐
                │                         │
        ┌───────▼──────────┐    ┌────────▼─────────┐
        │ STEP 3: NSFW     │    │  STEP 4: ADVICE  │
        │   DETECTION      │    │   GENERATION     │
        │                  │    │                  │
        │  nsfw_detector   │    │  advisor_agent   │
        │  (Subagent)      │    │   (Subagent)     │
        └──────────────────┘    └──────────────────┘
                │                        │
                └────────────┬───────────┘
                             │
                    ┌────────▼─────────┐
                    │ STEP 5: RETURN   │
                    │   FINAL ADVICE   │
                    │   TO USER        │
                    └──────────────────┘
```

### Component Breakdown

#### **Root Agent** (`agent.py`)

- Orchestrates the 5-step process
- Manages tool execution order
- Ensures data flows correctly between components

#### **Tools**

| Tool                    | File                   | Purpose                                         |
| ----------------------- | ---------------------- | ----------------------------------------------- |
| `save_uploaded_image()` | `save_upload_image.py` | Extracts and stores image artifacts             |
| `detect_deepfake()`     | `sightengine.py`       | Calls Sightengine API for AI/deepfake detection |

#### **Sub-Agents**

| Agent           | File               | Purpose                              |
| --------------- | ------------------ | ------------------------------------ |
| `nsfw_detector` | `nsfw_agent.py`    | Analyzes images for NSFW content     |
| `advisor_agent` | `advisor_agent.py` | Generates personalized safety advice |

#### **Prompts** (`prompts/`)

| Prompt           | File                      | Purpose                               |
| ---------------- | ------------------------- | ------------------------------------- |
| `SYSTEM_PROMPT`  | `root_agent_prompt.py`    | Root agent orchestration instructions |
| `NSFW_PROMPT`    | `nsfw_agent_prompt.py`    | NSFW detection criteria               |
| `ADVISOR_PROMPT` | `advisor_agent_prompt.py` | Safety advice logic                   |

### Data Flow Diagram

```
User Upload
    │
    ▼
┌─────────────────────────┐
│ Artifact Storage        │ ◄─── Saved as: upload_YYYYMMDD_HHMMSS
│ (InMemoryArtifactSvc)   │
└────────┬────────────────┘
         │
         ▼
    ┌────────────────────────────────────────┐
    │ Image Bytes Extracted (inline_data)    │
    │ - data: bytes                          │
    │ - mime_type: "image/jpeg" etc.         │
    └────────┬─────────────────────────────┘
             │
    ┌────────┴──────────┐
    │                   │
    ▼                   ▼
┌──────────────────┐ ┌──────────────────┐
│ Sightengine API  │ │ Gemini Vision    │
│ (Deepfake)       │ │ (NSFW Analysis)  │
│                  │ │                  │
│ Returns: {       │ │ Returns: {       │
│  "prob": 0.85    │ │  "is_nsfw": true │
│  ...             │ │  "category": ... │
│ }                │ │ }                │
└────────┬─────────┘ └──────────┬───────┘
         │                      │
         └──────────┬───────────┘
                    │
                    ▼
            ┌──────────────────┐
            │ Advisor Agent    │
            │ Interprets Scores│
            │ Generates Advice │
            └────────┬─────────┘
                     │
                     ▼
            ┌──────────────────┐
            │ Return to User   │
            │ (Advice Text)    │
            └──────────────────┘
```

---

## Features

### 🔍 **Deepfake Detection**

- Uses Sightengine's multi-model approach (deepfake + genai models)
- Returns probability scores (0.0 - 1.0)
- Detects AI-generated and manipulated images

### 🛡️ **NSFW Detection**

- Identifies nudity, sexually suggestive content
- Classifies content severity (0.0 - 1.0)
- Provides confidence levels for analysis

### 🤖 **Intelligent Advice**

- Threat-level-based responses (HIGH/MILD/LOW)
- Actionable safety steps
- Empathetic, non-judgmental guidance
- Emergency contacts and resource recommendations

### 📦 **Artifact Management**

- Automatic image storage with timestamps
- Session history tracking
- Evidence preservation for users

---

## Setup Instructions

### Prerequisites

- **Python:** 3.12+
- **pip:** Package manager
- **API Keys:**
  - Google AI API Key
  - Sightengine API credentials (user + secret)

### Step 1: Clone & Install

```bash
# Clone repository
git clone <repo-url>
cd deepfake_detector

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Configure Environment

Copy the example environment file:

```bash
cp deepfake_detector/.env.example deepfake_detector/.env
```

Edit `deepfake_detector/.env`:

```env
# Google AI Configuration
GOOGLE_GENAI_USE_VERTEXAI=0
GOOGLE_API_KEY="your_google_api_key_here"

# Sightengine Configuration
api_user="your_sightengine_user_key"
api_secret="your_sightengine_secret_key"
```

**How to get API Keys:**

#### Google API Key

1. Visit [Google AI Studio](https://aistudio.google.com/)
2. Click "Create API Key"
3. Copy the key to `.env`

#### Sightengine Credentials

1. Sign up at [Sightengine](https://sightengine.com/)
2. Get your API user & secret from the dashboard
3. Add to `.env`

### Step 3: Verify Installation

```bash
python -m pytest tests/  # If tests exist
# Or test manually:
python -c "from deepfake_detector.agent import root_agent; print('✅ Agent loaded successfully')"
```

---

## Usage

### Running the Application

#### Interactive Mode

```bash
python main.py
```

The runner will accept user input and process uploaded images through the analysis pipeline.

#### Example Workflow

```
User: [Uploads image via interface]
  ↓
Root Agent: "Processing image..."
  ↓
Step 1: "Image saved as upload_20240115_143022"
Step 2: "Deepfake score: 0.78"
Step 3: "NSFW detected: True (bikini, confidence: 0.92)"
Step 4: "HIGH THREAT - Immediate action recommended"
  ↓
Output:
"🚨 HIGH THREAT DETECTED
The analysis indicates a potential manipulated/AI-generated image combined
with suggestive content.

⚠️ IMMEDIATE ACTIONS:
1. Do not delete the original file - it's evidence
2. Change passwords on all linked accounts
3. Block the source immediately
4. Report to the platform's abuse team
5. Document all evidence (screenshots, links)

📞 Resources: [Local law enforcement, digital safety orgs]"
```

### Programmatic Usage

```python
from deepfake_detector.agent import runner

# Create a session
session = runner.create_session("unique_session_id")

# Send user message with image
response = runner.run(
    session_id="unique_session_id",
    user_message="Analyze this image for deepfakes",
    # Image is attached via the runner's interface
)

print(response)  # Final advice from advisor_agent
```

---

## API Documentation

### Tool: `save_uploaded_image()`

**Location:** `deepfake_detector/tools/save_upload_image.py`

**Purpose:** Extracts image data from session history and saves as an artifact

**Parameters:**

- `tool_context: ToolContext` - ADK context for artifact access

**Returns:**

```python
str  # "Image saved as upload_YYYYMMDD_HHMMSS"
```

**Example:**

```python
filename = await save_uploaded_image(tool_context)
# Returns: "Image saved as upload_20240115_143022"
```

---

### Tool: `detect_deepfake()`

**Location:** `deepfake_detector/tools/sightengine.py`

**Purpose:** Analyzes image for deepfake/AI generation using Sightengine API

**Parameters:**

- `filename: str` - Artifact filename from step 1
- `tool_context: ToolContext` - ADK context for artifact loading

**Returns:**

```python
{
    "result": {
        "deepfake": {"prob": 0.78},
        "genai": {"prob": 0.65},
        ...
    },
    "score": 0.78  # Deepfake probability
}
# Or on error:
{
    "error": "Error message",
    "score": 0.0
}
```

**Example Response:**

```json
{
  "result": {
    "deepfake": { "prob": 0.85 },
    "genai": { "prob": 0.72 },
    "status": "success"
  },
  "score": 0.85
}
```

---

### Sub-Agent: `nsfw_detector`

**Location:** `deepfake_detector/subagents/nsfw_agent.py`

**Purpose:** Analyzes image descriptions for NSFW content

**Input:**

```
Image description (text): "A woman in a bikini on a beach"
```

**Returns:**

```json
{
  "is_nsfw": true,
  "confidence_level": 0.92,
  "category": "bikini",
  "unsafe_score": 0.65
}
```

**Categories:**

- `nudity` - Full or partial nudity
- `bikini` - Bikini/swimwear
- `lingerie` - Lingerie/intimate apparel
- `sexual_content` - Explicit sexual material
- `safe` - No NSFW content

---

### Sub-Agent: `advisor_agent`

**Location:** `deepfake_detector/subagents/advisor_agent.py`

**Purpose:** Generates personalized safety advice based on threat levels

**Input:**

```python
{
    "deepfake_result": {"score": 0.85, ...},
    "nsfw_result": {"is_nsfw": True, "unsafe_score": 0.75, ...}
}
```

**Returns:**

```
🚨 HIGH THREAT DETECTED
[Actionable advice based on threat level]
```

**Threat Levels:**

- **HIGH:** Deepfake score > 0.7 OR (NSFW + Deepfake > 0.5)
- **MILD:** Any score > 0.4
- **LOW:** All scores < 0.4

---

## Configuration

### config.py

**Retry Configuration:**

```python
retry_config = types.HttpRetryOptions(
    attempts=5,                    # Max retries
    exp_base=7,                    # Exponential backoff multiplier
    initial_delay=1,               # Initial delay in seconds
    http_status_codes=[429, 500, 503, 504]  # Codes to retry on
)
```

**Adjust for your needs:**

```python
# More aggressive retries:
retry_config = types.HttpRetryOptions(
    attempts=10,
    exp_base=5,
    initial_delay=2,
    http_status_codes=[429, 500, 502, 503, 504]
)
```

### Model Configuration

Edit `agent.py` to change models:

```python
# Root Agent Model
model = Gemini(
    model_name="gemini-2.0-flash",  # Change model here
    retry_options=retry_config
)

# Sub-Agent Models
advisor_agent = Agent(
    model=Gemini(model="gemini-2.0-flash", retry_options=retry_config),
    ...
)
```

**Available Models:**

- `gemini-1.5-flash` - Fast, cost-effective
- `gemini-2.5-flash` - Latest, better quality
- `gemini-pro` - Advanced reasoning

---

## Troubleshooting

### Issue: "Artifact not found"

**Cause:** Image extraction failed

**Solution:**

```python
# Check session history
print(tool_context.session.events)

# Ensure image is attached as inline_data, not file_uri
```

### Issue: "Sightengine credentials not configured"

**Cause:** Environment variables not set

**Solution:**

```bash
# Verify .env file exists
cat deepfake_detector/.env

# Check variables are exported
export api_user="your_user"
export api_secret="your_secret"

# Test API connection
python -c "import os; print(os.getenv('api_user'))"
```

### Issue: "GOOGLE_API_KEY not found"

**Cause:** Google API key missing

**Solution:**

```bash
# Set in .env
echo 'GOOGLE_API_KEY="your_key"' >> deepfake_detector/.env

# Or set as environment variable
export GOOGLE_API_KEY="your_key"
```

### Issue: Slow Response Times

**Cause:** Network latency or API rate limits

**Solution:**

```python
# Increase timeouts
response = requests.post(
    url,
    timeout=60,  # Increase from 30
    ...
)

# Or reduce retry attempts to fail faster
retry_config = types.HttpRetryOptions(attempts=2, ...)
```

### Issue: "401 Unauthorized" on Sightengine

**Cause:** Invalid credentials

**Solution:**

```bash
# Verify credentials
curl -X POST "https://api.sightengine.com/1.0/check.json" \
  -F "media=@test_image.jpg" \
  -F "api_user=YOUR_USER" \
  -F "api_secret=YOUR_SECRET" \
  -F "models=deepfake,genai"

# Check credentials in Sightengine dashboard
```

---

## Project Structure

```
deepfake_detector/
├── agent.py                      # Root agent orchestration
├── config.py                     # Configuration & retry settings
├── __init__.py                   # Package initialization
├── .env                          # Environment variables (⚠️ Keep secret)
├── .env.example                  # Template for .env
│
├── logger/
│   ├── logger.py                 # Logging configuration
│   └── __pycache__/
│
├── tools/
│   ├── save_upload_image.py      # Image extraction tool
│   ├── sightengine.py            # Deepfake detection tool
│   └── __pycache__/
│
├── subagents/
│   ├── advisor_agent.py          # Safety advice sub-agent
│   ├── nsfw_agent.py             # NSFW detection sub-agent
│   └── __pycache__/
│
└── prompts/
    ├── root_agent_prompt.py      # Root orchestration instructions
    ├── advisor_agent_prompt.py   # Advice generation logic
    ├── nsfw_agent_prompt.py      # NSFW detection criteria
    └── __pycache__/
```

---

## Security Considerations

⚠️ **Important:**

1. **Never commit `.env` file** - Contains API keys

   - Add to `.gitignore`: `deepfake_detector/.env`

2. **Validate image inputs** - Check mime types before processing

   ```python
   allowed_types = ["image/jpeg", "image/png", "image/gif", "image/webp"]
   if mime_type not in allowed_types:
       raise ValueError("Invalid image format")
   ```

3. **Rate limiting** - Implement user-level rate limits

   ```python
   # Max 10 requests per minute
   RATE_LIMIT = 10
   WINDOW = 60  # seconds
   ```

4. **Data privacy** - Don't store images beyond analysis

   - Delete temporary artifacts after processing
   - Don't log sensitive image data

5. **HTTPS only** - Ensure encrypted communication with APIs

   - Enforce TLS 1.2+
   - Verify SSL certificates

6. **Access control** - Restrict to authorized users
   - Implement authentication
   - Use API keys/tokens
   - Log all access attempts

---

## Performance Metrics

| Operation          | Time      | Notes                    |
| ------------------ | --------- | ------------------------ |
| Image extraction   | 100ms     | In-memory operation      |
| Deepfake detection | 2-5s      | Depends on image size    |
| NSFW analysis      | 1-3s      | Gemini vision processing |
| Advice generation  | 1-2s      | LLM reasoning            |
| **Total pipeline** | **5-12s** | End-to-end               |

---

## Future Enhancements

- [ ] Batch image processing
- [ ] Custom model fine-tuning
- [ ] Database persistence
- [ ] Web UI/REST API
- [ ] Multi-language support
- [ ] Integration with law enforcement platforms
- [ ] Real-time detection webhooks
- [ ] Mobile app integration
- [ ] Advanced analytics dashboard
- [ ] Export reports functionality

---

## Support & Resources

### Documentation:

- [Google ADK Docs](https://ai.google.dev/adk)
- [Gemini API Reference](https://ai.google.dev/gemini-api)
- [Sightengine API Docs](https://sightengine.com/docs)

### Community:

- Google AI Community Forum
- GitHub Issues
- Stack Overflow

---

## License

This project is licensed under the **MIT License**.  
© 2025 Aurpit bhatia.  

You are free to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the software, under the conditions of the MIT License. See [LICENSE](LICENSE) for full details.

---

## Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository  
2. Create a feature branch (`git checkout -b feature/your-feature`)  
3. Commit your changes (`git commit -m 'Add some feature'`)  
4. Push to the branch (`git push origin feature/your-feature`)  
5. Open a Pull Request

---

**Last Updated:** November 2025  
**Version:** 0.1.0  
**Maintainer:** Aurpit 21BC007

---

## FAQ

### Q: How accurate is the deepfake detection?

**A:** Sightengine reports ~95% accuracy on standard benchmarks. However, accuracy varies based on:

- Image quality and resolution
- Type of deepfake (face-swap, expression modification, etc.)
- Training data overlap with detection models

### Q: Can I use this for commercial purposes?

**A:** Check the Sightengine and Google API terms of service. Commercial licenses may be required.

### Q: What happens to the uploaded images?

**A:** By default:

1. Images are temporarily stored in memory
2. Artifacts are deleted after analysis completes
3. No data is logged or persisted

### Q: Can I integrate this into my web application?

**A:** Yes! You can:

1. Wrap the agent in a REST API using FastAPI/Flask
2. Use async tasks for long-running analysis
3. Store results in a database

### Q: How do I report false positives?

**A:**

1. Document the case with image details
2. Test with Sightengine directly
3. File an issue on GitHub
4. Contact support with test cases

---

**End of Documentation**

