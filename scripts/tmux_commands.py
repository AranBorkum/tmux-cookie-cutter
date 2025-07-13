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


def get_window_width(index: int, session: str) -> int:
    width = subprocess.run(
        [
            "tmux",
            "display",
            "-t",
            f"{session}:{index}",
            "-p",
            "#{window_width}",
        ],
        capture_output=True,
        text=True,
    ).stdout
    return int(width)


def get_window_height(index: int, session: str) -> int:
    width = subprocess.run(
        [
            "tmux",
            "display",
            "-t",
            f"{session}:{index}",
            "-p",
            "#{window_height}",
        ],
        capture_output=True,
        text=True,
    ).stdout
    return int(width)


def resize_pane_horizontally(
    window_index: int, pane_index: int, session: str, size: int
) -> None:
    target_width = get_window_width(index=window_index, session=session) * size // 100
    subprocess.run(
        [
            "tmux",
            "resize-pane",
            "-t",
            f"{session}:{window_index}.{pane_index}",
            "-x",
            f"{target_width}",
        ]
    )


def resize_pane_vertically(
    window_index: int, pane_index: int, session: str, size: int
) -> None:
    target_height = get_window_height(index=window_index, session=session) * size // 100
    subprocess.run(
        [
            "tmux",
            "resize-pane",
            "-t",
            f"{session}:{window_index}.{pane_index}",
            "-y",
            f"{target_height}",
        ]
    )
