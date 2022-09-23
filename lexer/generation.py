

from lib2to3.pytree import convert
import math
from pprint import pprint
from turtle import pos
from lexer.htmlParser import HtmlParser
from lexer.htmlParser2 import HtmlParser2
from lexer.lexer import Lexer
from lexer.utils.closingTag import getClosingTagNumber
from tokens.Operation import OperationType
from tokens.Token import Token, TokenType


class Generation():

    def __init__(self):
        pass

    @staticmethod
    def generateHTML(errors=False):

        criticalErrors = Lexer.getCriticalErrors()
        if errors:
            HtmlParser2().createFile()
            return True

        if len(criticalErrors) > 0:
            return False

        # 3 phases, scope, references/documentStructure, and html generation

        print(' \n OPERACIONES : \n')
        scopes = Generation.languageScopes()

        print(' \n ESTRUCTURA : \n')
        documentStructure = Generation.documentStructure(scopes)

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
            "AZUL": "color: blue;",
            "ROJO": "color: red;",
            "VERDE": "color: green;",
            "GRIS": "color: gray;",
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

        pprint(documentParts)

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

        operationType = ""
        while tokenNumber < len(tokens):
            analizedToken = Lexer.tokenFlow[tokenNumber]

            # * Select the scope
            if analizedToken.tokenType == TokenType.OPEN_TAG and analizedToken.getMainValue().upper() == 'TEXTO':
                actualScope = documentScopes["TEXTO"]
                print("\n\nSCOPE: TEXTO \n")
                tokenNumber += 1
                continue

            elif analizedToken.tokenType == TokenType.OPEN_TAG and analizedToken.getMainValue().upper() == 'TIPO':
                actualScope = documentScopes["TIPO"]
                tokenNumber += 1
                print("\n\nSCOPE: TIPO \n")
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
                scopeObject = operationAsString.replace('math.', '') + \
                    " = " + str(eval(operationAsString))
                operationType = "CALCULAR"

                # Go to closing tag

                tokenNumber = getClosingTagNumber(tokenNumber+1)

            # * Just content
            if analizedToken.tokenType == TokenType.CONTENT:
                scopeObject = analizedToken.value
                operationType = "ESCRIBIR"

            # * Add the object to the scope
            if scopeObject:
                print(operationType + " : " + scopeObject)
                actualScope.append(scopeObject)

            tokenNumber += 1

        return documentScopes

    @staticmethod
    def makeOperation(tokenNumber: int):

        tokens = Lexer.tokenFlow
        operationToken = tokens[tokenNumber]
        operationType = operationToken.operation.operationType

        operationTokenNumberOfClosingTag = getClosingTagNumber(tokenNumber+1)

        # first number
        operation = ""
        n = tokenNumber+2
        firstNumberToken = tokens[tokenNumber+1]

        # If first token is number
        if firstNumberToken.tokenType == TokenType.NUMBER:
            # One number operation
            if operationType == OperationType.SENO or operationType == OperationType.COSENO or operationType == OperationType.TANGENTE or operationType == OperationType.INVERSO:
                return Generation.concatSign(
                    operationToken, str(firstNumberToken.value))
            else:
                operation = str(firstNumberToken.value)

        # If first token is operation
        elif firstNumberToken.tokenType == TokenType.OPEN_TAG and firstNumberToken.operation:
            if operationType == OperationType.SENO or operationType == OperationType.COSENO or operationType == OperationType.TANGENTE or operationType == OperationType.INVERSO:
                return "("+Generation.concatSign(operationToken, str(Generation.makeOperation(tokenNumber+1)))+")"
            else:
                operation = "("+Generation.makeOperation(tokenNumber+1)+")"
            # resets the where start
            n = getClosingTagNumber(tokenNumber+2)+1

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
                n = getClosingTagNumber(n+1)+1
                continue
            n += 1

        return operation

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
            return f"**(1/({rightNumber}))"
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
            pass
