from pathlib import Path


def parse_input(path: Path) -> tuple[list[tuple[str, str]], str]:
    with path.open("r", encoding="utf-8") as file:
        lines = file.read().strip().splitlines()

    replacements = []
    for line in lines[:-2]:  # exclude the blank line and the target molecule
        if "=>" in line:
            source, _, target = line.partition(" => ")
            replacements.append((source, target))

    molecule = lines[-1]  # The target molecule is the last line
    return replacements, molecule


def generate_replacements(replacements: list[tuple[str, str]], molecule: str) -> set[str]:
    distinct_molecules = set()
    for source, target in replacements:
        start = 0
        while (index := molecule.find(source, start)) != -1:
            # replace the occurrence of `source` with `target`
            new_molecule = molecule[:index] + target + molecule[index + len(source) :]
            distinct_molecules.add(new_molecule)
            start = index + 1  # move to the next character to continue searching
    return distinct_molecules


def main() -> None:
    file_path = Path("input.data")
    replacements, molecule = parse_input(file_path)

    # Generate distinct molecules after one replacement
    distinct_molecules = generate_replacements(replacements, molecule)
    print(f"Number of distinct molecules: {len(distinct_molecules)}")


if __name__ == "__main__":
    main()
