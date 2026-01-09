import importlib

constants = importlib.import_module("constants")
tmux_commands = importlib.import_module("tmux_commands")
utils = importlib.import_module("utils")


def main() -> None:
    config_file_path = utils.get_config_file_path()
    window_base_index = tmux_commands.get_window_base_index()
    session_name = tmux_commands.get_tmux_session_name()

    if not config_file_path:
        return

    parsed_configuration = utils.parse_config_file(config_file_path=config_file_path)

    if parsed_configuration is None:
        return

    default_window_name = parsed_configuration.get(constants.DEFAULT_WINDOW_NAME, None)
    shared = utils.parse_shared_values(parsed_configuration=parsed_configuration)
    window_index = tmux_commands.get_current_tmux_window_index()

    utils.run_shared_window_configuration(
        shared_configuration=shared,
        session_name=session_name,
        window_base_index=window_base_index,
        index=window_index - window_base_index,
        window_name=default_window_name,
    )


main()
