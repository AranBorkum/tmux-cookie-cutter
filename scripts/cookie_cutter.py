import importlib
from pathlib import Path

import yaml

constants = importlib.import_module("constants")
data_objects = importlib.import_module("data_objects")
tmux_commands = importlib.import_module("tmux_commands")

FILE_NAME = ".tmux-cookie-cutter.yaml"
CONFIG_PATH = Path.joinpath(Path.home(), ".config")


def get_config_file_path() -> Path | None:
    file_path = Path(FILE_NAME)
    if file_path.is_file():
        return file_path
    else:
        default_path = Path.joinpath(CONFIG_PATH, FILE_NAME)
        if Path(default_path).is_file():
            return default_path
    return None


def generate_configurations(config_file_path: Path) -> list[data_objects.Config]:
    parsed_configurations = yaml.safe_load(open(config_file_path))
    configurations = []
    for configuration in parsed_configurations["default_windows"]:
        pane_configuration = []
        if pane_configs := configuration.get("panes"):
            pane_configuration = [
                data_objects.PaneConfig(
                    command=pane_config.get("command"),
                    split_direction=constants.SplitDirection(
                        pane_config["split_direction"]
                    ),
                    envvars=configuration.get("envvars"),
                    setup_command=configuration.get("setup_command"),
                    size=pane_config.get("size"),
                )
                for pane_config in pane_configs
            ]

        configurations.append(
            data_objects.Config(
                name=configuration["name"],
                command=configuration.get("command"),
                envvars=configuration.get("envvars"),
                setup_command=configuration.get("setup_command"),
                panes=pane_configuration,
            )
        )
    return configurations


def run_pane_configuration(
    pane_configuration: data_objects.PaneConfig,
    window_index: int,
    pane_index: int,
    session: str,
) -> None:
    tmux_commands.split_window(
        index=window_index,
        session=session,
        direction=pane_configuration.split_direction,
    )
    tmux_commands.set_environment_variables(
        envvars=pane_configuration.envvars,
        index=window_index,
        session=session,
    )
    tmux_commands.run_setup_command(
        command=pane_configuration.setup_command,
        index=window_index,
        session=session,
    )
    tmux_commands.run_command(
        command=pane_configuration.command,
        index=window_index,
        session=session,
    )
    if not pane_configuration.size:
        return

    match pane_configuration.split_direction:
        case constants.SplitDirection.vertical:
            tmux_commands.resize_pane_horizontally(
                window_index=window_index,
                pane_index=pane_index,
                session=session,
                size=pane_configuration.size,
            )
        case constants.SplitDirection.horizontal:
            tmux_commands.resize_pane_vertically(
                window_index=window_index,
                pane_index=pane_index,
                session=session,
                size=pane_configuration.size,
            )


def run_configurations(
    configurations: list[data_objects.Config],
    session_name: str,
    window_base_index: int,
    pane_base_index: int,
) -> None:
    for index, configuration in enumerate(configurations):
        if index == 0:
            tmux_commands.rename_tmux_window(
                name=configuration.name,
                session=session_name,
                index=index + window_base_index,
            )
        else:
            tmux_commands.create_tmux_window(
                name=configuration.name, session=session_name
            )

        tmux_commands.set_environment_variables(
            envvars=configuration.envvars,
            index=index + window_base_index,
            session=session_name,
        )
        tmux_commands.run_setup_command(
            command=configuration.setup_command,
            index=index + window_base_index,
            session=session_name,
        )
        tmux_commands.run_command(
            command=configuration.command,
            index=index + window_base_index,
            session=session_name,
        )

        for pane_index, pane in enumerate(configuration.panes):
            run_pane_configuration(
                pane_configuration=pane,
                window_index=index + window_base_index,
                pane_index=pane_index + pane_base_index + 1,
                session=session_name,
            )

    tmux_commands.select_window(
        window_index=window_base_index + 1,
        session=session_name,
    )
    tmux_commands.select_window(
        window_index=window_base_index,
        session=session_name,
    )


def main():
    config_file_path = get_config_file_path()
    window_base_index = tmux_commands.get_window_base_index()
    pane_base_index = tmux_commands.get_pane_base_index()

    if not config_file_path:
        return

    session_name = tmux_commands.get_tmux_session_name()
    configurations = generate_configurations(config_file_path=config_file_path)
    run_configurations(
        configurations=configurations,
        session_name=session_name,
        window_base_index=window_base_index,
        pane_base_index=pane_base_index,
    )


main()
