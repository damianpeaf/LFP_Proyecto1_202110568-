
from typing import List
from errors.LexicError import LexerError
from lexer.constants.digitDFA import generateDigitDFA
from tokens.Token import Token


class Lexer():

    tokenFlow: List[Token] = []
    lexicErrors: List[LexerError] = []

    def __init__(self):
        pass

    @staticmethod
    def addToken(token: Token):
        Lexer.tokenFlow.append(token)

    @staticmethod
    def addError(error: LexerError):
        Lexer.lexicErrors.append(error)

    @staticmethod
    def reset():
        Lexer.tokenFlow = []
        Lexer.lexicErrors = []
