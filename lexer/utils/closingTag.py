

from lexer.lexer import Lexer
from tokens.Token import TokenType


def getClosingTagNumber(startTokenNumber):
    tokens = Lexer.tokenFlow
    needsToFind = 1
    for posibleTokenNumber in range(startTokenNumber, len(tokens)):
        posibleToken = tokens[posibleTokenNumber]
        if posibleToken.tokenType == TokenType.OPEN_TAG:
            needsToFind += 1
        elif posibleToken.tokenType == TokenType.CLOSING_TAG:
            needsToFind -= 1
            if needsToFind == 0:
                return posibleTokenNumber
