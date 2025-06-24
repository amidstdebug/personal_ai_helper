import sys, pathlib
import types as _types
sys.modules.setdefault("faster_whisper", _types.SimpleNamespace(WhisperModel=object))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "stt_dev"))
import os
import types
import pytest
import builtins
from stt_dev.telegram_server import telegram_handlers as th

class DummyFile:
    def __init__(self, path):
        self.path = path
    async def download_to_drive(self, dest):
        with open(dest, 'wb') as f:
            f.write(b'data')

class DummyContext:
    def __init__(self, file):
        async def _get_file(fid):
            return file
        self.bot = types.SimpleNamespace(get_file=_get_file)

class DummyUpdate:
    def __init__(self, voice=None):
        self.message = types.SimpleNamespace(voice=voice, reply_text=lambda msg: None)

class DummyResponse:
    def __init__(self, json_data, status=200):
        self._json = json_data
        self.status_code = status
    def raise_for_status(self):
        if self.status_code >= 400:
            raise Exception('http error')
    def json(self):
        return self._json

@pytest.mark.asyncio
async def test_download_voice_file(tmp_path):
    voice_file = DummyFile('remote')
    voice = types.SimpleNamespace(file_id='1')
    update = DummyUpdate(voice)
    context = DummyContext(voice_file)
    result = await th.download_voice_file(update, context)
    assert os.path.exists(result)

@pytest.mark.asyncio
async def test_download_voice_file_no_voice(tmp_path):
    update = DummyUpdate(None)
    context = DummyContext(None)
    with pytest.raises(ValueError):
        await th.download_voice_file(update, context)

def test_send_audio_to_api(monkeypatch, tmp_path):
    path = tmp_path / 'a.wav'
    path.write_bytes(b'1')
    def mock_post(url, files):
        return DummyResponse({'transcript': ['ok']})
    monkeypatch.setattr(th.requests, 'post', mock_post)
    transcript = th.send_audio_to_api(str(path))
    assert transcript == ['ok']


def test_send_audio_api_failure(monkeypatch, tmp_path):
    path = tmp_path / 'a.wav'
    path.write_bytes(b'1')
    def mock_post(url, files):
        return DummyResponse({}, status=500)
    monkeypatch.setattr(th.requests, 'post', mock_post)
    with pytest.raises(Exception):
        th.send_audio_to_api(str(path))
