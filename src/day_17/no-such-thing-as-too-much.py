from collections.abc import Generator
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

    def find_fitting_combinations(
        self, containers: list[Container], party_size: int | None = None
    ) -> list[tuple[Container, ...]]:
        if party_size is None:
            return list(self._generate_combinations(containers))

        if party_size < 1:
            return []

        return list(self._generate_combinations_of_size(containers, party_size))

    def _generate_combinations_of_size(
        self, containers: list[Container], size: int
    ) -> Generator[tuple[Container, ...], None, None]:
        for combination in combinations(containers, size):
            if sum(container.size for container in combination) == self.capacity:
                yield combination

    def _generate_combinations(self, containers: list[Container]) -> Generator[tuple[Container, ...], None, None]:
        for size in range(1, len(containers) + 1):
            yield from self._generate_combinations_of_size(containers, size)


def find_smallest_combinations(combinations: list[tuple[Container, ...]]) -> list[tuple[Container, ...]]:
    if not combinations:
        return []

    # minimize the party size and return the corresponding combinations
    min_party_size = min(len(combination) for combination in combinations)
    return [combination for combination in combinations if len(combination) == min_party_size]


def load_containers(path: Path) -> list[Container]:
    with path.open("r", encoding="utf-8") as file:
        return list(map(Container.from_str, file.read().splitlines()))


def main() -> None:
    file_path = Path("input.data")
    containers = load_containers(file_path)
    print(*containers, sep="\n")

    refrigerator = Refrigerator(capacity=150)
    fitting_combinations = refrigerator.find_fitting_combinations(containers)
    print(
        f"There are {len(fitting_combinations)} possible party configurations to "
        f"fill the refrigerator size of {refrigerator.capacity}"
    )

    smallest_combinations = find_smallest_combinations(fitting_combinations)
    print(
        f"The smallest party size is {len(smallest_combinations[0])}, "
        f"and there are {len(smallest_combinations)} such possible configurations"
    )


if __name__ == "__main__":
    main()
