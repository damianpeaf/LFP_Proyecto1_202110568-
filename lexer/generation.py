

from lib2to3.pytree import convert
import math
from turtle import pos
from lexer.htmlParser import HtmlParser
from lexer.lexer import Lexer
from tokens.Operation import OperationType
from tokens.Token import Token, TokenType


class Generation():

    htmlStr = ""

    def __init__(self):
        pass

    @staticmethod
    def generateHTML():

        criticalErrors = Lexer.getCriticalErrors()

        if len(criticalErrors) > 0:
            return False

        # 3 phases, scope, references/documentStructure, and html generation

        scopes = Generation.languageScopes()
        documentStructure = Generation.documentStructure(scopes)
        print(documentStructure)
        HtmlParser(documentStructure).createFile()

        return True

    @staticmethod
    def documentStructure(scope):

        tokens = Lexer.tokenFlow

        documentParts = {
            "TITULO": [],
            "DESCRIPCION": [],
            "CONTENIDO": [],
            "ESTILOS_TITULO": [],
            "ESTILOS_DESCRIPCION": [],
            "ESTILOS_CONTENIDO": [],
        }

        COLORS = {
            "AZUL": "background-color: blue;",
            "ROJO": "background-color: red;",
            "VERDE": "background-color: green;",
            "GRIS": "background-color: gray;",
        }

        tokenNumber = 0
        while tokenNumber < len(tokens):
            analizedToken = tokens[tokenNumber]

            # * "Funcion=Escribir"
            if analizedToken.tokenType == TokenType.OPEN_TAG and analizedToken.getMainValue() == 'Funcion' and analizedToken.operation.operationType == OperationType.ESCRIBIR:
                # watch inside tokens (title, description, content)
                documentPart = None
                for contentTokenNumber in range(tokenNumber+1, len(tokens)):
                    contentToken = tokens[contentTokenNumber]

                    # watch until finds Closing tag or pass throught all tokens
                    if contentToken.tokenType == TokenType.CLOSING_TAG and contentToken.getMainValue() == 'Funcion':
                        break

                    if contentToken.tokenType == TokenType.OPEN_TAG and contentToken.getMainValue() == 'Titulo':
                        documentPart = "TITULO"
                        continue
                    elif contentToken.tokenType == TokenType.OPEN_TAG and contentToken.getMainValue() == 'Descripcion':
                        documentPart = "DESCRIPCION"
                        continue
                    elif contentToken.tokenType == TokenType.OPEN_TAG and contentToken.getMainValue() == 'Contenido':
                        documentPart = "CONTENIDO"
                        continue

                    # content of the posible referece

                    if contentToken.tokenType == TokenType.CONTENT:
                        if not documentPart:
                            continue
                        # reference
                        if contentToken.value.strip().upper() == '[TEXTO]':
                            documentParts[documentPart] += scope['TEXTO']
                        elif contentToken.value.strip().upper() == '[TIPO]':
                            documentParts[documentPart] += scope['TIPO']
                        else:
                            # just content
                            if contentToken.tokenType == TokenType.CONTENT:
                                documentParts[documentPart] += [
                                    contentToken.value]
                            else:
                                # No content
                                documentParts[documentPart] += ['']

             # * "ESTILO"
            if analizedToken.tokenType == TokenType.OPEN_TAG and analizedToken.getMainValue() == 'Estilo':
                # watch inside tokens (title, description, content)
                documentPart = None
                for contentTokenNumber in range(tokenNumber+1, len(tokens)):
                    contentToken = tokens[contentTokenNumber]

                    # watch until finds Closing tag or pass throught all tokens
                    if contentToken.tokenType == TokenType.CLOSING_TAG and contentToken.getMainValue() == 'Estilo':
                        break

                    if contentToken.tokenType == TokenType.AUTOCLOSING_TAG and contentToken.getMainValue() == 'Titulo':
                        documentPart = "ESTILOS_TITULO"
                    elif contentToken.tokenType == TokenType.AUTOCLOSING_TAG and contentToken.getMainValue() == 'Descripcion':
                        documentPart = "ESTILOS_DESCRIPCION"
                    elif contentToken.tokenType == TokenType.AUTOCLOSING_TAG and contentToken.getMainValue() == 'Contenido':
                        documentPart = "ESTILOS_CONTENIDO"
                    else:
                        continue

                    # Eval atributes
                    for atr in contentToken.getAtributes():
                        print(atr)
                        for clave in atr:
                            try:
                                # Color
                                if clave == "Color":
                                    documentParts[documentPart].append(
                                        COLORS[atr[clave]])
                                # font size
                                elif clave == "Tamanio":
                                    documentParts[documentPart].append(
                                        f"font-size: {atr[clave]};")
                            except:
                                print('ERROR EN EL ATRIBUTO')

            tokenNumber += 1

        return documentParts

    @staticmethod
    def languageScopes():
        tokens = Lexer.tokenFlow

        documentScopes = {
            "TEXTO": [],
            "TIPO": []
        }

        tokenNumber = 0

        actualScope = []
        # * General operations (Text and Math operations)
        while tokenNumber < len(tokens):
            analizedToken = Lexer.tokenFlow[tokenNumber]

            # * Select the scope
            if analizedToken.tokenType == TokenType.OPEN_TAG and analizedToken.getMainValue().upper() == 'TEXTO':
                actualScope = documentScopes["TEXTO"]
                tokenNumber += 1
                continue

            elif analizedToken.tokenType == TokenType.OPEN_TAG and analizedToken.getMainValue().upper() == 'TIPO':
                actualScope = documentScopes["TIPO"]
                tokenNumber += 1
                continue

            # * Skip tags

            # "funcion" reference

            if analizedToken.tokenType == TokenType.OPEN_TAG and analizedToken.getMainValue() == 'Funcion':
                for skipTokenNumber in range(tokenNumber+1, len(tokens)):
                    # until its close tag
                    if tokens[skipTokenNumber].tokenType == TokenType.CLOSING_TAG and tokens[skipTokenNumber].getMainValue() == 'Funcion':
                        tokenNumber = skipTokenNumber
                continue

            # "Estilo" tag
            if analizedToken.tokenType == TokenType.OPEN_TAG and analizedToken.getMainValue() == 'Estilo':
                for skipTokenNumber in range(tokenNumber+1, len(tokens)):
                    # until its close tag
                    if tokens[skipTokenNumber].tokenType == TokenType.CLOSING_TAG and tokens[skipTokenNumber].getMainValue() == 'Estilo':
                        tokenNumber = skipTokenNumber
                continue

            # Closing tags (just for optimization)
            if analizedToken.tokenType == TokenType.CLOSING_TAG:
                tokenNumber += 1
                continue
            # * OPERATIONS *
            scopeObject = None

            # * Math operation
            if analizedToken.tokenType == TokenType.OPEN_TAG and analizedToken.operation and analizedToken.operation.operationType != OperationType.ESCRIBIR:
                operationAsString = Generation.makeOperation(tokenNumber)
                # result = Generation.evalExpresion(tokenNumber)
                # scopeObject = result['expStr'] + " = " + str(result['result'])
                scopeObject = operationAsString + \
                    " = " + str(eval(operationAsString))

                # Go to closing tag
                needToFind = 1
                for skipTokenNumber in range(tokenNumber+1, len(tokens)):
                    if tokens[skipTokenNumber].tokenType == TokenType.OPEN_TAG:
                        needToFind += 1
                    elif tokens[skipTokenNumber].tokenType == TokenType.CLOSING_TAG:
                        needToFind -= 1
                        if needToFind == 0:
                            # set the new token numbe to go
                            tokenNumber = skipTokenNumber
                            break

            # * Just content
            if analizedToken.tokenType == TokenType.CONTENT:
                scopeObject = analizedToken.value

            # * Add the object to the scope
            if scopeObject:
                print(scopeObject)
                actualScope.append(scopeObject)

            tokenNumber += 1

        return documentScopes

