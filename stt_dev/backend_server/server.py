# backend_server/server.py

from fastapi import FastAPI, UploadFile, File
from .backend_handlers import transcribe
from ..utils.logger import get_logger

logger = get_logger("backend_server")

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    logger.info("Backend server starting up")

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/transcribe/")
async def transcribe_endpoint(file: UploadFile = File(...)):
    return await transcribe(file)