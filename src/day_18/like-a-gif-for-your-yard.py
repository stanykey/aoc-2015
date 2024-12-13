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
    rows, cols = len(grid), len(grid[0])
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


def enforce_corners_on(grid: list[list[bool]]) -> None:
    rows, cols = len(grid), len(grid[0])
    grid[0][0] = True
    grid[0][cols - 1] = True
    grid[rows - 1][0] = True
    grid[rows - 1][cols - 1] = True


def run_animation(grid: list[list[bool]], count: int) -> tuple[int, list[list[bool]]]:
    for _ in range(count):
        grid = animate(grid)
    return sum(sum(row) for row in grid), grid


def run_animation_with_corners(grid: list[list[bool]], steps: int) -> tuple[int, list[list[bool]]]:
    enforce_corners_on(grid)  # Enforce corners at the start
    for _ in range(steps):
        grid = animate(grid)
        enforce_corners_on(grid)  # Enforce corners after each step
    return sum(sum(row) for row in grid), grid


def main() -> None:
    file_path = Path("input.data")
    lights_configuration = load_lights_configuration(file_path)

    steps = 100
    total_lights_on, _ = run_animation(lights_configuration, steps)
    print(f"After {steps} steps, there are {total_lights_on} lights on.")

    total_lights_on, _ = run_animation_with_corners(lights_configuration, steps)
    print(f"After {steps} steps, there are {total_lights_on} lights on.")


if __name__ == "__main__":
    main()
