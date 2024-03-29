from enum import Enum


class Response(Enum):
    """
    Enum modelling the possible responses provided by the Replay Buffer.
    """

    SUCCESSFUL = 1
    WRONG_SHAPE = 2
    ERROR = 3
