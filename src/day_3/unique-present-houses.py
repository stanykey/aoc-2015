from itertools import cycle
from pathlib import Path


def load_route(file_path: Path) -> str:
    with file_path.open("r") as file:
        return file.read().strip()


def get_unique_houses(route: str, santa_count: int = 1) -> set[tuple[int, int]]:
    houses = {(0, 0)}

    tracker = [{"x": 0, "y": 0} for _ in range(santa_count)]
    santa_cycle = cycle(range(santa_count))

    for direction in route:
        current_santa = tracker[next(santa_cycle)]
        match direction:
            case "^":  # north
                current_santa["y"] += 1
            case "v":  # south
                current_santa["y"] -= 1
            case ">":  # east
                current_santa["x"] += 1
            case "<":  # west
                current_santa["x"] -= 1
        houses.add((current_santa["x"], current_santa["y"]))

    return houses


def main() -> None:
    route = load_route(Path("input.data"))

    for santa_count in range(1, 3):
        houses = get_unique_houses(route, santa_count)
        print(f"There are {len(houses)} houses receive at least one present with {santa_count} of Santa")


if __name__ == "__main__":
    main()
