#!/usr/bin/env bash

tmux set-option -go @cookie_cutter_python "python3"

tmux set-hook -g session-created 'run-shell "$(tmux show-options -g -v @cookie_cutter_python) $HOME/.config/tmux/plugins/tmux-cookie-cutter/scripts/cookie_cutter.py'
tmux bind C-p display-popup -E 'run-shell "$(tmux show-options -g -v @cookie_cutter_python) $HOME/.config/tmux/plugins/tmux-cookie-cutter/scripts/mini_window.py'


