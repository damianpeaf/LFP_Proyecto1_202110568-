
from typing import List
from errors.LexicError import LexerError, LexerErrorType
from tokens.Operation import Operation, OperationType
from tokens.Token import Token, TokenType


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

    @staticmethod
    def generateIntermdiateTokens():
        Lexer.generateNumbers()
        Lexer.generateOperationTokens()

    @staticmethod
    def generateNumbers():

        try:
            tokenNumber = 0
            while tokenNumber < len(Lexer.tokenFlow):
                token = Lexer.tokenFlow[tokenNumber]
                nextToken = Lexer.tokenFlow[tokenNumber+1]
                nextNextToken = Lexer.tokenFlow[tokenNumber+2]

                if token.tokenType == TokenType.OPEN_TAG:
                    if token.value.upper() == "NUMERO":
                        if nextToken.tokenType == TokenType.CONTENT:
                            try:
                                number = float(nextToken.value)

                                if nextNextToken.tokenType == TokenType.CLOSING_TAG:
                                    Lexer.tokenFlow[tokenNumber] = Token(
                                        TokenType.NUMBER, number, token.row, token.col)
                                    Lexer.tokenFlow.remove(nextToken)
                                    Lexer.tokenFlow.remove(nextNextToken)
                                else:
                                    Lexer.addError(LexerError(LexerErrorType.EXPECTED_CLOSING_TAG, nextToken.value,
                                                   'Se esperaba una etiqueta de cierre', nextNextToken.row, nextNextToken.col))

                            except Exception as e:
                                print(e)
                                Lexer.addError(LexerError(
                                    LexerErrorType.EXPECTED_NUMBER, nextToken.value, 'Se esperaba un numero', nextToken.row, nextToken.col))
                        else:
                            Lexer.addError(LexerError(LexerErrorType.EXPECTED_CONTENT, nextToken.value,
                                           'Se esperaba un contenido dentro de las etiquetas', nextToken.row, nextToken.col))

                        # token = Token(TokenType.NUMBER, token.value, token.row, token.column)
                tokenNumber += 1

        except:
            pass

    @staticmethod
    def generateOperationTokens():

        # Eval all tokens
        for token in Lexer.tokenFlow:

            # * Eval if token is a number
            if token.tokenType == TokenType.NUMBER:
                continue

            # * manipulates token value
            formatedTokenValue = token.value.replace(" ", "")

            # * if is not a operation token
            if "=" not in formatedTokenValue:
                continue

            # * searchs for =
            tokenProps = formatedTokenValue.split("=")

            # * valid props
            if tokenProps[0].upper() == 'OPERACION' or tokenProps[0].upper() == 'FUNCION':
                if len(tokenProps) == 2:
                    if tokenProps[0].upper() == 'OPERACION' or tokenProps[0].upper() == 'FUNCION':
                        # * Is a operation/fuction

                        operation = None

                        for operationType in OperationType:
                            if operationType.name == tokenProps[1].upper():
                                operation = Operation(operationType)
                                break

                        if operation:
                            token.operation = operation
                        else:
                            token.tokenType = TokenType.ERROR
                            Lexer.addError(LexerError(LexerErrorType.INVALID_OPERATION,
                                                      tokenProps[1], 'Operacion invalida', token.row, token.col))
                else:
                    Lexer.addError(LexerError(LexerErrorType.INVALID_OPERATION_ASSIGMENT, token.value,
                                              'Asignacion de operacion invalida', token.row, token.col))
