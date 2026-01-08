#!/usr/bin/env bash

CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

SCRIPT_PATH="$CURRENT_DIR/scripts/cookie_cutter.py"
REFRESH_WINDOW_SCRIPT_PATH="$CURRENT_DIR/scripts/re_run_cookie_cutter.py"

tmux set-option -go @cookie_cutter_python "python3"
tmux bind C-c run-shell "$(tmux show-options -g -v @cookie_cutter_python) $REFRESH_WINDOW_SCRIPT_PATH"

tmux set-hook -g session-created "run-shell \"\$(tmux show-options -g -v @cookie_cutter_python) \\\"$SCRIPT_PATH\\\"\""
