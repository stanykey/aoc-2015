def find_code(row: int, col: int) -> int:
    """read more at https://en.wikipedia.org/wiki/Cantor's_diagonal_argument"""

    # starting values
    initial_code = 20151125
    multiplier = 252533
    divisor = 33554393

    # calculate the diagonal index for the given (row, col)
    # diagonal filling formula: sum of numbers up to (row + col - 2) + col
    diagonal_number = row + col - 1
    index = (diagonal_number * (diagonal_number - 1)) // 2 + col

    # generate codes up to the target index
    code = initial_code
    for _ in range(1, index):  # start from 1 since the first code is already known
        code = (code * multiplier) % divisor

    return code


def main() -> None:
    for cell in [(6, 6), (2981, 3075)]:
        print(f"code for {cell} is {find_code(*cell)}")


if __name__ == "__main__":
    main()
