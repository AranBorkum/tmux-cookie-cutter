#!/usr/bin/env bash

$(tmux show-options -gv @cookie_cutter_python) -c "import yaml"

if [ ! $? -eq 0 ]; then
	tmux command-prompt -I "tmux-cookie-cutter requires PyYAML to be installed [Esc]"
else
	tmux run-shell "$(tmux show-options -g -v @cookie_cutter_python) $TMUX_PLUGIN_MANAGER_PATH/tmux-cookie-cutter/scripts/cookie_cutter.py"
fi
