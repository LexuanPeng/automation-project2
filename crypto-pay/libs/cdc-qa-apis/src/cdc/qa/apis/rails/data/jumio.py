from enum import unique, Enum, auto


@unique
class DocumentType(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name

    ID_CARD = auto()
    PASSPORT = auto()
    DRIVING_LICENSE = auto()
