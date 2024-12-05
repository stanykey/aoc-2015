from pathlib import Path


def load_string_codes(file_path: Path) -> list[str]:
    with file_path.open("r") as file:
        return [line.strip() for line in file]


def calculate_string_delta(string: str) -> int:
    memory_representation = bytes(string[1:-1], "utf-8").decode("unicode_escape")
    return len(string) - len(memory_representation)


def main() -> None:
    string_codes = load_string_codes(Path("input.data"))
    # print(*string_codes, sep="\n")

    string_deltas = [calculate_string_delta(string) for string in string_codes]
    total_string_deltas = sum(string_deltas)
    print(f"The difference between code and memory is {total_string_deltas}")


if __name__ == "__main__":
    main()
