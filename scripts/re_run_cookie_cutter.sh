#!/usr/bin/env bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck disable=SC1091
source "$SCRIPT_DIR/lib.sh"

main() {
	local config_file
	config_file=$(get_config_file)
	[[ -z "$config_file" ]] && exit 0

	local window_base_index pane_base_index session_name current_window_index
	window_base_index=$(get_window_base_index)
	pane_base_index=$(get_pane_base_index)
	session_name=$(get_session_name)
	current_window_index=$(get_current_window_index)

	local config_index=$((current_window_index - window_base_index))
	local window_count
	window_count=$(yq '.default_windows | length' "$config_file")

	if [[ $config_index -ge 0 && $config_index -lt $window_count ]]; then
		create_aliases_file "$config_file"
		run_window_config "$config_file" "$session_name" "$window_base_index" "$pane_base_index" "$config_index" "rename"
		rm -f "$ALIASES_FILE"
	fi
}

main
