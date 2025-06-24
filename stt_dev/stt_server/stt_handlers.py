# stt_handlers.py
import os
import time
from functools import lru_cache
from faster_whisper import WhisperModel
from ..utils.config import WHISPER_DEVICE, WHISPER_COMPUTE, MODEL_SIZE
from ..utils.logger import get_logger
logger = get_logger("stt_server")

@lru_cache(maxsize=1)
def get_model() -> WhisperModel:
    logger.info(
        f"Initializing WhisperModel: size={MODEL_SIZE}, device={WHISPER_DEVICE}, compute_type={WHISPER_COMPUTE}"
    )
    return WhisperModel(
        MODEL_SIZE,
        device=WHISPER_DEVICE,
        compute_type=WHISPER_COMPUTE
    )

def transcribe_audio(file_path: str, language: str = "en") -> list[str]:
    if not os.path.exists(file_path):
        logger.error(f"File not found: {file_path}")
        raise FileNotFoundError(f"Input file not found: {file_path}")

    logger.info(f"Starting transcription: file={file_path}, language={language}")
    start_time = time.time()

    model = get_model()
    segments, _ = model.transcribe(
        file_path,
        beam_size=5,
        language=language,
        condition_on_previous_text=False
    )

    transcript = [segment.text for segment in segments]
    duration = time.time() - start_time

    logger.info(f"Transcription complete: segments={len(transcript)}, duration={duration:.2f}s")
    return transcript

def process_transcript(transcript: list[str]) -> str:
    text = " ".join(transcript).strip()
    logger.debug(f"Processed transcript: {len(text)} characters")
    return text