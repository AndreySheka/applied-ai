#!/usr/bin/env bash
# Запуск демонстрации из самостоятельного репозитория курса.
set -euo pipefail
repo_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
conda_executable="${CONDA_EXE:-$(command -v conda || true)}"
if [[ -z "$conda_executable" ]]; then
    printf '%s\n' 'Conda не найдена. Инструкции для других сред: docs/SETUP.md.' >&2
    exit 1
fi
export DETECTION_LAB_ROOT="${DETECTION_LAB_ROOT:-$repo_dir/.cache/detection}"
export JUPYTER_PREFER_ENV_PATH=1
cd -- "$repo_dir"
exec "$conda_executable" run --no-capture-output --name applied-ai \
    python -m jupyterlab --ServerApp.ip=127.0.0.1 --ServerApp.root_dir="$repo_dir" \
    labs/01_detection/01_interactive_demo.ipynb "$@"
