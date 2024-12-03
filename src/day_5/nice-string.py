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


def is_ridiculous_nice_string(string: str) -> bool:
    def has_repeated_pair(s: str) -> bool:
        # Check for a pair of two letters appearing twice without overlapping
        for i in range(len(s) - 1):
            pair = s[i : i + 2]
            if pair in s[i + 2 :]:
                return True
        return False

    def has_repeat_with_one_between(s: str) -> bool:
        # Check for a letter repeating with exactly one letter between
        for i in range(len(s) - 2):
            if s[i] == s[i + 2]:
                return True
        return False

    # Check both conditions
    return has_repeated_pair(string) and has_repeat_with_one_between(string)


def main() -> None:
    strings = load_strings(Path("input.data"))

    nice_strings = sum(1 if is_nice_string(string) else 0 for string in strings)
    print(f"There are {nice_strings} nice strings")

    ridiculous_nice_strings = sum(1 if is_ridiculous_nice_string(string) else 0 for string in strings)
    print(f"There are {ridiculous_nice_strings} ridiculous nice strings")


if __name__ == "__main__":
    main()
