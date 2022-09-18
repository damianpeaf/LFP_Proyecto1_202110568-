

from typing import List
from DFA.DFA2 import DFA2
from DFA.DFAState import DFAState
from DFA.DFATransitionFunction import DFATransitionFunction
from lexer.constants.letter import LETTERS
from tokens.auxTokens import AuxTokenTypes


def attributeDFA():

    # * Initial State
    initialState = DFAState(0)
    initialStateTransitionFunction1 = DFATransitionFunction(
        initialState, initialState, [' '])

    # * First state
    firstState = DFAState(1)
    firstStateTransitionFunction1 = DFATransitionFunction(
        initialState, firstState, LETTERS)
    firstStateTransitionFunction2 = DFATransitionFunction(
        firstState, firstState, LETTERS)

    # * Second state
    secondState = DFAState(2, True, AuxTokenTypes.MAIN_VALUE)
    secondStateFunction1 = DFATransitionFunction(
        firstState, secondState, [' '])
    secondStateFunction2 = DFATransitionFunction(
        secondState, secondState, [' '])

    # * Third State
    thirdState = DFAState(3)
    thirdStateTransitionFunction1 = DFATransitionFunction(
        firstState, thirdState, ['='])
    thirdStateTransitionFunction2 = DFATransitionFunction(
        secondState, thirdState, ['='])
    thirdStateTransitionFunction3 = DFATransitionFunction(
        thirdState, thirdState, [' '])

    # * Fourth State
    fourthState = DFAState(4, True, AuxTokenTypes.ATTRIBUTE)
    fourthStateTransitionFunction1 = DFATransitionFunction(
        thirdState, fourthState, LETTERS)
    fourthStateTransitionFunction2 = DFATransitionFunction(
        fourthState, fourthState, LETTERS)

    # # * Fifth State
    # fifthState = DFAState(5, True, AuxTokenTypes.ATTRIBUTE)
    # fifthStateTransitionFunction1 = DFATransitionFunction(
    #     fourthState, fifthState, [' '])
    # fifthStateTransitionFunction2 = DFATransitionFunction(
    #     fifthState, fifthState, [' '])

    # * ADD STATE
    states: List[DFAState] = [
        initialState,
        secondState,
        thirdState,
        fourthState,
    ]

    # * ADD FUNCTIONS
    functions: List[DFATransitionFunction] = [
        initialStateTransitionFunction1,
        firstStateTransitionFunction1,
        firstStateTransitionFunction2,
        secondStateFunction1,
        secondStateFunction2,
        thirdStateTransitionFunction1,
        thirdStateTransitionFunction2,
        thirdStateTransitionFunction3,
        fourthStateTransitionFunction1,
        fourthStateTransitionFunction2,
    ]

    return DFA2(initialState, states, functions)
