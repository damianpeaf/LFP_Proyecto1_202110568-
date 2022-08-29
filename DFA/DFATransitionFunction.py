

from lib2to3.pgen2.pgen import DFAState
from typing import List


class DFATransitionFunction():

    def __init__(self, prevState: DFAState, nextState: DFAState, characters: List[str]):
        self.prevState = prevState
        self.nextState = nextState
        self.characters = characters
