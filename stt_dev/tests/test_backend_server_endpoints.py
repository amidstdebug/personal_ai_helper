import sys, pathlib, types as _types
sys.modules.setdefault("faster_whisper", _types.SimpleNamespace(WhisperModel=object))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import stt_dev.stt_server.stt_handlers as real_handlers
sys.modules.setdefault("stt_handlers", real_handlers)

from fastapi.testclient import TestClient
from stt_dev.backend_server import server as backend_server
import pytest

client = TestClient(backend_server.app, raise_server_exceptions=False)


def test_backend_health():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


async def _dummy_transcribe(file):
    return {"transcript": ["ok"]}


async def _fail_transcribe(file):
    raise RuntimeError("boom")


@pytest.mark.asyncio
async def test_transcribe_endpoint_success(monkeypatch, tmp_path):
    monkeypatch.setattr(backend_server, "transcribe", _dummy_transcribe)
    path = tmp_path / "file.wav"
    path.write_text("dummy")
    with open(path, "rb") as f:
        resp = client.post("/transcribe/", files={"file": ("file.wav", f, "audio/wav")})
    assert resp.status_code == 200
    assert resp.json() == {"transcript": ["ok"]}


@pytest.mark.asyncio
async def test_transcribe_endpoint_failure(monkeypatch, tmp_path):
    monkeypatch.setattr(backend_server, "transcribe", _fail_transcribe)
    path = tmp_path / "file.wav"
    path.write_text("dummy")
    with open(path, "rb") as f:
        resp = client.post("/transcribe/", files={"file": ("file.wav", f, "audio/wav")})
    assert resp.status_code == 500
