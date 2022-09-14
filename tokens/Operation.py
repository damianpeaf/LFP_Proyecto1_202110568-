

from enum import Enum, auto


class OperationType(Enum):
    # ? More precedence means it will be evaluated first
    INVERSO = auto()
    POTENCIA = auto()
    RAIZ = auto()
    MULTIPLICACION = auto()
    DIVISION = auto()
    SENO = auto()
    COSENO = auto()
    TANGENTE = auto()
    MOD = auto()
    SUMA = auto()
    RESTA = auto()
    ESCRIBIR = auto()


class Operation():

    def __init__(self, operationType: OperationType):
        self.operationType = operationType
