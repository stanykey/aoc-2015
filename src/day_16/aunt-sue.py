from dataclasses import dataclass
from pathlib import Path
from typing import List
from typing import Self


@dataclass(frozen=True)
class Sue:
    id: int
    children: int | None = None
    cats: int | None = None
    samoyeds: int | None = None
    pomeranians: int | None = None
    akitas: int | None = None
    vizslas: int | None = None
    goldfish: int | None = None
    trees: int | None = None
    cars: int | None = None
    perfumes: int | None = None

    @classmethod
    def from_str(cls, record: str) -> Self:
        """
        Parse a string into a Sue object.
        Example:
        "Sue 1: children: 1, cars: 8, vizslas: 7"
        """
        address, _, properties = record.partition(": ")
        name, _, sue_id = address.rpartition(" ")
        props = {key: int(value) for key, value in (prop.split(": ") for prop in properties.split(", "))}
        return cls(int(sue_id), **props)


def load_sue_records(file_path: Path) -> List[Sue]:
    with file_path.open("r", encoding="utf-8") as file:
        return [Sue.from_str(record.strip()) for record in file]


def matches(aim: Sue, sue: Sue) -> bool:
    """Check if a given Sue matches the aim Sue. Only compare known attributes."""
    for attr, aim_value in aim.__dict__.items():
        if attr == "id":
            continue
        sue_value = getattr(sue, attr)
        if sue_value is not None and sue_value != aim_value:
            return False
    return True


def find_matching_sue(aim: Sue, sues: List[Sue]) -> Sue | None:
    for sue in sues:
        if matches(aim, sue):
            return sue
    return None


def main() -> None:
    file_path = Path("input.data")
    sues = load_sue_records(file_path)
    print("Loaded Sue Records:")
    print(*sues, sep="\n")

    aim = Sue(
        id=0,
        children=3,
        cats=7,
        samoyeds=2,
        pomeranians=3,
        akitas=0,
        vizslas=0,
        goldfish=5,
        trees=3,
        cars=2,
        perfumes=1,
    )
    if sue := find_matching_sue(aim, sues):
        print(f"Sue #{sue.id} got your gift!")


if __name__ == "__main__":
    main()
