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


def find_fewest_steps(replacements: list[tuple[str, str]], molecule: str) -> int:
    reverse_replacements = [(target, source) for source, target in replacements]
    reverse_replacements.sort(key=lambda x: -len(x[0]))  # sort by target length descending for greedy match

    steps = 0
    while molecule != "e":
        for target, source in reverse_replacements:
            if target in molecule:
                # replace the first occurrence of `target` with `source`
                molecule = molecule.replace(target, source, 1)
                steps += 1
                break
        else:
            # if no replacement can be applied, it's an error
            raise ValueError("Unable to reduce molecule to 'e'")
    return steps


def main() -> None:
    file_path = Path("input.data")
    replacements, molecule = parse_input(file_path)

    # generate distinct molecules after one replacement
    distinct_molecules = generate_replacements(replacements, molecule)
    print(f"Number of distinct molecules: {len(distinct_molecules)}")

    # find the fewest steps to reduce the molecule to `e`
    fewest_steps = find_fewest_steps(replacements, molecule)
    print(f"The fewest number of steps to fabricate the medicine is: {fewest_steps}")


if __name__ == "__main__":
    main()
