import importlib
import subprocess

constants = importlib.import_module("constants")


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


def split_window(
    index: int,
    session: str,
    direction: constants.SplitDirection,
) -> None:
    split_flag = "-v" if direction == constants.SplitDirection.horizontal else "-h"
    subprocess.run(
        [
            "tmux",
            "split-window",
            "-t",
            f"{session}:{index}",
            split_flag,
        ]
    )


def select_window(window_index: int, session: str) -> None:
    subprocess.run(
        [
            "tmux",
            "select-window",
            "-t",
            f"{session}:{window_index}",
        ]
    )
