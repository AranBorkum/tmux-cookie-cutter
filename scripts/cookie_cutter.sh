#!/usr/bin/env bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck disable=SC1091
source "$SCRIPT_DIR/lib.sh"

main() {
	local config_file
	config_file=$(get_config_file)
	[[ -z "$config_file" ]] && exit 0

	local window_base_index pane_base_index session_name
	window_base_index=$(get_window_base_index)
	pane_base_index=$(get_pane_base_index)
	session_name=$(get_session_name)

	create_aliases_file "$config_file"

	local window_count
	window_count=$(yq '.default_windows | length' "$config_file")

	for i in $(seq 0 $((window_count - 1))); do
		local rename_or_create="create"
		[[ $i -eq 0 ]] && rename_or_create="rename"
		run_window_config "$config_file" "$session_name" "$window_base_index" "$pane_base_index" "$i" "$rename_or_create"
	done

	tmux select-window -t "${session_name}:$((window_base_index + 1))" 2>/dev/null || true
	tmux select-window -t "${session_name}:${window_base_index}"

	rm -f "$ALIASES_FILE"
}

main
