#!/bin/sh
MODULE=$1
PORT=$2
if [ "$HOT_RELOAD" = "1" ]; then
    exec uvicorn "$MODULE":app --host 0.0.0.0 --port "$PORT" --reload --reload-dir /app/stt_dev
else
    exec uvicorn "$MODULE":app --host 0.0.0.0 --port "$PORT"
fi
