
from typing import List
from errors.LexicError import DocumentError, ErrorType
from tokens.Operation import Operation, OperationType
from tokens.Token import Token, TokenType


class Lexer():

    tokenFlow: List[Token] = []
    documentErrors: List[DocumentError] = []

    validOpenAndClosingTags = ['Tipo', 'Operacion', 'Texto', 'Funcion',
                               'Estilo', 'Numero', 'Titulo', 'Descripcion', 'Contenido']
    validAutoclosingTags = ['Titulo', 'Descripcion', 'Contenido']

    def __init__(self):
        pass

    @staticmethod
    def addToken(token: Token):
        Lexer.tokenFlow.append(token)

    @staticmethod
    def getCriticalErrors():
        criticalErrors: List[DocumentError] = []
        for error in Lexer.documentErrors:
            if error.type == ErrorType.INVALID_OPERATION or error.type == ErrorType.INVALID_TAG or error.type == ErrorType.INVALID_OPERATION_ASSIGMENT or error.type == ErrorType.EXPECTED_CONTENT or error.type == ErrorType.EXPECTED_NUMBER or error.type == ErrorType.EXPECTED_CLOSING_TAG or error.type == ErrorType.MISSING_CLOSING_TAG:
                criticalErrors.append(error)

        return criticalErrors

    @staticmethod
    def getTolerableErrors():
        tolerableErrors: List[DocumentError] = []
        for error in Lexer.documentErrors:
            if error.type == ErrorType.INVALID_CHARACTER or error.type == ErrorType.INCOMPLETE_LEXEME:
                tolerableErrors.append(error)

        return tolerableErrors

    @staticmethod
    def addError(error: DocumentError):
        Lexer.documentErrors.append(error)

    @staticmethod
    def reset():
        Lexer.tokenFlow = []
        Lexer.documentErrors = []

    @staticmethod
    def generateIntermdiateTokens():
        Lexer.evaluateValidTags()
        Lexer.evaluateClosingTags()
        Lexer.generateNumbers()
        Lexer.generateOperationTokens()

    @staticmethod
    def evaluateValidTags():
        for token in Lexer.tokenFlow:

            # * Validates if number or content
            if token.tokenType == TokenType.NUMBER or token.tokenType == TokenType.CONTENT:
                continue

            formatedTokenValue = token.getMainValue()

            if token.tokenType == TokenType.OPEN_TAG or token.tokenType == TokenType.CLOSING_TAG:
                # * Valid token value
                if formatedTokenValue in Lexer.validOpenAndClosingTags:
                    continue
            # * Same for autoclosing tags
            elif token.tokenType == TokenType.AUTOCLOSING_TAG:
                if formatedTokenValue in Lexer.validAutoclosingTags:
                    continue

            # ! Then is an error
            # * Remove token from the flow
            Lexer.tokenFlow.remove(token)

            # * Generate error

            Lexer.addError(DocumentError(ErrorType.INVALID_TAG,
                           formatedTokenValue, 'Etiqueta invalida', token.col, token.row))

    @staticmethod
    def evaluateClosingTags():
        for tokenNumber in range(0, len(Lexer.tokenFlow)):
            analyzedToken = Lexer.tokenFlow[tokenNumber]
            # * If its a open tag token
            if analyzedToken.tokenType == TokenType.OPEN_TAG:
                # * Search for its closing tag, needs to find 1 closing tag
                needToFind = 1
                for nextTokenNumber in range(tokenNumber+1, len(Lexer.tokenFlow)):
                    nextToken = Lexer.tokenFlow[nextTokenNumber]
                    # * if finds same open tag value, needs to skip +1 closing tag
                    sameValue = nextToken.getMainValue() == analyzedToken.getMainValue()
                    if nextToken.tokenType == TokenType.OPEN_TAG:
                        if sameValue:
                            needToFind += 1
                    # * If finds a closing tag, eval if have to skip it
                    elif nextToken.tokenType == TokenType.CLOSING_TAG:
                        # * It haves a closing tag
                        if sameValue:
                            needToFind -= 1
                            if needToFind == 0:
                                break

                    # * If eval all tokens
                    if nextTokenNumber == len(Lexer.tokenFlow) - 1:
                        Lexer.addError(DocumentError(ErrorType.MISSING_CLOSING_TAG, analyzedToken.value,
                                       'Hace falta la etiqueta de cierre', analyzedToken.row, analyzedToken.col))

    @staticmethod
    def generateNumbers():

        try:
            tokenNumber = 0
            while tokenNumber < len(Lexer.tokenFlow):
                token = Lexer.tokenFlow[tokenNumber]
                nextToken = Lexer.tokenFlow[tokenNumber+1]
                nextNextToken = Lexer.tokenFlow[tokenNumber+2]

                if token.tokenType == TokenType.OPEN_TAG:
                    if token.getMainValue() == "Numero":
                        if nextToken.tokenType == TokenType.CONTENT:
                            try:
                                number = float(nextToken.value)

                                if nextNextToken.tokenType == TokenType.CLOSING_TAG:
                                    Lexer.tokenFlow[tokenNumber] = Token(
                                        TokenType.NUMBER, number, token.row, token.col)
                                    Lexer.tokenFlow.remove(nextToken)
                                    Lexer.tokenFlow.remove(nextNextToken)
                                else:
                                    Lexer.addError(DocumentError(ErrorType.EXPECTED_CLOSING_TAG, nextToken.value,
                                                   'Se esperaba una etiqueta de cierre', nextNextToken.row, nextNextToken.col))

                            except Exception as e:
                                print(e)
                                Lexer.addError(DocumentError(
                                    ErrorType.EXPECTED_NUMBER, nextToken.value, 'Se esperaba un numero', nextToken.row, nextToken.col))
                        else:
                            Lexer.addError(DocumentError(ErrorType.EXPECTED_CONTENT, nextToken.value,
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
            if tokenProps[0] == 'Operacion' or tokenProps[0] == 'Funcion':
                if len(tokenProps) == 2:
                    if tokenProps[0] == 'Operacion' or tokenProps[0] == 'Funcion':
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
                            Lexer.addError(DocumentError(ErrorType.INVALID_OPERATION,
                                                         tokenProps[1], 'Operacion invalida', token.row, token.col))
                else:
                    Lexer.addError(DocumentError(ErrorType.INVALID_OPERATION_ASSIGMENT, token.value,
                                                 'Asignacion de operacion invalida', token.row, token.col))
