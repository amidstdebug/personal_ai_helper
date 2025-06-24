# STT Development Package

This package contains a small collection of speech-to-text utilities and example
FastAPI servers used for testing. The key components are:

- **stt_server** – exposes endpoints for transcribing existing audio files.
- **backend_server** – accepts uploaded audio and returns a transcript.
- **telegram_server** – example integration with a Telegram bot.
- **utils** – helper modules for configuration, logging and file management.

## Running the Servers

Each server can be started with `uvicorn` or run directly when modules provide a
`main` entry point. They rely on environment variables defined in `.env`.

```
uvicorn stt_dev.stt_server.server:app --reload
uvicorn stt_dev.backend_server.server:app --reload
```

## Testing

The `tests` directory contains an extensive test-suite that uses `pytest`.
Install the dependencies from `requirements.txt` and run:

```
pytest
```
