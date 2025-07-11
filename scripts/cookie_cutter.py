import dataclasses
import subprocess
from pathlib import Path

import yaml

FILE_NAME = ".cookie-cutter.yaml"
CONFIG_PATH = Path.joinpath(Path.home(), ".config")


@dataclasses.dataclass(frozen=True)
class Config:
    name: str
    command: str | None
    envvars: list[str] | None
    setup_command: str | None


def get_tmux_session_name() -> str:
    return subprocess.run(
        ["tmux", "display-message", "#{session_name}"],
        capture_output=True,
        text=True,
    ).stdout


def create_tmux_window(name: str, session: str) -> None:
    print(session)
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
    print(session)
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


def get_config_file_path() -> str:
    if Path(FILE_NAME).is_file():
        return FILE_NAME
    else:
        default_path = Path.joinpath(CONFIG_PATH, FILE_NAME)
        if Path(default_path).is_file():
            return default_path


def generate_configurations(config_file_path: str) -> list[Config]:
    parsed_configurations = yaml.safe_load(open(config_file_path))
    return [
        Config(
            name=configuration["name"],
            command=configuration.get("command"),
            envvars=configuration.get("envvars"),
            setup_command=configuration.get("setup_command"),
        )
        for configuration in parsed_configurations.values()
    ]


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


def main():
    config_file_path = get_config_file_path()
    session_name = get_tmux_session_name()
    configurations = generate_configurations(config_file_path=config_file_path)
    run_configurations(
        configurations=configurations,
        session_name=session_name,
    )


main()
