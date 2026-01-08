import importlib

constants = importlib.import_module("constants")
data_objects = importlib.import_module("data_objects")
tmux_commands = importlib.import_module("tmux_commands")
utils = importlib.import_module("utils")


def main() -> None:
    config_file_path = utils.get_config_file_path()
    window_base_index = tmux_commands.get_window_base_index()
    pane_base_index = tmux_commands.get_pane_base_index()
    session_name = tmux_commands.get_tmux_session_name()

    if not config_file_path:
        return

    parsed_configuration = utils.parse_config_file(config_file_path=config_file_path)

    if parsed_configuration is None:
        return

    configurations = utils.generate_configurations(
        parsed_configuration=parsed_configuration
    )
    shared = utils.parse_shared_values(parsed_configuration=parsed_configuration)
    window_index = tmux_commands.get_current_tmux_window_index()

    config_index = window_index - window_base_index
    if 0 <= config_index < len(configurations):
        utils.run_configuration(
            configuration=configurations[config_index],
            shared_configuration=shared,
            session_name=session_name,
            window_base_index=window_base_index,
            pane_base_index=pane_base_index,
            index=config_index,
            create_or_rename=constants.WindowNamingOption.rename,
        )


main()
