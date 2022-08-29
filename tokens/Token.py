

from enum import Enum, auto


class TokenType(Enum):
    ERROR = auto()
    OPEN_TAG = auto()
    AUTOCLOSING_TAG = auto()
    CLOSING_TAG = auto()
    CONTENT = auto()
    EOF = auto()


class Token():

    def __init__(self, tokenType: TokenType, value: str):
        self.tokenType = tokenType
        self.value = value
