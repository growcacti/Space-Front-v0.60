#!/usr/bin/env bash
set -e
GAME_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
if [[ -x "$GAME_DIR/.venv/bin/python" ]]; then
    exec "$GAME_DIR/.venv/bin/python" "$GAME_DIR/main.py" "$@"
else
    exec python3 "$GAME_DIR/main.py" "$@"
fi
