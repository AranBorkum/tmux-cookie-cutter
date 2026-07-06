#!/usr/bin/env bash

ALIASES_FILE="/tmp/.tmux-cookie-cutter-aliases"

get_config_file() {
	local local_config=".tmux-cookie-cutter.yaml"
	local global_config="$HOME/.config/.tmux-cookie-cutter.yaml"
	if [[ -f "$local_config" ]]; then
		echo "$local_config"
	elif [[ -f "$global_config" ]]; then
		echo "$global_config"
	fi
}

get_window_base_index() {
	tmux show-option -gv base-index
}

get_pane_base_index() {
	tmux show-option -gv pane-base-index
}

get_session_name() {
	tmux display-message -p "#S"
}

get_current_window_index() {
	tmux display-message -p "#I"
}

# Set tmux session envvars from a yq path pointing to a string->string map.
set_envvars() {
	local config_file="$1"
	local yq_path="$2"
	local session="$3"

	local entry
	while IFS= read -r entry; do
		[[ -z "$entry" ]] && continue
		local key="${entry%%=*}"
		local value="${entry#*=}"
		tmux set-environment -t "$session" "$key" "$value"
	done < <(yq "${yq_path} // {} | to_entries[] | .key + \"=\" + .value" "$config_file" 2>/dev/null)
}

send_command() {
	local target="$1"
	local command="$2"
	[[ -z "$command" || "$command" == "null" ]] && return
	tmux send-keys -t "$target" "$command" C-m
}

create_aliases_file() {
	local config_file="$1"
	rm -f "$ALIASES_FILE"

	local entry
	while IFS= read -r entry; do
		[[ -z "$entry" ]] && continue
		local alias_name="${entry%%=*}"
		local alias_value="${entry#*=}"
		echo "alias ${alias_name}=\"${alias_value}\"" >>"$ALIASES_FILE"
	done < <(yq '.shared.aliases // {} | to_entries[] | .key + "=" + .value' "$config_file" 2>/dev/null)
}

source_aliases() {
	local target="$1"
	[[ -f "$ALIASES_FILE" ]] && send_command "$target" "source $ALIASES_FILE"
}

run_window_config() {
	local config_file="$1"
	local session="$2"
	local window_base_index="$3"
	local pane_base_index="$4"
	local index="$5"
	local rename_or_create="$6" # "rename" or "create"

	local window_index=$((window_base_index + index))
	local target="${session}:${window_index}"

	local win_name
	win_name=$(yq ".default_windows[${index}].name" "$config_file")

	if [[ "$rename_or_create" == "rename" ]]; then
		tmux rename-window -t "$target" "$win_name"
	else
		tmux new-window -n "$win_name" -t "$session"
	fi

	local shared_setup win_setup win_command
	shared_setup=$(yq '.shared.setup_command // ""' "$config_file")
	win_setup=$(yq ".default_windows[${index}].setup_command // \"\"" "$config_file")
	win_command=$(yq ".default_windows[${index}].command // \"\"" "$config_file")

	set_envvars "$config_file" ".shared.envvars" "$session"
	send_command "$target" "$shared_setup"
	set_envvars "$config_file" ".default_windows[${index}].envvars" "$session"
	send_command "$target" "$win_setup"
	source_aliases "$target"
	send_command "$target" "$win_command"

	local pane_count
	pane_count=$(yq ".default_windows[${index}].panes | length" "$config_file" 2>/dev/null)
	[[ -z "$pane_count" || "$pane_count" == "null" || "$pane_count" -eq 0 ]] && return

	for j in $(seq 0 $((pane_count - 1))); do
		local pane_index=$((pane_base_index + j + 1))
		local split_dir pane_command pane_size
		split_dir=$(yq ".default_windows[${index}].panes[${j}].split_direction" "$config_file")
		pane_command=$(yq ".default_windows[${index}].panes[${j}].command // \"\"" "$config_file")
		pane_size=$(yq ".default_windows[${index}].panes[${j}].size // \"\"" "$config_file")

		if [[ "$split_dir" == "horizontal" ]]; then
			tmux split-window -v -t "$target"
		else
			tmux split-window -h -t "$target"
		fi

		# Pane envvars and setup_command come from the parent window (matching Python behaviour).
		set_envvars "$config_file" ".shared.envvars" "$session"
		send_command "$target" "$shared_setup"
		set_envvars "$config_file" ".default_windows[${index}].envvars" "$session"
		send_command "$target" "$win_setup"
		send_command "$target" "$pane_command"

		if [[ -n "$pane_size" && "$pane_size" != "null" ]]; then
			if [[ "$split_dir" == "vertical" ]]; then
				local window_width
				window_width=$(tmux display -t "$target" -p "#{window_width}")
				local target_width=$((window_width * pane_size / 100))
				tmux resize-pane -t "${session}:${window_index}.${pane_index}" -x "$target_width"
			else
				local window_height
				window_height=$(tmux display -t "$target" -p "#{window_height}")
				local target_height=$((window_height * pane_size / 100))
				tmux resize-pane -t "${session}:${window_index}.${pane_index}" -y "$target_height"
			fi
		fi
	done
}
