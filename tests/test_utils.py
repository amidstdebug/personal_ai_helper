import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "stt_dev"))
import os
import io
import pytest

from stt_dev.utils import file_utils


def test_save_and_delete_file(tmp_path):
    target_path = tmp_path / "example.bin"
    # simulate UploadFile with minimal interface
    class DummyUpload:
        def __init__(self, content):
            self.file = io.BytesIO(content)
    dummy = DummyUpload(b"data")

    file_utils.save_upload_file(dummy, str(target_path))
    assert target_path.exists()

    file_utils.delete_file(str(target_path))
    assert not target_path.exists()


def test_delete_missing_file(tmp_path):
    missing = tmp_path / "missing.txt"
    # should not raise
    file_utils.delete_file(str(missing))
    assert not missing.exists()
