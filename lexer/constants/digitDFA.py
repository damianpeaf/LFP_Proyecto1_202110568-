

from tokenize import Token
from DFA.DFA import DFA
from DFA.DFAState import DFAState
from DFA.DFATransitionFunction import DFATransitionFunction
from lexer.constants.digit import DIGITS
from tokens.Token import TokenType


def generateDigitDFA(initialStateNumber=0, finalStateNumber=1):

    initialState = DFAState(initialStateNumber)
    finalState = DFAState(finalStateNumber, True, TokenType.CONTENT)

    states = [initialState, finalState]

    initToFinal = DFATransitionFunction(initialState, finalState, DIGITS)
    finalToFinal = DFATransitionFunction(finalState, finalState, DIGITS)

    functions = [initToFinal, finalToFinal]

    return DFA(initialState, states, functions)


def digitDFAProps(stateNumber: int= -1, isFinalState = False):

    finalState = DFAState(stateNumber, isFinalState, TokenType.CONTENT)

    finalToFinal = DFATransitionFunction(finalState, finalState, DIGITS)


    return {
        'state': finalState,
        'function': finalToFinal
    }
