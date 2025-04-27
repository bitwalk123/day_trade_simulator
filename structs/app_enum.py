from enum import Enum, auto


class SimulationMode(Enum):
    NORMAL = auto()
    EXPLORE = auto()


class LoopStatus(Enum):
    NEXT_CONDITION = auto()
    NEXT_CODE = auto()
    NEXT_FILE = auto()
    COMPLETE = auto()
