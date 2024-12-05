from collections import defaultdict
from collections.abc import Callable
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


class TravelingSalesperson:
    def __init__(self, matrix: dict[str, dict[str, int]]):
        self.locations = list(matrix.keys())
        self.location_count = len(self.locations)
        self.dist = self._create_distance_matrix(matrix)

    def solve(self, comparison: Callable[[int, int], bool], initial_value: int) -> tuple[list[str], int]:
        dp = [[initial_value] * self.location_count for _ in range(1 << self.location_count)]
        parent = [[-1] * self.location_count for _ in range(1 << self.location_count)]

        # Base case: start at each node
        for i in range(self.location_count):
            dp[1 << i][i] = 0

        # Iterate over all subsets of nodes
        for mask in range(1 << self.location_count):
            for i in range(self.location_count):
                if not (mask & (1 << i)):  # If `i` is not in the current subset
                    continue

                for j in range(self.location_count):
                    if mask & (1 << j):  # If `j` is already visited
                        continue

                    new_mask = mask | (1 << j)
                    new_distance = dp[mask][i] + self.dist[i][j]
                    if comparison(new_distance, dp[new_mask][j]):
                        dp[new_mask][j] = new_distance
                        parent[new_mask][j] = i

        # Find the optimal path
        full_mask = (1 << self.location_count) - 1
        optimal_value = initial_value
        end_node = -1
        for i in range(self.location_count):
            if comparison(dp[full_mask][i], optimal_value):
                optimal_value = dp[full_mask][i]
                end_node = i

        # Reconstruct the path
        mask = full_mask
        path = []
        while end_node != -1:
            path.append(self.locations[end_node])
            prev_node = parent[mask][end_node]
            mask ^= 1 << end_node
            end_node = prev_node
        path.reverse()

        return path, optimal_value

    def _create_distance_matrix(self, matrix: dict[str, dict[str, int]]) -> list[list[int]]:
        dist = [
            [10**9] * self.location_count
            for _ in range(self.location_count)  # Use a large integer as "infinity"
        ]
        for i, departure in enumerate(self.locations):
            for j, arrival in enumerate(self.locations):
                if arrival in matrix[departure]:
                    dist[i][j] = matrix[departure][arrival]
        return dist


def find_shortest_path(matrix: dict[str, dict[str, int]]) -> tuple[list[str], int]:
    tsp = TravelingSalesperson(matrix)
    return tsp.solve(lambda x, y: x < y, 10**9)


def find_longest_path(matrix: dict[str, dict[str, int]]) -> tuple[list[str], int]:
    tsp = TravelingSalesperson(matrix)
    return tsp.solve(lambda x, y: x > y, -(10**9))


def main() -> None:
    data = load_distances(Path("input.data"))
    distance_matrix = create_distance_matrix(data)
    # print(*data, sep="\n")

    route, distance = find_shortest_path(distance_matrix)
    print(f"Shortest route: {'->'.join(route)}")
    print(f"The distance of the shortest route is {distance}")

    route, distance = find_longest_path(distance_matrix)
    print(f"Longest route: {'->'.join(route)}")
    print(f"The distance of the longest route is {distance}")


if __name__ == "__main__":
    main()
