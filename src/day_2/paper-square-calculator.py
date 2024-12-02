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

    @property
    def square(self) -> int:
        return 2 * self.length * self.width + 2 * self.width * self.height + 2 * self.height * self.length


def load_prisms(file_path: Path) -> list[Prism]:
    with file_path.open("r") as file:
        return [Prism.load(line) for line in file]


def calculate_slack_size(prism: Prism) -> int:
    return min(prism.length * prism.width, prism.length * prism.height, prism.width * prism.height)


def calculate_paper_for_boxing(prism: Prism) -> int:
    return prism.square + calculate_slack_size(prism)


def main() -> None:
    prisms = load_prisms(Path("input.data"))
    # print(*prisms, sep="\n")

    paper_required = sum(calculate_paper_for_boxing(prism) for prism in prisms)
    print(f"Elves are required to order {paper_required} of wrapping paper")


if __name__ == "__main__":
    main()
