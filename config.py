import os
from dotenv import load_dotenv

load_dotenv()

# LLM Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Image Generator Configuration
REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")
COMFYUI_API_URL = os.getenv("COMFYUI_API_URL", "http://127.0.0.1:8188")

# Instagram Credentials
IG_USERNAME = os.getenv("IG_USERNAME")
IG_PASSWORD = os.getenv("IG_PASSWORD")

# Character Base Setup
CHARACTER_NAME = os.getenv("CHARACTER_NAME", "AI Influencer")
CHARACTER_STYLE = os.getenv("CHARACTER_STYLE", "A beautiful woman, highly detailed face")
FACE_ID_REFERENCE_IMAGE_URL = os.getenv("FACE_ID_REFERENCE_IMAGE_URL", "")

# App Settings
SESSION_FILE = "ig_session.json"
POSTS_PER_DAY = 2
