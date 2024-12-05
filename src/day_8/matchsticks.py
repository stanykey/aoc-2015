from pathlib import Path


def load_string_literals(file_path: Path) -> list[str]:
    with file_path.open("r") as file:
        return [line.strip() for line in file]


def calculate_string_memory_delta(literal: str) -> int:
    memory_representation = bytes(literal[1:-1], "utf-8").decode("unicode_escape")
    return len(literal) - len(memory_representation)


def encode_literal(literal: str) -> str:
    literal = literal.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{literal}"'


def calculate_string_encoding_deltas(string_literals: list[str], encoded_strings: list[str]) -> list[int]:
    return [len(encoded) - len(literal) for literal, encoded in zip(string_literals, encoded_strings, strict=True)]


def main() -> None:
    string_literals = load_string_literals(Path("input.data"))
    # print(*string_literals, sep="\n")

    string_memory_deltas = [calculate_string_memory_delta(literal) for literal in string_literals]
    total_string_deltas = sum(string_memory_deltas)
    print(f"The difference between code and memory is {total_string_deltas}")

    encoded_strings = [encode_literal(literal) for literal in string_literals]
    string_encoded_deltas = calculate_string_encoding_deltas(string_literals, encoded_strings)
    total_string_encoded_deltas = sum(string_encoded_deltas)
    print(f"The difference between code and encoded versions is {total_string_encoded_deltas}")


if __name__ == "__main__":
    main()
