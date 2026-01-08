import importlib

constants = importlib.import_module("constants")
data_objects = importlib.import_module("data_objects")
tmux_commands = importlib.import_module("tmux_commands")
utils = importlib.import_module("utils")


def run_cookie_cutter(
    configurations: list[data_objects.Config],
    shared_configuration: data_objects.SharedValues,
    session_name: str,
    window_base_index: int,
    pane_base_index: int,
) -> None:
    for index, configuration in enumerate(configurations):
        create_or_rename = (
            constants.WindowNamingOption.rename
            if index == 0
            else constants.WindowNamingOption.create
        )
        utils.run_configuration(
            configuration=configuration,
            shared_configuration=shared_configuration,
            session_name=session_name,
            window_base_index=window_base_index,
            pane_base_index=pane_base_index,
            index=index,
            create_or_rename=create_or_rename,
        )

    tmux_commands.select_window(
        window_index=window_base_index + 1,
        session=session_name,
    )
    tmux_commands.select_window(
        window_index=window_base_index,
        session=session_name,
    )


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
    run_cookie_cutter(
        configurations=configurations,
        shared_configuration=shared,
        session_name=session_name,
        window_base_index=window_base_index,
        pane_base_index=pane_base_index,
    )


main()
