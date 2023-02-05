from enum import Enum, auto
from dataclasses import dataclass

class AddressMode(Enum):
    IMMEDIATE = auto()
    DIRECT = auto()
    INDIRECT = auto()

@dataclass
class Address:
    mode: AddressMode
    value: int

    def __eq__(self, other):
        return self.mode == other.mode and self.value == other.value

class InstructionType(Enum):
    INC = auto()
    DEC = auto()
    STOP = auto()
    PRINT = auto()
    JZERO = auto()
    JNZERO = auto()

@dataclass
class Instruction:
    type: InstructionType
    args: list

    def __eq__(self, other):
        return self.type == other.type and self.args == other.args
