from typing import List
from DFA.DFA import DFA
from DFA.DFAState import DFAState
from DFA.DFATransitionFunction import DFATransitionFunction
from lexer.constants.digit import DIGITS
from lexer.constants.digitContent import DIGITS_CONTENT
from lexer.constants.digitDFA import digitDFAProps
from tokens.Token import TokenType


def languageDFA():

    # * Initial State
    initialState = DFAState(0)

    # * Content
    firstState = DFAState(1, True, TokenType.CONTENT)
    firstStateFunction1 = DFATransitionFunction(
        initialState, firstState, DIGITS_CONTENT,)
    firstStateFunction2 = DFATransitionFunction(
        firstState, firstState, DIGITS_CONTENT)

    # * TAGS

    # Open Symbol
    secondState = DFAState(2)
    secondStateFuntion = DFATransitionFunction(
        initialState, secondState, ['<'])

    # * Closing Tags

    # /
    thirdState = DFAState(3)
    thirdStateFuntion = DFATransitionFunction(
        secondState, thirdState, ['/'])

    # content of the closing tag

    fourthStateProps = digitDFAProps(4, False)
    fourthState = fourthStateProps['state']

    fourthStateFunction1 = DFATransitionFunction(
        thirdState, fourthState, DIGITS)
    fourthStateFunction2 = fourthStateProps['function']

    # End symbol

    fifthState = DFAState(5, True, TokenType.CLOSING_TAG)
    fifthStateFunction = DFATransitionFunction(fourthState, fifthState, ['>'])

    # * AUTOCLOSING and OPEN TAG

    sixthStateProps = digitDFAProps(6)
    sixthState = sixthStateProps['state']

    sixthStateFunction1 = DFATransitionFunction(
        secondState, sixthState, DIGITS)
    sixthStateFunction2 = sixthStateProps['function']

    # / for autoclosing tag
    seventhState = DFAState(7)
    seventhStateFunction = DFATransitionFunction(
        sixthState, seventhState, ['/'])

    # > for autoclosing tag
    eighthState = DFAState(8, True, TokenType.AUTOCLOSING_TAG)
    eighthStateFunction = DFATransitionFunction(
        seventhState, eighthState, ['>'])

    # > for closisng tag

    ninethState = DFAState(9, True, TokenType.OPEN_TAG)
    ninethStateFunction = DFATransitionFunction(sixthState, ninethState, ['>'])

    # * ADD STATES

    states: List[DFAState] = [
        initialState,
        firstState,
        secondState,
        thirdState,
        fourthState,
        fifthState,
        sixthState,
        seventhState,
        eighthState,
        ninethState
    ]

    # * ADD FUNCTIONS
    functions: List[DFATransitionFunction] = [
        firstStateFunction1,
        firstStateFunction2,
        secondStateFuntion,
        thirdStateFuntion,
        fourthStateFunction1,
        fourthStateFunction2,
        fifthStateFunction,
        sixthStateFunction1,
        sixthStateFunction2,
        seventhStateFunction,
        eighthStateFunction,
        ninethStateFunction
    ]

    return DFA(initialState, states, functions)
