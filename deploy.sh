#!/bin/bash
set -e
MODE=${1:-dev}
if [ "$MODE" != "dev" ] && [ "$MODE" != "prod" ]; then
  echo "Usage: $0 [dev|prod]" >&2
  exit 1
fi
MODEL_DIR="$(pwd)/stt_dev/stt_server/whisper_model"
python - <<'PY'
import importlib, subprocess, sys
spec = importlib.util.find_spec("faster_whisper")
if spec is None:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "faster-whisper"])
PY
if [ ! -d "$MODEL_DIR" ]; then
  echo "Whisper model not found. Downloading to $MODEL_DIR" >&2
  mkdir -p "$MODEL_DIR"
  python - <<PY
from faster_whisper.utils import download_model
download_model("distil-large-v3", output_dir="$MODEL_DIR")
PY
fi
python - <<'PY'
from faster_whisper import WhisperModel
import wave, struct, os
model = WhisperModel("distil-large-v3")
path="stt_dev/stt_server/warm.wav"
with wave.open(path, "w") as f:
    f.setnchannels(1); f.setsampwidth(2); f.setframerate(16000)
    f.writeframes(struct.pack("<h",0)*16000)
model.transcribe(path, beam_size=1, language="en")
os.remove(path)
PY
if [ "$MODE" = "dev" ]; then
  export HOT_RELOAD=1
else
  export HOT_RELOAD=0
fi
docker compose -f stt_dev/docker-compose.yml up --build -d
sleep 5
curl -fs http://localhost:8000/health >/dev/null && echo "Backend healthy" || echo "Backend failed"
curl -fs http://localhost:8001/health >/dev/null && echo "STT healthy" || echo "STT failed"
docker compose ps
