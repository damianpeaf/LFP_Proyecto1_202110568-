from errors.LexicError import LexerError, LexerErrorType
from lexer.constants.languageDFA import languageDFA
from lexer.generation import Generation
from lexer.lexer import Lexer
from tokens.Token import Token, TokenType


def analyzeFile(path: str):

    Lexer.tokenFlow = []
    Lexer.lexicErrors = []

    dfa = languageDFA()

    file = open(path, 'r', encoding='utf-8')

    lines = file.readlines()

    row = 1
    for line in lines:
        line = line.replace('\n', '')
        column = 1

        i = 0
        while i < len(line):

            evaluatedCharacter = line[i]

            isCharacterNext = i < len(line)-1
            dfaResp = dfa.evalCharacter(
                evaluatedCharacter, isCharacterNext, row, column)

            if isinstance(dfaResp, Token):

                # ! VALIDATE TOKEN TYPE ERROR
                if dfaResp.tokenType == TokenType.ERROR:
                    # just a blank space
                    if dfaResp.value.strip() == '':
                        # print('monton de espcios en blanco')
                        pass
                    elif len(dfaResp.value) == 1:
                        Lexer.addError(
                            LexerError(LexerErrorType.INVALID_CHARACTER,
                                       dfaResp.value, 'Caracter invalido', row, column)
                        )

                    else:
                        Lexer.addError(
                            LexerError(LexerErrorType.INCOMPLETE_LEXEME,
                                       dfaResp.value, 'Lexema incompleto o invalido', row, column)
                        )
                    column += 1
                    i += 1
                    dfa.reset()
                    continue

                Lexer.addToken(dfaResp)

                # ! New lexeme
                if dfa.validCharacter == False:
                    dfa.reset()
                    continue

                dfa.reset()

            i += 1
            column += 1

        row += 1

    print(' \n TOKEN GENERADOS : \n')

    for token in Lexer.tokenFlow:

        operation = "-"

        if token.operation:
            operation = token.operation.operationType.name

        print(
            f'TIPO:  {token.tokenType} VALUE: {token.value} ')
    Lexer.generateIntermdiateTokens()

    Generation.generateHTML()

    print(' \n ERRORES GENERADOS : \n')

    for error in Lexer.lexicErrors:
        print(
            f'TIPO:  {error.type} - VALUE: {error.lexeme} - COL: {error.column} - ROW: {error.row}')
