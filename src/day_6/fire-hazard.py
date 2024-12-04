from dataclasses import dataclass
from enum import StrEnum
from enum import unique
from pathlib import Path
from typing import Self

GRID_WIDTH = 1000
GRID_HEIGHT = 1000


@unique
class Action(StrEnum):
    TURN_ON = "turn on"
    TURN_OFF = "turn off"
    TOGGLE = "toggle"


@dataclass(frozen=True, slots=True)
class Instruction:
    x1: int
    y1: int
    x2: int
    y2: int
    action: Action

    @classmethod
    def from_str(cls, s: str) -> Self:
        # Match the action
        if s.startswith("turn on"):
            action = Action.TURN_ON
            s = s[len("turn on ") :]
        elif s.startswith("turn off"):
            action = Action.TURN_OFF
            s = s[len("turn off ") :]
        else:
            action = Action.TOGGLE
            s = s[len("toggle ") :]

        # Extract coordinates
        start, _, end = s.partition(" through ")
        x1, y1 = map(int, start.split(","))
        x2, y2 = map(int, end.split(","))

        return cls(x1=x1, y1=y1, x2=x2, y2=y2, action=action)


def load_instructions(file_path: Path) -> list[Instruction]:
    with file_path.open("r") as file:
        return [Instruction.from_str(record) for record in file]


def install_lighting(instructions: list[Instruction]) -> list[list[bool]]:
    lights = [[False for x in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
    for instruction in instructions:
        for y in range(instruction.y1, instruction.y2 + 1):
            for x in range(instruction.x1, instruction.x2 + 1):
                match instruction.action:
                    case Action.TURN_ON:
                        lights[y][x] = True
                    case Action.TURN_OFF:
                        lights[y][x] = False
                    case Action.TOGGLE:
                        lights[y][x] = not lights[y][x]
    return lights


def count_light_lit(lights: list[list[bool]]) -> int:
    return sum(cell for line in lights for cell in line)


def main() -> None:
    instructions = load_instructions(Path("input.data"))
    print(*instructions, sep="\n")

    lights = install_lighting(instructions)
    active_lights = count_light_lit(lights)
    print(f"There are {active_lights} active lights")


if __name__ == "__main__":
    main()
