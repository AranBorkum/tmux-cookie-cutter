#!/usr/bin/env bash

set-option -go @cookie_cutter_python "python3"

tmux set-hook -g session-created 'run-shell "$(tmux show-options -g -v @cookie_cutter_python) $TMUX_PLUGIN_MANAGER_PATH/tmux-cookie-cutter/scripts/cookie_cutter.py'
