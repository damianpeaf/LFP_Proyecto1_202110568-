

from enum import Enum, auto
from typing import List
from lexer.analyzeToken import analyzeToken
from tokens.Operation import Operation
from tokens.auxTokens import AuxTokenTypes


class TokenType(Enum):
    ERROR = auto()
    OPEN_TAG = auto()
    AUTOCLOSING_TAG = auto()
    CLOSING_TAG = auto()
    CONTENT = auto()
    NUMBER = auto()


class Token():

    def __init__(self, tokenType: TokenType, value: str, row: int = None, col: int = None):
        self.tokenType = tokenType
        self.value = value
        self.row = row
        self.col = col
        self.operation: Operation = None
        self.auxTokens: List[Token] = []

    def runAttibuteRecognition(self):
        self.auxTokens = analyzeToken(self.value)

    def getMainValue(self):
        # * Removes = and uses ' ' as delimiter for words
        self.runAttibuteRecognition()
        return self.auxTokens[0].value.replace(' ', '').split('=')[0]

    def getAtributes(self):
        # NOMBRE COLOR=AZUL COLOR = AZUL
        self.runAttibuteRecognition()
        wordsInTag = []

        for token in self.auxTokens:
            if token.tokenType == AuxTokenTypes.ATTRIBUTE:
                wordsInTag.append(token.value.replace(' ', ''))

        atributes = []
        for word in wordsInTag:
            word = word.strip()
            if word == self.getMainValue():
                continue
            if "=" in word:
                atr = word.split('=')
                atributes.append({atr[0]: atr[1]})
            else:
                print('ERROR EN EL ATRIBUTO')

        return atributes
