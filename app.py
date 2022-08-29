
from errors.LexicError import LexerError, LexerErrorType
from lexer.constants.languageDFA import languageDFA
from lexer.lexer import Lexer
from tokens.Token import Token, TokenType


dfa = languageDFA()

# dot = dfaProbe.generateDOT(True)

file = open('entrada.txt', 'r', encoding='utf-8')

lines = file.readlines()


row = 1
for line in lines:
    line = line.replace('\n', '')
    column = 1

    i = 0
    while i < len(line):

        evaluatedCharacter = line[i]

        isCharacterNext = i < len(line)-1
        dfaResp = dfa.evalCharacter(evaluatedCharacter, isCharacterNext)

        if isinstance(dfaResp, Token):

            print(dfa.validCharacter)
            Lexer.addToken(dfaResp)

            # ! VALIDATE TOKEN TYPE ERROR
            if dfaResp.tokenType == TokenType.ERROR:
                if len(dfaResp.value) == 1:
                    Lexer.addError(
                        LexerError(LexerErrorType.INVALID_CHARACTER,
                                   dfaResp.value, 'Caracter invalido', row, column)
                    )
                    i += 1
                    continue
                else:
                    Lexer.addError(
                        LexerError(LexerErrorType.INCOMPLETE_LEXEME,
                                   dfaResp.value, 'Lexema invalido', row, column)
                    )

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

    print(f'TIPO:  {token.tokenType} VALUE: {token.value}')


print(' \n ERRORES GENERADOS : \n')

for error in Lexer.lexicErrors:
    print(
        f'TIPO:  {error.type} - VALUE: {error.lexeme} - COL: {error.column} - ROW: {error.row}')
