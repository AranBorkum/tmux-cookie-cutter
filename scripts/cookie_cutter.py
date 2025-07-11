import dataclasses
import enum
import subprocess
from pathlib import Path

import yaml

FILE_NAME = ".tmux-cookie-cutter.yaml"
CONFIG_PATH = Path.joinpath(Path.home(), ".config")


class SplitDirection(enum.StrEnum):
    horizontal = "horizontal"
    vertical = "vertical"


@dataclasses.dataclass(frozen=True)
class PaneConfig:
    command: str | None
    split_direction: SplitDirection
    envvars: list[str] | None
    setup_command: str | None


@dataclasses.dataclass(frozen=True)
class Config:
    name: str
    command: str | None
    envvars: list[str] | None
    setup_command: str | None
    panes: list[PaneConfig]


def get_tmux_session_name() -> str:
    return subprocess.run(
        ["tmux", "display-message", "#{session_name}"],
        capture_output=True,
        text=True,
    ).stdout


def create_tmux_window(name: str, session: str) -> None:
    subprocess.run(
        [
            "tmux",
            "new-window",
            "-t",
            session,
            "-n",
            name,
        ]
    )


def rename_tmux_window(name: str, index: int, session: str) -> None:
    subprocess.run(["tmux", "rename-window", "-t", f"{session}:{index}", name])


def set_environment_variables(
    envvars: list[str] | None, index: int, session: str
) -> None:
    if not envvars:
        return
    for envvar in envvars:
        subprocess.run(
            [
                "tmux",
                "send-keys",
                "-t",
                f"{session}:{index}",
                f"export {envvar}",
                "C-m",
            ]
        )


def run_setup_command(command: str | None, index: int, session: str) -> None:
    if not command:
        return
    subprocess.run(
        [
            "tmux",
            "send-keys",
            "-t",
            f"{session}:{index}",
            command,
            "C-m",
        ]
    )


def run_command(command: str | None, index: int, session: str) -> None:
    if not command:
        return
    subprocess.run(
        [
            "tmux",
            "send-keys",
            "-t",
            f"{session}:{index}",
            command,
            "C-m",
        ]
    )


def clear_terminal(index: int, session: str) -> None:
    subprocess.run(
        [
            "tmux",
            "send-keys",
            "-t",
            f"{session}:{index}",
            "clear",
            "C-m",
        ]
    )


def split_window(index: int, session: str, direction: SplitDirection) -> None:
    split_flag = "-v" if direction == SplitDirection.horizontal else "-h"
    subprocess.run(["tmux", "split-window", "-t", f"{session}:{index}", split_flag])


def get_config_file_path() -> str:
    if Path(FILE_NAME).is_file():
        return FILE_NAME
    else:
        default_path = Path.joinpath(CONFIG_PATH, FILE_NAME)
        if Path(default_path).is_file():
            return default_path


def generate_configurations(config_file_path: str) -> list[Config]:
    parsed_configurations = yaml.safe_load(open(config_file_path))
    configurations = []
    for configuration in parsed_configurations.values():
        pane_configuration = []
        if pane_configs := configuration.get("panes"):
            pane_configuration = [
                PaneConfig(
                    command=pane_config.get("command"),
                    split_direction=SplitDirection(pane_config["split_direction"]),
                    envvars=configuration.get("envvars"),
                    setup_command=configuration.get("setup_command"),
                )
                for pane_config in pane_configs.values()
            ]

        configurations.append(
            Config(
                name=configuration["name"],
                command=configuration.get("command"),
                envvars=configuration.get("envvars"),
                setup_command=configuration.get("setup_command"),
                panes=pane_configuration,
            )
        )
    return configurations


def run_pane_configuration(
    pane_configuration: PaneConfig, index: int, session: str
) -> None:
    split_window(
        index=index,
        session=session,
        direction=pane_configuration.split_direction,
    )
    set_environment_variables(
        envvars=pane_configuration.envvars,
        index=index,
        session=session,
    )
    run_setup_command(
        command=pane_configuration.setup_command,
        index=index,
        session=session,
    )
    run_command(
        command=pane_configuration.command,
        index=index,
        session=session,
    )

    clear_terminal(index=index, session=session)


def run_configurations(
    configurations: list[Config],
    session_name: str,
) -> None:
    for index, configuration in enumerate(configurations):
        if index == 0:
            rename_tmux_window(
                name=configuration.name, session=session_name, index=index + 1
            )
        else:
            create_tmux_window(name=configuration.name, session=session_name)

        set_environment_variables(
            envvars=configuration.envvars,
            index=index + 1,
            session=session_name,
        )
        run_setup_command(
            command=configuration.setup_command,
            index=index + 1,
            session=session_name,
        )
        run_command(
            command=configuration.command,
            index=index + 1,
            session=session_name,
        )

        for pane in configuration.panes:
            run_pane_configuration(
                pane_configuration=pane, index=index + 1, session=session_name
            )

        clear_terminal(index=index + 1, session=session_name)


def main():
    config_file_path = get_config_file_path()
    session_name = get_tmux_session_name()
    configurations = generate_configurations(config_file_path=config_file_path)
    run_configurations(
        configurations=configurations,
        session_name=session_name,
    )


main()
