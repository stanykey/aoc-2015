from dataclasses import dataclass
from pathlib import Path
from typing import Self


@dataclass(frozen=True, kw_only=True)
class Prism:
    length: int
    width: int
    height: int

    @classmethod
    def load(cls, serialized: str) -> Self:
        length, width, height = map(int, serialized.split("x"))
        return cls(length=length, width=width, height=height)

    def slack_size(self) -> int:
        return min(self.length * self.width, self.length * self.height, self.width * self.height)


def load_prisms(file_path: Path) -> list[Prism]:
    with file_path.open("r") as file:
        return [Prism.load(line) for line in file]


def calculate_square(prism: Prism) -> int:
    square = 2 * prism.length * prism.width + 2 * prism.width * prism.height + 2 * prism.height * prism.length
    slack = prism.slack_size()
    return square + slack


def main() -> None:
    prisms = load_prisms(Path("input.data"))
    # print(*prisms, sep="\n")

    paper_required = sum(calculate_square(prism) for prism in prisms)
    print(f"Elves are required to order {paper_required} of wrapping paper")


if __name__ == "__main__":
    main()
