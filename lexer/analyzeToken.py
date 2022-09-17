from lexer.constants.attributeDFA import attributeDFA
from tokens.auxTokens import AuxToken


def analyzeToken(line):

    dfa = attributeDFA()
    i = 0
    auxTokens = []

    while i < len(line):

        evaluatedCharacter = line[i]

        isCharacterNext = i < len(line)-1
        dfaResp = dfa.evalCharacter(
            evaluatedCharacter, isCharacterNext)

        if isinstance(dfaResp, AuxToken):
            auxTokens.append(dfaResp)
            # ! New lexeme
            if dfa.validCharacter == False:
                dfa.reset()
                continue

            dfa.reset()

        i += 1
    return auxTokens
