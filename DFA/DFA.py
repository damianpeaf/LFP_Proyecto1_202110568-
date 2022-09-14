
from typing import List
from DFA.DFAState import DFAState
from DFA.DFATransitionFunction import DFATransitionFunction
from lexer.constants.alphabet import ALPHABET
from lexer.constants.digit import DIGITS
from tokens.Token import Token, TokenType
import graphviz


class DFA ():

    def __init__(self, initialState: DFAState, states: List[DFAState], transitionFunctions: List[DFATransitionFunction]):
        # * Main props
        self.alphabet = ALPHABET
        self.initialState = initialState
        self.states = states
        self.transitionFunctions = transitionFunctions

        # * other props
        self.reset()

    def evalCharacter(self, character, isCharacterNext, row, col):

        # * Not in alphabet, not valid character
        if character not in self.alphabet:
            # ? Character
            return Token(TokenType.ERROR, character, row, col)

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
                            return Token(self.actualState.tokenType, self.cleanLexeme(), row, col)
                        else:
                            # * Incomplete lexema
                            return Token(TokenType.ERROR, self.lexeme, row, col)

                    # * New state set, keeps running
                    return True

        # * No related function

        # * Check if actual state is acceptance
        if self.actualState.isAcceptance:
            # * VALID TOKEN
            # !!! Lexemes adyascent
            self.validCharacter = False
            return Token(self.actualState.tokenType, self.cleanLexeme(), row, col)

        # * No valid lexeme
        self.lexeme += character
        return Token(TokenType.ERROR, self.lexeme, row, col)

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
            if function.characters == DIGITS:
                label = "D"
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

    def reset(self):
        # * reset eval props
        self.validCharacter = None
        self.actualState = self.initialState
        self.lexeme = ""
