from itertools import combinations
from math import prod
from pathlib import Path


def load_packages(path: Path) -> tuple[int, ...]:
    with path.open("r", encoding="utf-8") as file:
        return tuple(map(int, file))


def find_quantum_entanglement(bag: tuple[int, ...]) -> int:
    return prod(bag)


def distribute_packages(weights: tuple[int, ...], group_count: int) -> tuple[int, ...]:
    package_count = len(weights)
    total_weight = sum(weights)
    if total_weight % group_count != 0:
        raise ValueError("Packages cannot be evenly divided into groups.")

    target_weight_per_group = total_weight // group_count

    for num_packages in range(1, (package_count // group_count) + 1):
        distributions = [
            combo for combo in combinations(weights, num_packages) if sum(combo) == target_weight_per_group
        ]

        if distributions:  # we've found a solution
            return min(distributions, key=find_quantum_entanglement)

    return tuple()  # no valid combo found


def find_best_quantum_entanglement(packages: tuple[int, ...], *, group_count: int) -> int:
    best_bag = distribute_packages(packages, group_count)
    return find_quantum_entanglement(best_bag)


def main() -> None:
    path = Path("input.data")
    packages = load_packages(path)
    print(packages)

    best_quantum_entanglement = find_best_quantum_entanglement(packages, group_count=3)
    print(f"Best quantum entanglement: {best_quantum_entanglement}")

    best_quantum_entanglement = find_best_quantum_entanglement(packages, group_count=4)
    print(f"Best quantum entanglement: {best_quantum_entanglement}")


if __name__ == "__main__":
    main()
