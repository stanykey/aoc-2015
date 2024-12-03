from hashlib import md5


def mine_coins(secret_key: str, zeroes: int = 5) -> int:
    prefix = "0" * zeroes  # Create a string of the required number of leading zeroes
    number = 0

    while True:
        to_hash = f"{secret_key}{number}"
        hash_result = md5(to_hash.encode()).hexdigest()
        if hash_result.startswith(prefix):
            return number
        number += 1


def main() -> None:
    secret_key = "yzbqklnj"
    answer = mine_coins(secret_key)
    print(f"Answer: {answer}")


if __name__ == "__main__":
    main()
