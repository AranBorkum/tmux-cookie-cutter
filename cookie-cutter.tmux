#!/usr/bin/env bash

CURRENT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

SCRIPT_PATH="$CURRENT_DIR/scripts/cookie_cutter.sh"
REFRESH_SCRIPT_PATH="$CURRENT_DIR/scripts/re_run_cookie_cutter.sh"

tmux bind C-c run-shell "$REFRESH_SCRIPT_PATH"
tmux set-hook -g session-created "run-shell \"$SCRIPT_PATH\""
