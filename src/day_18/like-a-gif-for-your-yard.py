from pathlib import Path


def is_light_on(marker: str) -> bool:
    return marker == "#"


def load_lights_configuration(path: Path) -> list[list[bool]]:
    with path.open("r", encoding="utf-8") as file:
        return [[is_light_on(marker) for marker in line.strip()] for line in file]


def count_neighbors_on(grid: list[list[bool]], row: int, col: int) -> int:
    count = 0
    for dr, dc in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
        nr, nc = row + dr, col + dc
        if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]) and grid[nr][nc]:
            count += 1
    return count


def animate(grid: list[list[bool]]) -> list[list[bool]]:
    rows = len(grid)
    cols = len(grid[0])
    next_grid = [[False] * cols for _ in range(rows)]
    for row in range(rows):
        for col in range(cols):
            neighbors_on = count_neighbors_on(grid, row, col)
            if grid[row][col]:
                # A light stays on if it has 2 or 3 neighbors on
                next_grid[row][col] = neighbors_on in {2, 3}
            else:
                # A light turns on if exactly 3 neighbors are on
                next_grid[row][col] = neighbors_on == 3
    return next_grid


def run_animation(grid: list[list[bool]], count: int) -> tuple[int, list[list[bool]]]:
    for _ in range(count):
        grid = animate(grid)

    total_lights_on = sum(sum(row) for row in grid)
    return total_lights_on, grid


def main() -> None:
    file_path = Path("input.data")
    lights_configuration = load_lights_configuration(file_path)

    steps = 100
    total_lights_on, lights_configuration = run_animation(lights_configuration, steps)
    print(f"After {steps} steps, there are {total_lights_on} lights on.")


if __name__ == "__main__":
    main()
