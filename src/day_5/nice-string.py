from pathlib import Path


def load_strings(file_path: Path) -> list[str]:
    with file_path.open("r") as file:
        return file.readlines()


def is_nice_string(string: str) -> bool:
    # Check for at least three vowels
    vowels = "aeiou"
    vowel_count = sum(1 for char in string if char in vowels)
    if vowel_count < 3:
        return False

    # Check for at least one letter appearing twice in a row
    has_double = any(string[i] == string[i + 1] for i in range(len(string) - 1))
    if not has_double:
        return False

    # Check that it does not contain forbidden strings
    forbidden = {"ab", "cd", "pq", "xy"}
    if any(bad in string for bad in forbidden):
        return False

    # If all checks pass, the string is nice
    return True


def main() -> None:
    strings = load_strings(Path("input.data"))

    nice_strings = sum(1 if is_nice_string(string) else 0 for string in strings)
    print(f"There are {nice_strings} nice strings")


if __name__ == "__main__":
    main()
