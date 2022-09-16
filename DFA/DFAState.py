

from tokens.Token import TokenType


class DFAState():

    def __init__(self, number: int, isAcceptance: bool = False, tokenType: TokenType = None):
        try:
            self.number = int(number)
        except:
            self.number = -1
            print('Nombre de estado invalido')

        self.isAcceptance = isAcceptance

        if self.isAcceptance:
            self.tokenType = tokenType
        else:
            if tokenType:
                # print('No se esperaba que este estado generara un token')
                pass
