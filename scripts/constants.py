import enum


class SplitDirection(enum.StrEnum):
    horizontal = "horizontal"
    vertical = "vertical"


class WindowNamingOption(enum.StrEnum):
    create = "create"
    rename = "rename"
