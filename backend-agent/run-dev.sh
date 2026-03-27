#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV_PATH="$SCRIPT_DIR/.venv"

if [ -f "$VENV_PATH/bin/activate" ]; then
  source "$VENV_PATH/bin/activate"
fi

HOST="${PET_BACKEND_HOST:-127.0.0.1}"
PORT="${PET_BACKEND_PORT:-18787}"

cd "$SCRIPT_DIR"
python -m uvicorn app.main:app --host "$HOST" --port "$PORT" --reload
