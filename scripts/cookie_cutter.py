import importlib
import typing
from pathlib import Path

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


def parse_config_file(config_file_path: Path) -> dict[str, typing.Any] | None:
    try:
        import yaml

        return yaml.safe_load(open(config_file_path))
    except ModuleNotFoundError:
        tmux_commands.show_warning_message()
        return None


def generate_pane_configurations(
    configuration: dict[str, typing.Any],
) -> list[data_objects.PaneConfig]:
    pane_configs = configuration.get("panes")

    if pane_configs is None:
        return []

    return [
        data_objects.PaneConfig(
            command=pane_config.get("command"),
            split_direction=constants.SplitDirection(pane_config["split_direction"]),
            envvars=configuration.get("envvars"),
            setup_command=configuration.get("setup_command"),
            size=pane_config.get("size"),
        )
        for pane_config in pane_configs
    ]


def generate_configurations(
    parsed_configuration: dict[str, typing.Any],
) -> list[data_objects.Config]:
    return [
        data_objects.Config(
            name=configuration["name"],
            command=configuration.get("command"),
            envvars=configuration.get("envvars"),
            setup_command=configuration.get("setup_command"),
            panes=generate_pane_configurations(
                configuration=configuration,
            ),
        )
        for configuration in parsed_configuration["default_windows"]
    ]


def parse_shared_values(
    parsed_configuration: dict[str, typing.Any],
) -> data_objects.SharedValues:
    configuration = parsed_configuration.get("shared")
    if not configuration:
        return data_objects.SharedValues(
            envvars=None,
            setup_command=None,
        )
    return data_objects.SharedValues(
        envvars=configuration.get("envvars"),
        setup_command=configuration.get("setup_command"),
    )


def run_pane_configuration(
    pane_configuration: data_objects.PaneConfig,
    shared_configuration: data_objects.SharedValues,
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
        envvars=shared_configuration.envvars,
        index=window_index,
        session=session,
    )
    tmux_commands.run_setup_command(
        command=shared_configuration.setup_command,
        index=window_index,
        session=session,
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
    shared_configuration: data_objects.SharedValues,
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
            envvars=shared_configuration.envvars,
            index=index + window_base_index,
            session=session_name,
        )
        tmux_commands.run_setup_command(
            command=shared_configuration.setup_command,
            index=index + window_base_index,
            session=session_name,
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
                shared_configuration=shared_configuration,
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


def main() -> None:
    config_file_path = get_config_file_path()
    window_base_index = tmux_commands.get_window_base_index()
    pane_base_index = tmux_commands.get_pane_base_index()
    session_name = tmux_commands.get_tmux_session_name()

    if not config_file_path:
        return

    parsed_configuration = parse_config_file(config_file_path=config_file_path)

    if parsed_configuration is None:
        return

    configurations = generate_configurations(parsed_configuration=parsed_configuration)
    shared = parse_shared_values(parsed_configuration=parsed_configuration)
    run_configurations(
        configurations=configurations,
        shared_configuration=shared,
        session_name=session_name,
        window_base_index=window_base_index,
        pane_base_index=pane_base_index,
    )


main()
