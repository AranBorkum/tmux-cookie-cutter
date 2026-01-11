#!/usr/bin/env bash

set -euo pipefail

CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

RUN_SHARED_SCRIPT_PATH="$CURRENT_DIR/run_shared.py"

run_shared_config() {
	if [[ ${CREATED_BY+x} ]]; then
		exit 0
	else
		$(tmux show-options -g -v @cookie_cutter_python) $RUN_SHARED_SCRIPT_PATH
	fi
}

run_shared_config
