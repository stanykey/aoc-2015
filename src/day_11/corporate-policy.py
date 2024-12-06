from itertools import groupby


def has_increasing_sequence(password: str, seq_size: int) -> bool:
    return any(
        all(ord(password[i + j]) == ord(password[i]) + j for j in range(seq_size))
        for i in range(len(password) - seq_size + 1)
    )


def has_non_overlapping_pairs(password: str, pairs_count: int) -> bool:
    pairs = [char for char, group in groupby(password) if len(list(group)) >= 2]
    return len(set(pairs)) >= pairs_count


def is_valid_password(password: str) -> bool:
    # Requirement 1: Passwords must include one increasing straight of at least three letters
    if not has_increasing_sequence(password, seq_size=3):
        return False

    # Requirement 2: Passwords may not contain the letters i, o, or l
    if any(c in password for c in "iol"):
        return False

    # Requirement 3: Passwords must contain at least two different, non-overlapping pairs of letters
    if not has_non_overlapping_pairs(password, 2):
        return False

    return True


def increment_password(password: str) -> str:
    """Increment the password like a base-26 number"""
    letters = list(password)
    i = len(letters) - 1
    while i >= 0:
        if letters[i] == "z":
            letters[i] = "a"
            i -= 1
        else:
            letters[i] = chr(ord(letters[i]) + 1)
            break
    return "".join(letters)


def update_password(password: str) -> str:
    while True:
        password = increment_password(password)
        if is_valid_password(password):
            return password


def main() -> None:
    password = "hepxcrrq"

    next_password = update_password(password)
    print(f"The next password:{next_password}")


if __name__ == "__main__":
    main()
