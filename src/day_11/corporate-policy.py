INCREASING_SEQUENCES = set("".join(chr(ord("a") + i + j) for j in range(3)) for i in range(24))
FORBIDDEN_CHARS = set("iol")


def has_increasing_sequence(password: str, seq_size: int) -> bool:
    """Check if the password contains an increasing straight of letters of a given size."""
    for i in range(len(password) - seq_size + 1):
        if password[i : i + seq_size] in INCREASING_SEQUENCES:
            return True
    return False


def has_non_overlapping_pairs(password: str, pairs_count: int) -> bool:
    """Check if the password contains at least a given number of non-overlapping pairs."""
    seen = set()
    count = 0
    i = 0
    while i < len(password) - 1:
        if password[i] == password[i + 1]:
            if password[i] not in seen:
                seen.add(password[i])
                count += 1
            i += 1  # Skip the next character to ensure non-overlapping
        i += 1
    return count >= pairs_count


def is_valid_password(password: str) -> bool:
    """Validate password."""

    # Forbidden characters
    if any(c in password for c in FORBIDDEN_CHARS):
        return False

    # Increasing straight of at least three letters
    if not has_increasing_sequence(password, seq_size=3):
        return False

    # At least two non-overlapping pairs of letters
    if not has_non_overlapping_pairs(password, 2):
        return False

    return True


def increment_password(password: str) -> str:
    """Increment password like a base-26 number and skip invalid characters early."""
    letters = list(password)
    i = len(letters) - 1
    while i >= 0:
        if letters[i] == "z":
            letters[i] = "a"
            i -= 1
        else:
            letters[i] = chr(ord(letters[i]) + 1)
            if letters[i] in FORBIDDEN_CHARS:
                letters[i] = chr(ord(letters[i]) + 1)

            # Reset trailing characters to 'a' after increment
            for j in range(i + 1, len(letters)):
                letters[j] = "a"
            break
    return "".join(letters)


def update_password(password: str) -> str:
    """Find the next valid password."""
    while True:
        password = increment_password(password)
        if is_valid_password(password):
            return password


def main() -> None:
    password = "hepxcrrq"

    next_password = update_password(password)
    print(f"The next password: {next_password}")

    next_password = update_password(next_password)
    print(f"The next password: {next_password}")


if __name__ == "__main__":
    main()
