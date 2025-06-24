# Telegram-Interfacing Module

This module contains the different servers for enabling the Telegram bot and its respective STT functionality.

The key components are:

- **telegram_server** – Run the Telegram bot.
- **backend_server** – Backend server to call different services
- **stt_server** – Server to specifically handle all STT-related functionality
- **utils** – Helper modules for configuration, logging and file management

## Running the Servers



## Testing

The `tests` directory contains an extensive test-suite that uses `pytest`.
Install the dependencies from `requirements.txt` and run:

```
pytest
```