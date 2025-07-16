#!/usr/bin/env bash

tmux set-option -go @cookie_cutter_python "python3"

$(tmux show-options -gv @cookie_cutter_python) -c "import yaml"

if [ ! $? -eq 0 ]; then
	tmux command-prompt -I "tmux-cookie-cutter requires PyYAML to be installed [Esc]"
fi

# tmux set-hook -g session-created 'run-shell "$(tmux show-options -g -v @cookie_cutter_python) $TMUX_PLUGIN_MANAGER_PATH/tmux-cookie-cutter/scripts/cookie_cutter.py'

tmux set-hook -g session-created 'run-shell ".$TMUX_PLUGIN_MANAGER_PATH/tmux-cookie-cutter/scripts/cookie-cutter.sh'
