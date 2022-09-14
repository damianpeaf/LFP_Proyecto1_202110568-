

from enum import Enum, auto


class LexerErrorType(Enum):
    INVALID_CHARACTER = auto()
    INCOMPLETE_LEXEME = auto()
    INVALID_OPERATION = auto()
    INVALID_OPERATION_ASSIGMENT = auto()
    INVALID_OPERATION_TAG = auto()
    EXPECTED_CONTENT = auto()
    EXPECTED_NUMBER = auto()
    EXPECTED_CLOSING_TAG = auto()


class LexerError():

    def __init__(self, type: LexerErrorType, lexeme: str, msg: str = None, row: int = None, col: int = None):
        self.type = type
        self.lexeme = lexeme

        # ? optional
        self.msg = msg
        self.row = row
        self.column = col
