import sys, pathlib, types as _types
sys.modules.setdefault("faster_whisper", _types.SimpleNamespace(WhisperModel=object))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import stt_dev.stt_server.stt_handlers as real_handlers
sys.modules.setdefault("stt_handlers", real_handlers)

import types
import pytest
from stt_dev.stt_server import stt_handlers

class DummyModel:
    def __init__(self, result):
        self.result = result
    def transcribe(self, file_path, beam_size=5, language="en", condition_on_previous_text=False):
        return ([types.SimpleNamespace(text=t) for t in self.result], None)


def setup_module(module):
    stt_handlers.get_model.cache_clear()


def test_transcribe_file_not_found(tmp_path):
    missing = tmp_path / "nofile.wav"
    with pytest.raises(FileNotFoundError):
        stt_handlers.transcribe_audio(str(missing))


def test_transcribe_audio_success(monkeypatch, tmp_path):
    dummy_file = tmp_path / "audio.wav"
    dummy_file.write_bytes(b"x")
    monkeypatch.setattr(stt_handlers, "get_model", lambda: DummyModel(["hello", "world"]))
    result = stt_handlers.transcribe_audio(str(dummy_file))
    assert result == ["hello", "world"]


def test_process_transcript():
    text = stt_handlers.process_transcript(["a", "b", "c"])
    assert text == "a b c"
