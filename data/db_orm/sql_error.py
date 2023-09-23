from enum import Enum, auto


class SQLError(Enum):
    duplicate_entry = auto()
    not_found = auto()

