from pathlib import Path


def read_instructions(file_path: Path) -> str:
    with file_path.open("r") as file:
        return file.read().strip()


def get_destination_floor(route: str) -> int:
    up = route.count("(")
    down = len(route) - up
    return up - down


def find_instruction(instructions: str, *, floor: int) -> None | int:
    current_floor = 0
    for index, value in enumerate(instructions):
        current_floor += 1 if value == "(" else -1
        if current_floor == floor:
            return index + 1
    return None


def main() -> None:
    instructions = read_instructions(Path("input.data"))

    target_floor = get_destination_floor(instructions)
    print(f"Santa must go to {target_floor} floor")

    target_floor = -1
    position = find_instruction(instructions, floor=target_floor)
    print(f"An instruction leading to the {target_floor} floor is at {position} position")


if __name__ == "__main__":
    main()
