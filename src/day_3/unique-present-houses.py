from pathlib import Path


def load_route(file_path: Path) -> str:
    with file_path.open("r") as file:
        return file.read().strip()


def get_unique_locations(route: str) -> set[tuple[int, int]]:
    x, y = 0, 0
    locations = {(x, y)}

    for direction in route:
        match direction:
            case "^":  # north
                y += 1
            case "v":  # south
                y -= 1
            case ">":  # east
                x += 1
            case "<":  # west
                x -= 1
        locations.add((x, y))

    return locations


def main() -> None:
    route = load_route(Path("input.data"))

    locations = get_unique_locations(route)
    print(f"There are {len(locations)} houses receive at least one present")


if __name__ == "__main__":
    main()
