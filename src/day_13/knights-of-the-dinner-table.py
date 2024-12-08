from itertools import permutations
from pathlib import Path


def parse_input(file_path: Path) -> dict[tuple[str, str], int]:
    """
    Parse the input file to extract happiness changes between attendees.
    Returns a dictionary where keys are (person1, person2) tuples and values are happiness changes.
    """
    happiness_changes = {}
    with file_path.open("r", encoding="utf-8") as file:
        for line in file:
            parts = line.strip().split()
            person1 = parts[0]
            person2 = parts[-1].rstrip(".")
            happiness = int(parts[3]) if parts[2] == "gain" else -int(parts[3])
            happiness_changes[(person1, person2)] = happiness
    return happiness_changes


def calculate_happiness(arrangement: tuple[str, ...], happiness_changes: dict[tuple[str, str], int]) -> int:
    """
    Calculate the total happiness for a given seating arrangement.
    """
    total_happiness = 0
    num_people = len(arrangement)
    for i in range(num_people):
        person1 = arrangement[i]
        person2 = arrangement[(i + 1) % num_people]  # Circular seating
        total_happiness += happiness_changes.get((person1, person2), 0)
        total_happiness += happiness_changes.get((person2, person1), 0)
    return total_happiness


def find_optimal_arrangement(happiness_changes: dict[tuple[str, str], int]) -> int:
    """
    Find the optimal seating arrangement for maximum happiness.
    """
    attendees = set(person for pair in happiness_changes.keys() for person in pair)
    max_happiness = -1_000_000_000
    for arrangement in permutations(attendees):
        happiness = calculate_happiness(arrangement, happiness_changes)
        max_happiness = max(max_happiness, happiness)
    return max_happiness


def find_optimal_arrangement_with_me(happiness_changes: dict[tuple[str, str], int]) -> int:
    """
    Find the optimal seating arrangement for maximum happiness with me.
    """
    happiness_changes = happiness_changes.copy()
    attendees = set(person for pair in happiness_changes.keys() for person in pair)
    for attendee in attendees:
        happiness_changes[("me", attendee)] = 0
        happiness_changes[(attendee, "me")] = 0
    attendees.add("me")

    max_happiness = -1_000_000_000
    for arrangement in permutations(attendees):
        happiness = calculate_happiness(arrangement, happiness_changes)
        max_happiness = max(max_happiness, happiness)
    return max_happiness


def main() -> None:
    file_path = Path("input.data")
    happiness_changes = parse_input(file_path)

    optimal_happiness = find_optimal_arrangement(happiness_changes)
    print(f"The total change in happiness for the optimal seating arrangement is {optimal_happiness}")

    optimal_happiness = find_optimal_arrangement_with_me(happiness_changes)
    print(f"The total change in happiness for the optimal seating arrangement is {optimal_happiness}")


if __name__ == "__main__":
    main()
