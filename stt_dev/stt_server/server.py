# stt_server/server.py
from fastapi import FastAPI, HTTPException, Query
from stt_utils import transcribe_audio, process_transcript
import os

from logger import get_logger
logger = get_logger("stt_server")

app = FastAPI()

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/transcribe-file/")
def transcribe_file(file_path: str = Query(..., description="Absolute or relative path to audio file"),
                    language: str = Query("en", description="Language code for transcription")):
    try:
        if not os.path.exists(file_path):
            logger.error(f"Requested file not found: {file_path}")
            raise HTTPException(status_code=404, detail="Audio file not found")

        logger.info(f"Received request to transcribe: {file_path}")
        transcript = transcribe_audio(file_path, language)
        processed = process_transcript(transcript)
        return {
            "segments": transcript,
            "full_transcript": processed
        }

    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Audio file not found")

    except Exception as e:
        logger.exception("Transcription error")
        raise HTTPException(status_code=500, detail="Internal transcription error")