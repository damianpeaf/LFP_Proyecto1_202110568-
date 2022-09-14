

import math
from lexer.lexer import Lexer
from tokens.Operation import OperationType
from tokens.Token import Token, TokenType


class Generation():

    htmlStr = ""

    def __init__(self):
        pass

    @staticmethod
    def generateHTML():
        tokens = Lexer.tokenFlow
        errors = Lexer.lexicErrors

        tokenNumber = 0
        while tokenNumber < len(tokens):
            analizedToken = Lexer.tokenFlow[tokenNumber]

            # make math operation
            if analizedToken.tokenType == TokenType.OPEN_TAG and analizedToken.operation and analizedToken.operation.operationType != OperationType.ESCRIBIR:
                result = Generation.evalExpresion(tokenNumber)
                print(result['expStr'] + " = " + str(result['result']))
                # Go to closing tag
                for skipTokenNumber in range(tokenNumber, len(tokens)):
                    haveToSkipNOpeningtags = 0
                    if tokens[skipTokenNumber].tokenType == TokenType.OPEN_TAG:
                        haveToSkipNOpeningtags += 1
                    elif tokens[skipTokenNumber].tokenType == TokenType.CLOSING_TAG:
                        haveToSkipNOpeningtags -= 1
                        if haveToSkipNOpeningtags == -1:
                            tokenNumber = skipTokenNumber
                            # print('Skiping operation own content')
                            break
            tokenNumber += 1

    @staticmethod
    def evalExpresion(tokenNumber: int):
        try:
            tokens = Lexer.tokenFlow
            analizedToken = Lexer.tokenFlow[tokenNumber]
            number1Token = tokens[tokenNumber+1]
            number2Token = tokens[tokenNumber+2]

            operationType = analizedToken.operation.operationType
            expStr = ""
            expResult = 0

            # * Operation with 2 numbers
            if operationType == OperationType.SUMA or operationType == OperationType.RESTA or operationType.MULTIPLICACION == OperationType.DIVISION or operationType == OperationType.POTENCIA or operationType.RAIZ or operationType.MOD:
                # ? has 2 pure numbers
                if number1Token.tokenType == TokenType.NUMBER and number2Token.tokenType == TokenType.NUMBER:
                    expStr = Generation.evalOperationAsString(
                        analizedToken, number1Token.value, number2Token.value)
                    expResult = Generation.evalOperation(
                        analizedToken, number1Token.value, number2Token.value)

                # ? has 1 pure number and 1 operation
                elif (number1Token.tokenType == TokenType.NUMBER and (number2Token.tokenType == TokenType.OPEN_TAG and number2Token.operation)) or (number2Token.tokenType == TokenType.NUMBER and (number1Token.tokenType == TokenType.OPEN_TAG and number1Token.operation)):

                    # * Number 2 is the operation
                    if number2Token.tokenType == TokenType.OPEN_TAG and number2Token.operation:
                        partialResult = Generation.evalExpresion(tokenNumber+2)
                        expStr = Generation.evalOperationAsString(
                            analizedToken, number1Token.value, "("+partialResult['expStr']+")")
                        expResult = Generation.evalOperation(
                            analizedToken, number1Token.value, partialResult['result'])
                    # * Number 1 is the operation
                    else:
                        partialResult = Generation.evalExpresion(tokenNumber+1)
                        expStr = Generation.evalOperationAsString(
                            analizedToken, "("+partialResult['expStr']+")", number2Token.value)
                        expResult = Generation.evalOperation(
                            analizedToken, partialResult['result'], number2Token.value)

                # ? has 2 operations
                elif (number1Token.tokenType == TokenType.OPEN_TAG and number1Token.operation) and (number2Token.tokenType == TokenType.OPEN_TAG and number2Token.operation):
                    partialResult1 = Generation.evalExpresion(tokenNumber+1)
                    partialResult2 = Generation.evalExpresion(tokenNumber+2)
                    expStr = Generation.evalOperationAsString(
                        analizedToken, "("+partialResult1['expStr']+")", "("+partialResult2['expStr']+")")
                    expResult = Generation.evalOperation(
                        analizedToken, partialResult1['result'], partialResult2['result'])

            # * Operation with 1 number
            elif operationType == OperationType.SENO or operationType == OperationType.COSENO or operationType == OperationType.TANGENTE or operationType == OperationType.INVERSO:
                # ? has 1 pure number
                if number1Token.tokenType == TokenType.NUMBER:
                    expStr = Generation.evalOperationAsString(
                        analizedToken, number1Token.tokenType, number1Token.value)
                    expResult = Generation.evalOperation(
                        analizedToken, number1Token.tokenType, number1Token.value)

                # ? has 1 operation
                elif number1Token.tokenType == TokenType.OPEN_TAG and number1Token.operation:
                    partialResult1 = Generation.evalExpresion(tokenNumber+1)
                    expStr = Generation.evalOperationAsString(
                        analizedToken, number1Token.tokenType, "("+partialResult1['expStr']+")")
                    expResult = Generation.evalOperation(
                        analizedToken, number1Token.tokenType, partialResult1['result'])

            else:
                print('Operation not found')

            return {
                'expStr': expStr,
                'result': expResult
            }

        except Exception as e:
            print(e)
            pass

    @staticmethod
    def evalOperation(parentToken: Token, n1: float, n2: float):
        operation = parentToken.operation.operationType

        if operation == OperationType.SUMA:
            return n1 + n2
        elif operation == OperationType.RESTA:
            return n1 - n2
        elif operation == OperationType.MULTIPLICACION:
            return n1 * n2
        elif operation == OperationType.DIVISION:
            return n1 / n2
        elif operation == OperationType.POTENCIA:
            return n1 ** n2
        elif operation == OperationType.RAIZ:
            return n1 ** (1/n2)
        elif operation == OperationType.MOD:
            return n1 % n2
        elif operation == OperationType.SENO:
            return math.sin(n1)
        elif operation == OperationType.COSENO:
            return math.cos(n1)
        elif operation == OperationType.TANGENTE:
            return math.tan(n1)
        elif operation == OperationType.INVERSO:
            return 1 / n1
        else:
            # ! ERROR
            print(operation)
            print('OPERACION NO REALIZADA')
            pass

    @staticmethod
    def evalOperationAsString(parentToken: Token, n1: str, n2: str):
        operation = parentToken.operation.operationType

        n1 = str(n1)
        n2 = str(n2)

        if operation == OperationType.SUMA:
            return n1 + "+" + n2
        elif operation == OperationType.RESTA:
            return n1 + "-" + n2
        elif operation == OperationType.MULTIPLICACION:
            return n1 + "*" + n2
        elif operation == OperationType.DIVISION:
            return n1 + "/" + n2
        elif operation == OperationType.POTENCIA:
            return n1 + "^(" + n2+")"
        elif operation == OperationType.RAIZ:
            return n1 + "^(1/" + n2+")"
        elif operation == OperationType.MOD:
            return n1 + "%" + n2
        elif operation == OperationType.SENO:
            return "sin("+n1+")"
        elif operation == OperationType.COSENO:
            return "cos("+n1+")"
        elif operation == OperationType.TANGENTE:
            return"tan("+n1+")"
        elif operation == OperationType.INVERSO:
            return "1/("+n1+")"
        else:
            # ! ERROR
            print(operation)
            print('EXP STRING NO REALIZADA')
            pass

#     # * Operation with 2 numbers
#         # ? has 2 pure numbers
#         # ? has 1 pure number and 1 operation
#         # ? has 2 operations

#     # * Operation with 1 number
#         # ? has 1 pure number
#         # ? has 1 operation
#     # ! ERROR
