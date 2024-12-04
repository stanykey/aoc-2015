from pathlib import Path


def load_circuit(file_path: Path) -> dict[str, str]:
    circuit = {}

    with file_path.open("r") as file:
        for instruction in file:
            expression, _, target = instruction.strip().partition(" -> ")
            circuit[target] = expression

    return circuit


def evaluate(wire: str, circuit: dict[str, str], cache: dict[str, int]) -> int:
    """Evaluates the signal on a given wire."""
    if wire.isdigit():
        # Direct value
        return int(wire)

    if wire in cache:
        # Return cached value if available
        return cache[wire]

    expression = circuit[wire]
    match expression.split():
        case [a, "AND", b]:
            result = evaluate(a, circuit, cache) & evaluate(b, circuit, cache)
        case [a, "OR", b]:
            result = evaluate(a, circuit, cache) | evaluate(b, circuit, cache)
        case [a, "LSHIFT", n]:
            result = evaluate(a, circuit, cache) << int(n)
        case [a, "RSHIFT", n]:
            result = evaluate(a, circuit, cache) >> int(n)
        case ["NOT", a]:
            result = ~evaluate(a, circuit, cache) & 0xFFFF  # Ensure 16-bit result
        case [a]:
            # Single wire or direct value
            result = evaluate(a, circuit, cache)
        case _:
            raise ValueError(f"Unknown instruction: {expression}")

    cache[wire] = result
    return result


def main() -> None:
    circuit = load_circuit(Path("input.data"))

    requested_wire = "a"
    result = evaluate(requested_wire, circuit, {}) if requested_wire in circuit else 0
    print(f"The signal to wire {requested_wire} is: {result}")

    circuit["b"] = str(result)
    result = evaluate(requested_wire, circuit, {}) if requested_wire in circuit else 0
    print(f"The signal to wire {requested_wire} is: {result}")


if __name__ == "__main__":
    main()
