import sys, pathlib, types as _types
sys.modules.setdefault("faster_whisper", _types.SimpleNamespace(WhisperModel=object))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import stt_dev.stt_server.stt_handlers as real_handlers
sys.modules.setdefault("stt_handlers", real_handlers)

import io
import pytest
from fastapi import UploadFile, HTTPException
from stt_dev.backend_server import backend_handlers

class DummyUploadFile(UploadFile):
    def __init__(self, filename, content):
        super().__init__(filename=filename, file=io.BytesIO(content))

@pytest.mark.asyncio
async def test_transcribe_success(monkeypatch):
    upload = DummyUploadFile("x.wav", b"data")
    monkeypatch.setattr(backend_handlers, "transcribe_audio", lambda p: ["ok"])
    res = await backend_handlers.transcribe(upload)
    assert res == {"transcript": ["ok"]}

@pytest.mark.asyncio
async def test_transcribe_failure(monkeypatch):
    upload = DummyUploadFile("x.wav", b"data")
    def raise_error(p):
        raise RuntimeError("fail")
    monkeypatch.setattr(backend_handlers, "transcribe_audio", raise_error)
    with pytest.raises(HTTPException):
        await backend_handlers.transcribe(upload)
