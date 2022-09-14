

from enum import Enum, auto

from tokens.Operation import Operation


class TokenType(Enum):
    ERROR = auto()
    OPEN_TAG = auto()
    AUTOCLOSING_TAG = auto()
    CLOSING_TAG = auto()
    CONTENT = auto()
    NUMBER = auto()
    EOF = auto()


class Token():

    def __init__(self, tokenType: TokenType, value: str, row: int = None, col: int = None):
        self.tokenType = tokenType
        self.value = value
        self.row = row
        self.col = col
        self.operation: Operation = None
