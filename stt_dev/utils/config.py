# utils/config.py
from dotenv import load_dotenv
from pathlib import Path
import os

# Load environment variables from a .env file located at the project root
env_path = Path(__file__).resolve().parents[1] / '.env'
if env_path.exists():
    load_dotenv(env_path)

WHISPER_DEVICE = os.getenv("WHISPER_DEVICE", "cuda")
WHISPER_COMPUTE = os.getenv("WHISPER_COMPUTE", "float16")
MODEL_SIZE = os.getenv("WHISPER_MODEL", "distil-large-v3")
UPLOAD_DIR = os.getenv("UPLOAD_DIR", "../audio")
FASTAPI_URL = os.getenv("FASTAPI_URL", "http://localhost:8000/transcribe/")
BOT_TOKEN = os.getenv("BOT_TOKEN")