import dataclasses
import importlib

constants = importlib.import_module("constants")


@dataclasses.dataclass(frozen=True)
class PaneConfig:
    command: str | None
    split_direction: constants.SplitDirection
    envvars: list[str] | None
    setup_command: str | None
    size: int | None


@dataclasses.dataclass(frozen=True)
class Config:
    name: str
    command: str | None
    envvars: list[str] | None
    setup_command: str | None
    panes: list[PaneConfig]


@dataclasses.dataclass(frozen=True)
class SharedValues:
    envvars: list[str] | None
    setup_command: str | None
