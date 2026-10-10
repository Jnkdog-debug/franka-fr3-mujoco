#!/usr/bin/env bash
set -e
TASK_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
if [[ -n "${PYTHON:-}" ]]; then
  TASK_PYTHON="$PYTHON"
elif [[ -n "${CONDA_PREFIX:-}" ]]; then
  TASK_PYTHON="$CONDA_PREFIX/bin/python"
elif [[ -x /home/xyz/miniconda3/envs/mujoco/bin/python ]]; then
  TASK_PYTHON=/home/xyz/miniconda3/envs/mujoco/bin/python
else
  TASK_PYTHON=python3
fi
exec "$TASK_PYTHON" "$TASK_DIR/view_fr3.py"
