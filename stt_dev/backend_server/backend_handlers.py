# backend/backend_handlers.py

from fastapi import UploadFile, File, HTTPException
from ..stt_server.stt_handlers import transcribe_audio
from ..utils.config import UPLOAD_DIR
from ..utils.logger import get_logger
from ..utils.file_utils import save_upload_file, delete_file
import os

logger = get_logger("backend_server")

async def transcribe(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    try:
        save_upload_file(file, file_path)
        transcript = transcribe_audio(file_path)
        return {"transcript": transcript}

    except Exception as e:
        logger.exception("Transcription failed")
        raise HTTPException(status_code=500, detail=f"Transcription error: {e}")

    finally:
        delete_file(file_path)