# telegram_server/telegram_utils.py

import os
import uuid
import requests
from config import FASTAPI_URL, UPLOAD_DIR
from telegram import Update
from telegram.ext import ContextTypes
from logger import get_logger
logger = get_logger("telegram_server")

os.makedirs(UPLOAD_DIR, exist_ok=True)

async def download_voice_file(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    voice = update.message.voice
    if not voice:
        raise ValueError("No voice message found in update.")

    file = await context.bot.get_file(voice.file_id)
    file_ext = ".ogg"
    filename = f"{uuid.uuid4().hex}{file_ext}"
    file_path = os.path.join(UPLOAD_DIR, filename)

    logger.info(f"Downloading voice file to: {file_path}")
    await file.download_to_drive(file_path)
    return file_path

def send_audio_to_api(file_path: str) -> list[str]:
    logger.info(f"Sending audio file to backend_server API: {file_path}")
    with open(file_path, "rb") as f:
        response = requests.post(FASTAPI_URL, files={"file": (os.path.basename(file_path), f)})
    response.raise_for_status()
    data = response.json()
    transcript = data.get("transcript", [])
    if not transcript:
        logger.warning(f"No transcript returned for file: {file_path}")
    return transcript

async def handle_audio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file_path = None
    try:
        file_path = await download_voice_file(update, context)
        transcript = send_audio_to_api(file_path)

        if transcript:
            await update.message.reply_text(" ".join(transcript))
        else:
            await update.message.reply_text("Transcription returned no content.")

    except requests.exceptions.RequestException:
        logger.exception("HTTP error communicating with backend_server API")
        await update.message.reply_text("Transcription failed: backend_server API error.")

    except Exception:
        logger.exception("Unhandled error processing voice message")
        await update.message.reply_text("An error occurred while processing the audio.")

    finally:
        if file_path and os.path.exists(file_path):
            try:
                os.remove(file_path)
                logger.info(f"Deleted temp file: {file_path}")
            except Exception as cleanup_err:
                logger.warning(f"Failed to delete temp file {file_path}: {cleanup_err}")