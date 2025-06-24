# Telegram-Interfacing Module

This module contains the different servers for enabling the Telegram bot and its respective STT functionality.

The key components are:

- **telegram_server** – Run the Telegram bot.
- **backend_server** – Backend server to call different services
- **stt_server** – Server to specifically handle all STT-related functionality
- **utils** – Helper modules for configuration, logging and file management

Each server directory contains its own `Dockerfile` **and** `requirements.txt`.
The Docker Compose configuration starts one container per server using
these files.

## Running the Servers

Use the helper script `deploy.sh` in the repository root.

```bash
./deploy.sh dev   # hot reload enabled
./deploy.sh prod  # production mode
```

The script downloads the faster-whisper `distil-large-v3` model to
`stt_dev/stt_server/whisper_model/` if it is missing, warms it up with a
short transcription and then starts the Docker Compose stack. The model
folder is mounted into the containers so it persists across runs.

## Testing

The `tests` directory contains an extensive test-suite that uses `pytest`.
Install the development dependencies from the repository root
`requirements.txt` and run:

```bash
pytest
```
