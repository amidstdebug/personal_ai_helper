# fast_api_server/server.py

from fastapi import FastAPI, UploadFile, File, HTTPException
import shutil
import os
from stt_server.stt_utils import transcribe_audio
from utils.config import UPLOAD_DIR
from utils.logger import get_logger
logger = get_logger("backend_server")

app = FastAPI()

os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/transcribe/")
async def transcribe(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    try:
        # store file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # perform transcription
        transcript = transcribe_audio(file_path)

        return {"transcript": transcript}

    except Exception as e:
        logger.exception("Transcription failed")
        raise HTTPException(status_code=500, detail=f"Transcription error: {e}")

    finally:
        # always attempt to clean up the file
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception as cleanup_err:
            logger.warning(f"Failed to delete temp file {file_path}: {cleanup_err}")