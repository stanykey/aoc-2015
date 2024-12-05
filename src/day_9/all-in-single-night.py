from collections import defaultdict
from math import inf
from pathlib import Path


def parse_record(record: str) -> tuple[str, str, int]:
    trip, _, distance = record.partition(" = ")
    departure, _, arrival = trip.partition(" to ")
    return departure, arrival, int(distance)


def load_distances(path: Path) -> list[tuple[str, str, int]]:
    with path.open("r") as file:
        return [parse_record(line.strip()) for line in file]


def create_distance_matrix(records: list[tuple[str, str, int]]) -> dict[str, dict[str, int]]:
    matrix: dict[str, dict[str, int]] = defaultdict(dict)
    for departure, arrival, distance in records:
        matrix[departure][arrival] = distance
        matrix[arrival][departure] = distance
    return matrix


def find_shortest_path(matrix: dict[str, dict[str, int]]) -> tuple[list[str], int]:
    locations = list(matrix.keys())
    location_count = len(locations)

    # Create distance matrix
    dist = [[inf] * location_count for _ in range(location_count)]
    for i, loc1 in enumerate(locations):
        for j, loc2 in enumerate(locations):
            if loc2 in matrix[loc1]:
                dist[i][j] = matrix[loc1][loc2]

    # DP table: dp[mask][i] -> Minimum distance to visit all nodes in `mask`, ending at `i`
    dp = [[inf] * location_count for _ in range(1 << location_count)]
    parent = [[-1] * location_count for _ in range(1 << location_count)]  # For reconstructing path

    # Base case: start at each node
    for i in range(location_count):
        dp[1 << i][i] = 0

    # Iterate over all subsets of nodes
    for mask in range(1 << location_count):
        for i in range(location_count):
            if not (mask & (1 << i)):  # If `i` is not in the current subset
                continue

            for j in range(location_count):
                if mask & (1 << j):  # If `j` is already visited
                    continue

                new_mask = mask | (1 << j)
                if dp[new_mask][j] > dp[mask][i] + dist[i][j]:
                    dp[new_mask][j] = dp[mask][i] + dist[i][j]
                    parent[new_mask][j] = i

    # Find the shortest path
    full_mask = (1 << location_count) - 1
    min_distance = inf
    end_node = -1
    for i in range(location_count):
        if dp[full_mask][i] < min_distance:
            min_distance = dp[full_mask][i]
            end_node = i

    # Reconstruct the path
    mask = full_mask
    path = []
    while end_node != -1:
        path.append(locations[end_node])
        prev_node = parent[mask][end_node]
        mask ^= 1 << end_node
        end_node = prev_node
    path.reverse()  # Reverse to get the correct order

    return path, int(min_distance)


def main() -> None:
    data = load_distances(Path("input.data"))
    # print(*data, sep="\n")

    distance_matrix = create_distance_matrix(data)
    route, distance = find_shortest_path(distance_matrix)
    print(*route, sep="->")
    print(f"The distance of the shortest route is {distance}")


if __name__ == "__main__":
    main()
