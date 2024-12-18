from collections import defaultdict
from collections.abc import Callable
from dataclasses import dataclass
from enum import StrEnum
from enum import auto
from enum import unique
from pathlib import Path
from typing import Self

type Computer = dict[str, int]


def make_computer(a: int, b: int) -> Computer:
    computer = defaultdict(int)
    computer["a"] = a
    computer["b"] = b
    return computer


@unique
class OpCode(StrEnum):
    HLF = auto()
    TPL = auto()
    INC = auto()
    JMP = auto()
    JIE = auto()
    JIO = auto()


@dataclass(frozen=True)
class Operand:
    value: str


@dataclass(frozen=True)
class Instruction:
    opcode: OpCode
    operand1: Operand
    operand2: Operand

    @classmethod
    def from_str(cls, line: str) -> Self:
        parts = line.replace(",", "").split()
        opcode = OpCode(parts[0])
        operand1 = Operand(parts[1])
        operand2 = Operand(parts[2] if len(parts) > 2 else "")
        return cls(opcode, operand1, operand2)


@dataclass
class Program:
    instructions: list[Instruction]

    def __post_init__(self) -> None:
        self.__dispatch_table: dict[OpCode, Callable[[Instruction, Computer], int]] = {
            OpCode.HLF: self.__hlf,
            OpCode.TPL: self.__tpl,
            OpCode.INC: self.__inc,
            OpCode.JMP: self.__jmp,
            OpCode.JIE: self.__jie,
            OpCode.JIO: self.__jio,
        }

    def execute(self, computer: Computer) -> None:
        ip = 0
        while 0 <= ip < len(self.instructions):
            ip += self.__dispatch_table[self.instructions[ip].opcode](self.instructions[ip], computer)

    @staticmethod
    def __hlf(instruction: Instruction, computer: Computer) -> int:
        computer[instruction.operand1.value] //= 2
        return 1

    @staticmethod
    def __tpl(instruction: Instruction, computer: Computer) -> int:
        computer[instruction.operand1.value] *= 3
        return 1

    @staticmethod
    def __inc(instruction: Instruction, computer: Computer) -> int:
        computer[instruction.operand1.value] += 1
        return 1

    @staticmethod
    def __jmp(instruction: Instruction, computer: Computer) -> int:
        return int(instruction.operand1.value)

    @staticmethod
    def __jie(instruction: Instruction, computer: Computer) -> int:
        if computer[instruction.operand1.value] % 2 == 0:
            return int(instruction.operand2.value)
        return 1

    @staticmethod
    def __jio(instruction: Instruction, computer: Computer) -> int:
        if computer[instruction.operand1.value] == 1:
            return int(instruction.operand2.value)
        return 1


def load_assembly(path: Path) -> list[Instruction]:
    with path.open("r", encoding="utf-8") as file:
        return [Instruction.from_str(line.strip()) for line in file]


def main() -> None:
    path = Path("input.data")
    instructions = load_assembly(path)
    program = Program(instructions)

    computer = make_computer(0, 0)
    program.execute(computer)
    print(f"The value of registers: a = {computer['a']}, b = {computer['b']}")

    computer = make_computer(1, 0)
    program.execute(computer)
    print(f"The value of registers: a = {computer['a']}, b = {computer['b']}")


if __name__ == "__main__":
    main()
