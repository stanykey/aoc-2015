from pathlib import Path


def read_input(path: Path) -> int:
    with path.open("r", encoding="utf-8") as file:
        return int(file.read().strip())


def sum_of_divisors_sieve(limit: int) -> list[int]:
    divisors = [0] * (limit + 1)
    for i in range(1, limit + 1):
        for j in range(i, limit + 1, i):
            divisors[j] += i
    return divisors


def find_lowest_house(target: int, delivery_count: int) -> int:
    max_houses = target // 10  # Rough estimate for the upper bound
    divisors = sum_of_divisors_sieve(max_houses)

    # presents delivered to each house
    for house, divisor_sum in enumerate(divisors):
        if delivery_count * divisor_sum >= target:
            return house

    raise ValueError("No house found with the given target.")


def main() -> None:
    file_path = Path("input.data")
    puzzle_input = read_input(file_path)

    result = find_lowest_house(puzzle_input, 10)
    print(f"The lowest house number to get at least {puzzle_input} presents is: {result}")


if __name__ == "__main__":
    main()
