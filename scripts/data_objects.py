import dataclasses
import importlib

constants = importlib.import_module("constants")


@dataclasses.dataclass(frozen=True)
class PaneConfig:
    command: str | None
    split_direction: constants.SplitDirection
    envvars: list[str] | None
    setup_command: str | None


@dataclasses.dataclass(frozen=True)
class Config:
    name: str
    command: str | None
    envvars: list[str] | None
    setup_command: str | None
    panes: list[PaneConfig]
