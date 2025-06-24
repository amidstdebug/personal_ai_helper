# Test Suite Overview

This folder contains unit tests for the speech-to-text development module. The tests cover all server components and utility functions.

- **test_stt_handlers.py** – verifies the audio transcription helpers.
- **test_stt_server_endpoints.py** – exercises the FastAPI endpoints in `stt_server`.
- **test_backend_handlers.py** – checks file upload handling and transcription from the backend server.
- **test_backend_server_endpoints.py** – tests the backend server HTTP API.
- **test_telegram_handlers.py** – validates Telegram bot handlers and interaction with the backend API.
- **test_utils.py** – tests helper functions for saving and deleting files.
- **test_load.py** – runs simple concurrency tests against the STT server.

Run all tests with:

```bash
pytest
```
