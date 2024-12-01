from pathlib import Path


def read_instructions(file_path: Path) -> str:
    with file_path.open("r") as file:
        return file.read().strip()


def get_destination_floor(route: str) -> int:
    up = route.count("(")
    down = len(route) - up
    return up - down


def main() -> None:
    instructions = read_instructions(Path("input.data"))
    target_floor = get_destination_floor(instructions)
    print(f"Santa must go to {target_floor} floor")


if __name__ == "__main__":
    main()
