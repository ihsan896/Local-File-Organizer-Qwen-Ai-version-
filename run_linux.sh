#!/usr/bin/env bash
# ==============================================================================
# Desktop Organizer - Linux Launcher (Ihsan-AI)
# https://github.com/ihsan896/Local-File-Organizer
# ==============================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$SCRIPT_DIR"

echo "=================================================="
echo " Desktop Organizer & Local File Organizer"
echo " Developer: Ihsan-AI (https://github.com/ihsan896)"
echo "=================================================="

# Check for required system packages
NEED_INSTALL=0
if ! command -v python3 &> /dev/null; then
    NEED_INSTALL=1
fi
if ! python3 -c "import tkinter" &> /dev/null 2>&1; then
    NEED_INSTALL=1
fi

if [ "$NEED_INSTALL" -eq 1 ]; then
    echo "[INFO] Missing system dependencies detected. Requesting sudo to install required packages:"
    echo "       python3, python3-tk, python3-venv, python3-pip"
    sudo apt-get update && sudo apt-get install -y python3 python3-tk python3-venv python3-pip
fi

# Hardware / AI Environment Diagnostics & Auto-Start
echo "[INFO] Checking AI environment & Ollama service..."
if command -v ollama &> /dev/null; then
    if ! curl -s http://127.0.0.1:11434/api/tags &> /dev/null; then
        echo "[INFO] Ollama service is not running. Starting ollama serve in background..."
        ollama serve > /dev/null 2>&1 &
        sleep 2
    fi
    if ! ollama list 2>/dev/null | grep -q "qwen3.5:2b"; then
        echo "[INFO] Pulling qwen3.5:2b model for local AI..."
        ollama pull qwen3.5:2b || true
    fi
    echo "[INFO] AI readiness check passed."
else
    echo "[INFO] Ollama not found. Fast Mode will be used. To enable AI, visit https://ollama.com"
fi

# Prepare Virtual Environment
VENV_DIR="$PROJECT_ROOT/.venv_linux"
if [ ! -d "$VENV_DIR" ]; then
    echo "[INFO] Preparing virtual environment: $VENV_DIR"
    python3 -m venv --system-site-packages "$VENV_DIR"
    "$VENV_DIR/bin/pip" install --upgrade pip --quiet
    if [ -f "$PROJECT_ROOT/requirements.txt" ]; then
        echo "[INFO] Checking Python dependencies..."
        "$VENV_DIR/bin/pip" install -r "$PROJECT_ROOT/requirements.txt" --quiet
    fi
fi

export PYTHONIOENCODING="utf-8"
cd "$PROJECT_ROOT"

# Launch GUI in regular user context to preserve Desktop path
echo "[INFO] Starting Desktop Organizer UI..."
if [ -n "$SUDO_USER" ] && [ "$SUDO_USER" != "root" ]; then
    exec sudo -u "$SUDO_USER" -E "$VENV_DIR/bin/python3" "$PROJECT_ROOT/gui.py" "$@"
else
    exec "$VENV_DIR/bin/python3" "$PROJECT_ROOT/gui.py" "$@"
fi
