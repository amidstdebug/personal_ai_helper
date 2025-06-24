# config.py
from dotenv import load_dotenv
import os

load_dotenv('./env.dev')

WHISPER_DEVICE = os.getenv("WHISPER_DEVICE", "cuda")
WHISPER_COMPUTE = os.getenv("WHISPER_COMPUTE", "float16")
MODEL_SIZE = os.getenv("WHISPER_MODEL", "distil-large-v3")
UPLOAD_DIR = os.getenv("UPLOAD_DIR", "./audio")
FASTAPI_URL = os.getenv("FASTAPI_URL", "http://localhost:8000/transcribe/")
BOT_TOKEN = os.getenv("BOT_TOKEN")