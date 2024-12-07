from json import load
from pathlib import Path
from typing import TypeAlias
from typing import cast

JsonPrimitive: TypeAlias = int | str | bool
JsonValue: TypeAlias = JsonPrimitive | list["JsonValue"] | dict[str, "JsonValue"]


def load_json(path: Path) -> JsonValue:
    with path.open("r") as file:
        return cast(JsonValue, load(file))


def sum_all_numbers(document: JsonValue) -> int:
    if isinstance(document, int):
        return document

    if isinstance(document, list):
        return sum(sum_all_numbers(item) for item in document)

    if isinstance(document, dict):
        return sum(sum_all_numbers(item) for item in document.values())

    return 0


def main() -> None:
    document = load_json(Path("input.data"))

    numbers_sum = sum_all_numbers(document)
    print(f"The sum of all numbers in document is {numbers_sum}")


if __name__ == "__main__":
    main()
