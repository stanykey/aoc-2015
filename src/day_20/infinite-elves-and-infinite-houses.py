from pathlib import Path


def read_input(path: Path) -> int:
    with path.open("r", encoding="utf-8") as file:
        return int(file.read().strip())


def find_lowest_house(target: int, delivery_count: int, max_visits: int | None = None) -> int:
    max_houses = target // delivery_count  # rough estimate for the upper bound

    divisors = [0] * (max_houses + 1)
    for elf in range(1, max_houses + 1):
        count = 0
        for house in range(elf, max_houses + 1, elf):
            divisors[house] += elf
            count += 1
            # apply the max_visits limit if provided
            if max_visits is not None and count >= max_visits:
                break

    # find the first house that meets or exceeds the target presents
    for house, divisor_sum in enumerate(divisors):
        if delivery_count * divisor_sum >= target:
            return house

    raise ValueError("No house found with the given target.")


def main() -> None:
    file_path = Path("input.data")
    puzzle_input = read_input(file_path)

    result = find_lowest_house(puzzle_input, 10)
    print(f"The lowest house number to get at least {puzzle_input} presents is: {result}")

    result = find_lowest_house(puzzle_input, delivery_count=11, max_visits=50)
    print(f"The lowest house number to get at least {puzzle_input} presents is: {result}")


if __name__ == "__main__":
    main()
