#!/usr/bin/env bash

tmux set-hook -g session-created 'run-shell "python3 $TMUX_PLUGIN_MANAGER_PATH/tmux-cookie-cutter/scripts/cookie_cutter.py'
