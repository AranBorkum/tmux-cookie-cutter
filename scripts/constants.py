import enum
import pathlib

FILE_NAME = ".tmux-cookie-cutter.yaml"
CONFIG_PATH = pathlib.Path.joinpath(pathlib.Path.home(), ".config")
DEFAULT_WINDOW_NAME = "default_window_name"


class SplitDirection(enum.StrEnum):
    horizontal = "horizontal"
    vertical = "vertical"


class WindowNamingOption(enum.StrEnum):
    create = "create"
    rename = "rename"
