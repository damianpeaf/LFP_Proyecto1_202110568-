from errors.LexicError import DocumentError, ErrorType
from lexer.constants.attributeDFA import attributeDFA
from lexer.constants.languageDFA import languageDFA
from lexer.lexer import Lexer
from tokens.Token import Token, TokenType


def analyzeFile(path: str):

    Lexer.reset()
    dfa = languageDFA()

    file = open(path, 'r', encoding='utf-8')

    lines = file.readlines()

    row = 1
    for line in lines:
        line = line.replace('\n', '')
        line = line.replace('\t', '')
        column = 1

        i = 0
        while i < len(line):

            evaluatedCharacter = line[i]

            isCharacterNext = i < len(line)-1
            dfaResp = dfa.evalCharacter(
                evaluatedCharacter, isCharacterNext, row, column)

            if isinstance(dfaResp, Token):

                # Useless blank space
                if dfaResp.tokenType == TokenType.CONTENT:
                    if dfaResp.value.strip() == '':
                        dfa.reset()
                        if not isCharacterNext:
                            i += 1
                        continue

                # ! VALIDATE TOKEN TYPE ERROR
                if dfaResp.tokenType == TokenType.ERROR:
                    # just a blank space
                    if len(dfaResp.value) == 1:
                        Lexer.addError(
                            DocumentError(ErrorType.INVALID_CHARACTER,
                                          dfaResp.value, 'Caracter invalido', row, column)
                        )
                        # * Doest reset for posible valid lexeme

                    else:
                        Lexer.addError(
                            DocumentError(ErrorType.INCOMPLETE_LEXEME,
                                          dfaResp.value, 'Lexema incompleto o invalido', row, column)
                        )
                        # * Reset for next lexeme

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
        print(row)
    Lexer.generateIntermdiateTokens()

    print(' \n TOKEN GENERADOS : \n')

    tokenNumber = 0
    for token in Lexer.tokenFlow:

        operation = "-"

        if token.operation:
            operation = token.operation.operationType.name

        print(
            f'#{str(tokenNumber)} TIPO:  {token.tokenType} VALUE: {token.value} ')
        tokenNumber += 1
    print(' \n ERRORES GENERADOS : \n')

    for error in Lexer.documentErrors:
        print(
            f'TIPO:  {error.type} - VALUE: {error.lexeme} - COL: {error.column} - ROW: {error.row}')