#     # * Operation with 2 numbers
#         # ? has 2 pure numbers
#         # ? has 1 pure number and 1 operation
#         # ? has 2 operations

#     # * Operation with 1 number
#         # ? has 1 pure number
#         # ? has 1 operation
#     # ! ERROR

    @staticmethod
    def makeOperation(tokenNumber: int):

        tokens = Lexer.tokenFlow
        operationToken = tokens[tokenNumber]
        operationType = operationToken.operation.operationType

        operationTokenNumberOfClosingTag = tokenNumber+1

        needsToFind = 1
        for posibleTokenNumber in range(tokenNumber+1, len(tokens)):
            posibleToken = tokens[posibleTokenNumber]
            if posibleToken.tokenType == TokenType.OPEN_TAG:
                needsToFind += 1
            elif posibleToken.tokenType == TokenType.CLOSING_TAG:
                needsToFind -= 1
                if needsToFind == 0:
                    operationTokenNumberOfClosingTag = posibleTokenNumber
                    break

        # first number

        operation = ""
        n = tokenNumber+2
        firstNumberToken = tokens[tokenNumber+1]

        if firstNumberToken.tokenType == TokenType.NUMBER:
            if operationType == OperationType.SENO or operationType == OperationType.COSENO or operationType == OperationType.TANGENTE or operationType == OperationType.INVERSO:
                return Generation.concatSign(
                    operationToken, str(firstNumberToken.value))
            else:
                operation = str(firstNumberToken.value)
        elif firstNumberToken.tokenType == TokenType.OPEN_TAG and firstNumberToken.operation:
            if operationType == OperationType.SENO or operationType == OperationType.COSENO or operationType == OperationType.TANGENTE or operationType == OperationType.INVERSO:
                return Generation.concatSign(operationToken, str(Generation.makeOperation(tokenNumber+1)))
            else:
                operation = Generation.makeOperation(tokenNumber+1)

            for posibleTokenNumber in range(tokenNumber+1, len(tokens)):
                posibleToken = tokens[posibleTokenNumber]
                if posibleToken.tokenType == TokenType.OPEN_TAG:
                    needsToFind += 1
                elif posibleToken.tokenType == TokenType.CLOSING_TAG:
                    needsToFind -= 1
                    if needsToFind == 0:
                        n = posibleTokenNumber+1
                        break

        print(operationTokenNumberOfClosingTag)

        # starts on second number
        while n < operationTokenNumberOfClosingTag:
            nextNumber = tokens[n]
            if nextNumber.tokenType == TokenType.NUMBER:
                operation += Generation.concatSign(
                    operationToken, nextNumber.value)
            elif nextNumber.tokenType == TokenType.OPEN_TAG and nextNumber.operation:
                partialResult = Generation.makeOperation(n)
                operation += Generation.concatSign(
                    operationToken, "("+partialResult+")")
                needsToFind = 1
                for posibleTokenNumber in range(n+1, len(tokens)):
                    posibleToken = tokens[posibleTokenNumber]
                    if posibleToken.tokenType == TokenType.OPEN_TAG:
                        needsToFind += 1
                    elif posibleToken.tokenType == TokenType.CLOSING_TAG:
                        needsToFind -= 1
                        if needsToFind == 0:
                            n = posibleTokenNumber+1
                            break
                continue
            n += 1

        return operation

    @staticmethod
    def evalExpresion(tokenNumber: int):
        tokens = Lexer.tokenFlow
        analizedToken = Lexer.tokenFlow[tokenNumber]

        n1 = tokenNumber+1
        n2 = tokenNumber+2

        number1Token = tokens[n1]
        number2Token = tokens[n2]

        operationType = analizedToken.operation.operationType
        expStr = "NaO"
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
            # * Number 1 -> number ; Number 2 -> operation
            elif number1Token.tokenType == TokenType.NUMBER and (number2Token.tokenType == TokenType.OPEN_TAG and number2Token.operation):
                partialResult = Generation.evalExpresion(tokenNumber+2)
                expStr = Generation.evalOperationAsString(
                    analizedToken, number1Token.value, "("+partialResult['expStr']+")")
                expResult = Generation.evalOperation(
                    analizedToken, number1Token.value, partialResult['result'])

                # * Number 1 is the operation
                # 2 posibilites, n2 is number, or n2 is operation
            else:
                if number1Token.tokenType == TokenType.OPEN_TAG and number1Token.operation:

                    # Eval n1 (first operation)
                    partialResult1 = Generation.evalExpresion(
                        tokenNumber+1)

                    # find the closing tag of the first operation, needs to find 1 closing tag
                    needsToFind = 1
                    for posibleTokenNumber in range(tokenNumber+2, len(tokens)):
                        posibleToken = tokens[posibleTokenNumber]
                        if posibleToken.tokenType == TokenType.OPEN_TAG:
                            needsToFind += 1
                        elif posibleToken.tokenType == TokenType.CLOSING_TAG:
                            needsToFind -= 1
                            if needsToFind == 0:
                                n2 = posibleTokenNumber+1
                                break

                    # 2 posibilites, n2 is number, or n2 is operation
                    # n2 is number
                    number2Token = tokens[n2]
                    if number2Token.tokenType == TokenType.NUMBER:
                        expStr = Generation.evalOperationAsString(
                            analizedToken, "("+partialResult1['expStr']+")", number2Token.value)
                        expResult = Generation.evalOperation(
                            analizedToken, partialResult1['result'], number2Token.value)
                    # n2 is operation
                    elif number2Token.tokenType == TokenType.OPEN_TAG and number2Token.operation:
                        partialResult2 = Generation.evalExpresion(
                            n2)
                        expStr = Generation.evalOperationAsString(
                            analizedToken, "("+partialResult1['expStr']+")", "("+partialResult2['expStr']+")")
                        expResult = Generation.evalOperation(
                            analizedToken, partialResult1['result'], partialResult2['result'])

                        # Resets n2 to final bracket
                        needsToFind = 1
                        for posibleTokenNumber in range(n2+1, len(tokens)):
                            posibleToken = tokens[posibleTokenNumber]
                            if posibleToken.tokenType == TokenType.OPEN_TAG:
                                needsToFind += 1
                            elif posibleToken.tokenType == TokenType.CLOSING_TAG:
                                needsToFind -= 1
                                if needsToFind == 0:
                                    n2 = posibleTokenNumber
                                    break
                    else:
                        print('THIS NOT VALIDATED')
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

        # Recursive call for next numbers
        if tokens[n2+1].tokenType != TokenType.CLOSING_TAG:
            print('has numbers yet')
            # Convert n1 to parent token
            tokens[n1] = analizedToken
            # convert n2 to n1 and n2 result
            tokens[n2].value = expResult
            tokens[n2].tokenType = TokenType.NUMBER

            print(tokens[n1].value)
            print(tokens[n1].tokenType)
            print(tokens[n2].value)
            print(tokens[n2].tokenType)
            print(tokens[n2+1].value)
            print(tokens[n2+1].tokenType)
            finalResult = Generation.evalExpresion(n1)
            expStr = finalResult['expStr']
            expResult = finalResult['result']

        return {
            'expStr': expStr,
            'result': expResult
        }

        # except Exception as e:
        #     print(e)
        #     pass

    @ staticmethod
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

    @ staticmethod
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

    @ staticmethod
    def concatSign(operationToken: Token, rightNumber: str):
        operation = operationToken.operation.operationType
        rightNumber = str(rightNumber)

        if operation == OperationType.SUMA:
            return f"+{rightNumber}"
        elif operation == OperationType.RESTA:
            return f"-{rightNumber}"
        elif operation == OperationType.MULTIPLICACION:
            return f"*{rightNumber}"
        elif operation == OperationType.DIVISION:
            return f"/{rightNumber}"
        elif operation == OperationType.POTENCIA:
            return f"**{rightNumber}"
        elif operation == OperationType.RAIZ:
            return f"**1/({rightNumber})"
        elif operation == OperationType.MOD:
            return f"%{rightNumber}"
        elif operation == OperationType.SENO:
            return f"math.sin({rightNumber})"
        elif operation == OperationType.COSENO:
            return f"math.cos({rightNumber})"
        elif operation == OperationType.TANGENTE:
            return f"math.tan({rightNumber})"
        elif operation == OperationType.INVERSO:
            return f"1/({rightNumber})"
        else:
            # ! ERROR
            print(operation)
            print('EXP STRING NO REALIZADA')
            pass

            # # ! NEEDS TO FIND THE 2ND OPERATION
            # # ? has 2 operations
            # elif (number1Token.tokenType == TokenType.OPEN_TAG and number1Token.operation) and (number2Token.tokenType == TokenType.OPEN_TAG and number2Token.operation):
            #     partialResult1 = Generation.evalExpresion(tokenNumber+1)
            #     partialResult2 = Generation.evalExpresion(tokenNumber+2)
            #     expStr = Generation.evalOperationAsString(
            #         analizedToken, "("+partialResult1['expStr']+")", "("+partialResult2['expStr']+")")
            #     expResult = Generation.evalOperation(
            #         analizedToken, partialResult1['result'], partialResult2['result'])
