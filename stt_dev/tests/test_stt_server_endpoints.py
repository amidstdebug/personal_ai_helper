import sys, pathlib, types as _types
sys.modules.setdefault("faster_whisper", _types.SimpleNamespace(WhisperModel=object))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import stt_dev.stt_server.stt_handlers as real_handlers
sys.modules.setdefault("stt_handlers", real_handlers)

import os
from fastapi.testclient import TestClient
from stt_dev.stt_server import server as stt_server
from stt_dev.stt_server import stt_handlers
import pytest

client = TestClient(stt_server.app)

def test_health_check():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_transcribe_file_not_found(monkeypatch):
    resp = client.get("/transcribe-file/", params={"file_path": "nofile.wav", "language": "en"})
    assert resp.status_code == 500


def test_transcribe_file_success(monkeypatch, tmp_path):
    dummy_file = tmp_path / "file.wav"
    dummy_file.write_text("dummy")
    monkeypatch.setattr(stt_server, "transcribe_audio", lambda fp, language="en": ["a", "b"])
    monkeypatch.setattr(stt_server, "process_transcript", lambda t: "a b")
    resp = client.get("/transcribe-file/", params={"file_path": str(dummy_file), "language": "en"})
    assert resp.status_code == 200
    assert resp.json()["segments"] == ["a", "b"]
    assert resp.json()["full_transcript"] == "a b"


@pytest.mark.parametrize("path", ["../../etc/passwd", "..\\..\\secret", "/etc/passwd"])
def test_path_traversal_rejected(monkeypatch, path):
    resp = client.get("/transcribe-file/", params={"file_path": path, "language": "en"})
    assert resp.status_code == 500


@pytest.mark.parametrize("lang", ["en", "es", "de"])
def test_transcribe_file_various_languages(monkeypatch, tmp_path, lang):
    dummy_file = tmp_path / "test.wav"
    dummy_file.write_text("dummy")
    monkeypatch.setattr(stt_server, "transcribe_audio", lambda fp, language="en": [lang])
    monkeypatch.setattr(stt_server, "process_transcript", lambda t: "".join(t))
    resp = client.get("/transcribe-file/", params={"file_path": str(dummy_file), "language": lang})
    assert resp.status_code == 200
    assert resp.json()["segments"] == [lang]
