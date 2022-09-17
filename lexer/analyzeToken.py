from lexer.constants.attributeDFA import attributeDFA
from tokens.auxTokens import AuxToken


def analyzeToken(line, column, row):

    dfa = attributeDFA()
    i = 0
    auxTokens = []

    while i < len(line):

        evaluatedCharacter = line[i]

        isCharacterNext = i < len(line)-1
        dfaResp = dfa.evalCharacter(
            evaluatedCharacter, isCharacterNext, row, column)

        if isinstance(dfaResp, AuxToken):
            # ! VALIDATE TOKEN TYPE ERROR
            if dfaResp.tokenType == TokenType.ERROR:
                # just a blank space
                if len(dfaResp.value) == 1:
                    Lexer.addError(
                        DocumentError(ErrorType.INVALID_CHARACTER,
                                      dfaResp.value, 'Caracter invalido', row, column)
                    )
                    dfa.reset()
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

            auxTokens.append(dfaResp)
            # ! New lexeme
            if dfa.validCharacter == False:
                dfa.reset()
                continue

            dfa.reset()

        i += 1
        column += 1
