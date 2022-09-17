from distutils.log import ERROR
from enum import Enum, auto


class AuxTokenTypes(Enum):
    ATTRIBUTE = auto()
    MAIN_VALUE = auto()
    ERROR = auto()


class AuxToken():

    def __init__(self, tokenType: AuxTokenTypes, value: str):
        self.tokenType = tokenType
        self.value = value
