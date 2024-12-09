from dataclasses import dataclass
from pathlib import Path
from typing import Self


@dataclass
class Reindeer:
    name: str
    speed: int
    flying_time: int
    resting_time: int

    @classmethod
    def from_str(cls, record: str) -> Self:
        """
        Parse a string into a Reindeer object
        the pattern of record string:
        "<name> can fly <speed> km/s for <flying time> seconds, but then must rest for <resting time> seconds."
        """
        parts = record.split(" ")

        return cls(name=parts[0], speed=int(parts[3]), flying_time=int(parts[6]), resting_time=int(parts[-2]))

    def calc_distance(self, duration: int) -> int:
        cycle_duration = self.flying_time + self.resting_time
        full_cycles, reminder = divmod(duration, cycle_duration)
        total_flying_time = full_cycles * self.flying_time + min(reminder, self.flying_time)
        return total_flying_time * self.speed


def load_reindeer_records(file_path: Path) -> list[Reindeer]:
    with file_path.open("r", encoding="utf-8") as file:
        return [Reindeer.from_str(record.strip()) for record in file]


def calculate_winner_distance(reindeers: list[Reindeer], duration: int) -> int:
    return max(reindeer.calc_distance(duration) for reindeer in reindeers)


def main() -> None:
    file_path = Path("input.data")
    reindeers = load_reindeer_records(file_path)
    print(*reindeers, sep="\n")

    race_duration = 2503
    winner_distance = calculate_winner_distance(reindeers, race_duration)
    print(f"A winner would travel for {winner_distance}km")


if __name__ == "__main__":
    main()
