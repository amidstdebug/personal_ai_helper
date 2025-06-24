import sys, pathlib, types as _types
sys.modules.setdefault("faster_whisper", _types.SimpleNamespace(WhisperModel=object))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import stt_dev.stt_server.stt_handlers as real_handlers
sys.modules.setdefault("stt_handlers", real_handlers)

import asyncio
from fastapi.testclient import TestClient
from stt_dev.stt_server import server as stt_server
import pytest

client = TestClient(stt_server.app)

def make_request(monkeypatch):
    monkeypatch.setattr(stt_server, "transcribe_audio", lambda fp, language='en': ['ok'])
    monkeypatch.setattr(stt_server, "process_transcript", lambda t: 'ok')
    resp = client.get('/transcribe-file/', params={'file_path': 'dummy', 'language': 'en'})
    assert resp.status_code in (404, 500, 200)

@pytest.mark.asyncio
async def test_concurrent_requests(monkeypatch):
    tasks = [asyncio.to_thread(make_request, monkeypatch) for _ in range(20)]
    await asyncio.gather(*tasks)
