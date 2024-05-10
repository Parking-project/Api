from enum import IntEnum, auto

class ReserveStatus(IntEnum):
    DELETED = auto()
    SENDED = auto()
    APPROVE = auto()
    PAYED = auto()