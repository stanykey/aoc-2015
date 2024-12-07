from json import load
from pathlib import Path
from typing import TypeAlias
from typing import cast

JsonPrimitive: TypeAlias = int | str | bool
JsonValue: TypeAlias = JsonPrimitive | list["JsonValue"] | dict[str, "JsonValue"]


def load_json(path: Path) -> JsonValue:
    with path.open("r", encoding="utf-8") as file:
        return cast(JsonValue, load(file))


def sum_all_numbers(document: JsonValue) -> int:
    match document:
        case int(value):
            return value
        case list(items):
            return sum(sum_all_numbers(item) for item in items)
        case dict(mapping):
            return sum(sum_all_numbers(value) for value in mapping.values())
        case _:
            return 0


def sum_all_numbers_without_red_property(document: JsonValue) -> int:
    match document:
        case int(value):
            return value
        case list(items):
            return sum(sum_all_numbers_without_red_property(item) for item in items)
        case dict(mapping):
            if "red" in mapping.values():
                return 0
            return sum(sum_all_numbers_without_red_property(value) for value in mapping.values())
        case _:
            return 0


def main() -> None:
    document = load_json(Path("input.data"))

    numbers_sum_1 = sum_all_numbers(document)
    print(f"The sum of all numbers in document is {numbers_sum_1}")

    numbers_sum_2 = sum_all_numbers_without_red_property(document)
    print(f"The sum of all numbers in document is {numbers_sum_2}")


if __name__ == "__main__":
    main()
