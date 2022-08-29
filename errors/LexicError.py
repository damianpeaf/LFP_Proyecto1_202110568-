

from enum import Enum, auto


class LexerErrorType(Enum):
    INVALID_CHARACTER = auto()
    INCOMPLETE_LEXEME = auto()


class LexerError():

    def __init__(self, type: LexerErrorType, lexeme: str, msg: str = None, row: int = None, col: int = None):
        self.type = type
        self.lexeme = lexeme

        # ? optional
        self.msg = msg
        self.row = row
        self.column = col
