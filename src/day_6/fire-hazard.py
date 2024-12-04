from collections import defaultdict
from dataclasses import dataclass
from enum import StrEnum
from enum import unique
from pathlib import Path
from typing import Self

GRID_WIDTH = 1000
GRID_HEIGHT = 1000

type LightMap = dict[tuple[int, int], int]


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


def install_simple_lighting(instructions: list[Instruction]) -> LightMap:
    lights: LightMap = defaultdict(int)

    for instruction in instructions:
        for y in range(instruction.y1, instruction.y2 + 1):
            for x in range(instruction.x1, instruction.x2 + 1):
                coord = (x, y)
                match instruction.action:
                    case Action.TURN_ON:
                        lights[coord] = 1
                    case Action.TURN_OFF:
                        lights[coord] = 0
                    case Action.TOGGLE:
                        lights[coord] = 0 if lights[coord] else 1
    return lights


def install_lighting_with_brightness(instructions: list[Instruction]) -> LightMap:
    lights: LightMap = defaultdict(int)

    for instruction in instructions:
        for y in range(instruction.y1, instruction.y2 + 1):
            for x in range(instruction.x1, instruction.x2 + 1):
                coord = (x, y)
                match instruction.action:
                    case Action.TURN_ON:
                        lights[coord] += 1
                    case Action.TURN_OFF:
                        lights[coord] = max(0, lights[coord] - 1)
                    case Action.TOGGLE:
                        lights[coord] += 2

    return lights


def get_total_brightness(lights: LightMap) -> int:
    return sum(lights.values())


def main() -> None:
    instructions = load_instructions(Path("input.data"))
    print(*instructions, sep="\n")

    lights = install_simple_lighting(instructions)
    total_brightness = get_total_brightness(lights)
    print(f"There are {total_brightness} active lights")

    lights = install_lighting_with_brightness(instructions)
    total_brightness = get_total_brightness(lights)
    print(f"The total brightness is {total_brightness}")


if __name__ == "__main__":
    main()
