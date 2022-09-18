
from typing import List
from DFA.DFAState import DFAState
from DFA.DFATransitionFunction import DFATransitionFunction
from lexer.constants.alphabet import ALPHABET
from lexer.constants.digit import DIGITS
from lexer.constants.letter import LETTERS
from tokens.auxTokens import AuxToken, AuxTokenTypes
import graphviz


class DFA2 ():

    def __init__(self, initialState: DFAState, states: List[DFAState], transitionFunctions: List[DFATransitionFunction]):
        # * Main props
        self.alphabet = ALPHABET
        self.initialState = initialState
        self.states = states
        self.transitionFunctions = transitionFunctions

        # * other props
        self.reset()

    def evalCharacter(self, character, isCharacterNext):

        # * Not in alphabet, not valid character
        if character not in self.alphabet:
            # ? Character
            return AuxToken(AuxTokenTypes.ERROR, character)

        # * Looks for next state

        for function in self.transitionFunctions:

            # * Transition function related to actual state
            if function.prevState == self.actualState:

                # * Able to go to next state
                if character in function.characters:
                    self.actualState = function.nextState

                    self.lexeme += character

                    # * There is no character next
                    if not isCharacterNext:
                        # * Eval if new state is acceptance
                        if self.actualState.isAcceptance:
                            # * VALID TOKEN
                            self.validCharacter = True
                            return AuxToken(self.actualState.tokenType, self.cleanLexeme())
                        else:
                            # * Incomplete lexema
                            return AuxToken(AuxTokenTypes.ERROR, self.lexeme)

                    # * New state set, keeps running
                    return True

        # * No related function

        # * Check if actual state is acceptance
        if self.actualState.isAcceptance:
            # * VALID TOKEN
            # !!! Lexemes adyascent
            self.validCharacter = False
            return AuxToken(self.actualState.tokenType, self.cleanLexeme())

        # * No valid lexeme
        self.lexeme += character
        return AuxToken(AuxTokenTypes.ERROR, self.lexeme)

    def generateDOT(self, render=False):
        dot = graphviz.Digraph('DFA', comment='DFA :)')

        # * Creates nodes

        for state in self.states:
            nodeName = f'S{state.number}'
            if state.isAcceptance:
                dot.node(nodeName, nodeName, shape='doublecircle')
                continue
            dot.node(nodeName, nodeName, shape='circle')

        # * Create edges

        for function in self.transitionFunctions:

            label = ""
            # * Label abreviation for all digits
            if function.characters == LETTERS:
                label = "L"
            elif function.characters == [' ']:
                label = "b"
            else:
                label = ', '.join(function.characters)

            dot.edge(f'S{function.prevState.number}',
                     f'S{function.nextState.number}',  f' {label} ')

        if render:
            dot.render(directory='dfa-graphs', view=True)
            return

        return dot

    def cleanLexeme(self):
        return self.lexeme.replace('<', '').replace('>', '').replace('/', '')
        # return self.lexeme

    def reset(self):
        # * reset eval props
        self.validCharacter = None
        self.actualState = self.initialState
        self.lexeme = ""
