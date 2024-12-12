from dataclasses import dataclass
from itertools import combinations
from pathlib import Path
from typing import Self


@dataclass(frozen=True)
class Container:
    size: int

    @classmethod
    def from_str(cls, number: str) -> Self:
        return cls(int(number))


@dataclass(frozen=True)
class Refrigerator:
    capacity: int

    def find_fitting_combinations(self, containers: list[Container]) -> list[tuple[Container, ...]]:
        return [
            combination
            for size in range(1, len(containers) + 1)
            for combination in combinations(containers, size)
            if sum(container.size for container in combination) == self.capacity
        ]


def load_containers(path: Path) -> list[Container]:
    with path.open("r", encoding="utf-8") as file:
        return list(map(Container.from_str, file.read().splitlines()))


def main() -> None:
    file_path = Path("input.data")
    containers = load_containers(file_path)

    refrigerator = Refrigerator(capacity=150)
    fitting_combinations = refrigerator.find_fitting_combinations(containers)
    print(
        f"There are {len(fitting_combinations)} possible party configurations to "
        f"fill the refrigerator size of {refrigerator.capacity}"
    )


if __name__ == "__main__":
    main()
