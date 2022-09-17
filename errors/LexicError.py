

from enum import Enum, auto


class ErrorType(Enum):
    INVALID_CHARACTER = auto()
    INCOMPLETE_LEXEME = auto()
    INVALID_OPERATION = auto()
    INVALID_TAG = auto()
    INVALID_OPERATION_ASSIGMENT = auto()
    INVALID_OPERATION_TAG = auto()
    EXPECTED_CONTENT = auto()
    EXPECTED_NUMBER = auto()
    EXPECTED_CLOSING_TAG = auto()
    MISSING_CLOSING_TAG = auto()


class DocumentError():

    def __init__(self, type: ErrorType, lexeme: str, msg: str = None, row: int = None, col: int = None):
        self.type = type
        self.lexeme = lexeme

        # ? optional
        self.msg = msg
        self.row = row
        self.column = col
