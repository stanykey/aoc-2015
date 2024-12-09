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


@dataclass
class ReindeerState:
    """Represents the state of a reindeer during the race."""

    name: str
    distance: int = 0
    time_in_state: int = 0
    is_flying: bool = True
    score: int = 0


def load_reindeer_records(file_path: Path) -> list[Reindeer]:
    with file_path.open("r", encoding="utf-8") as file:
        return [Reindeer.from_str(record.strip()) for record in file]


def calculate_winner_by_distance(reindeers: list[Reindeer], duration: int) -> int:
    return max(reindeer.calc_distance(duration) for reindeer in reindeers)


def calculate_winner_by_scoring_system(reindeers: list[Reindeer], duration: int) -> int:
    states = {reindeer.name: ReindeerState(name=reindeer.name) for reindeer in reindeers}

    for _ in range(1, duration + 1):
        for reindeer in reindeers:
            state = states[reindeer.name]

            state.time_in_state += 1
            if state.is_flying:
                state.distance += reindeer.speed

                if state.time_in_state == reindeer.flying_time:
                    state.is_flying = False
                    state.time_in_state = 0
            else:
                if state.time_in_state == reindeer.resting_time:
                    state.is_flying = True
                    state.time_in_state = 0

        max_distance = max(state.distance for state in states.values())
        for state in states.values():
            if state.distance == max_distance:
                state.score += 1

    return max(state.score for state in states.values())


def main() -> None:
    file_path = Path("input.data")
    reindeers = load_reindeer_records(file_path)
    print(*reindeers, sep="\n")

    race_duration = 2503

    winner_by_distance = calculate_winner_by_distance(reindeers, race_duration)
    print(f"A winner by distance would be traveled for {winner_by_distance} km")

    winner_by_scoring_system = calculate_winner_by_scoring_system(reindeers, race_duration)
    print(f"A winner by scoring system would be win with {winner_by_scoring_system} points")


if __name__ == "__main__":
    main()
