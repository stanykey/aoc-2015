def dictate_number(digits: str) -> str:
    parts = []
    counter = 1
    for i in range(1, len(digits)):
        if digits[i] == digits[i - 1]:
            counter += 1
        else:
            parts.append(f"{counter}{digits[i - 1]}")
            counter = 1
    parts.append(f"{counter}{digits[-1]}")

    return "".join(parts)


def dictate_number_with_repetition(digits: str, repeat: int) -> str:
    for _ in range(repeat):
        digits = dictate_number(digits)
    return digits


def main() -> None:
    numbers = ["1", "11", "21", "1211", "111221", "1113222113"]
    for number in numbers:
        dictated_number = dictate_number(number)
        print(f"The answer is {dictated_number}, which has a length of {len(dictated_number)} symbols.")

    number = dictate_number_with_repetition("1113222113", 40)
    print(f"The answer has a length of {len(str(number))} symbols.")

    number = dictate_number_with_repetition("1113222113", 50)
    print(f"The answer has a length of {len(str(number))} symbols.")


if __name__ == "__main__":
    main()
