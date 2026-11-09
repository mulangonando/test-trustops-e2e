from collections import deque

# State is a flat tuple of 9 values; 0 represents the blank tile.
# Goal state:
#   1 2 3
#   4 5 6
#   7 8 _
GOAL = (1, 2, 3, 4, 5, 6, 7, 8, 0)

# Valid swaps for each blank position in the 3×3 grid
#   0 1 2
#   3 4 5
#   6 7 8
NEIGHBORS = {
    0: [1, 3],
    1: [0, 2, 4],
    2: [1, 5],
    3: [0, 4, 6],
    4: [1, 3, 5, 7],
    5: [2, 4, 8],
    6: [3, 7],
    7: [4, 6, 8],
    8: [5, 7],
}


def is_solvable(state: tuple) -> bool:
    """
    A puzzle is solvable iff the number of inversions is even.
    An inversion is a pair (i, j) where i < j but state[i] > state[j],
    ignoring the blank tile (0).
    """
    tiles = [t for t in state if t != 0]
    inversions = sum(
        1
        for i in range(len(tiles))
        for j in range(i + 1, len(tiles))
        if tiles[i] > tiles[j]
    )
    return inversions % 2 == 0


def solve(start: tuple) -> list[tuple] | None:
    """
    BFS from start to GOAL. Returns the list of states (the path),
    or None if the puzzle is unsolvable.

    BFS guarantees the shortest path (fewest moves).
    """
    if not is_solvable(start):
        return None

    if start == GOAL:
        return [start]

    # Each queue entry: (current_state, path_so_far)
    queue = deque([(start, [start])])
    visited = {start}

    while queue:
        state, path = queue.popleft()
        blank = state.index(0)

        for neighbor_idx in NEIGHBORS[blank]:
            # Swap blank with the neighboring tile
            new_state = list(state)
            new_state[blank], new_state[neighbor_idx] = (
                new_state[neighbor_idx],
                new_state[blank],
            )
            new_state = tuple(new_state)

            if new_state == GOAL:
                return path + [new_state]

            if new_state not in visited:
                visited.add(new_state)
                queue.append((new_state, path + [new_state]))

    return None  # should not reach here if is_solvable passed


def print_state(state: tuple) -> None:
    for row in range(3):
        row_vals = state[row * 3 : row * 3 + 3]
        print(" ".join(str(v) if v != 0 else "_" for v in row_vals))


def print_solution(path: list[tuple]) -> None:
    for step, state in enumerate(path):
        print(f"Step {step}:")
        print_state(state)
        print()


# ---------------------------------------------------------------------------
# Example
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # Start state:
    #   1 2 3
    #   4 _ 6
    #   7 5 8   →  requires 3 moves
    start = (1, 2, 3, 4, 0, 6, 7, 5, 8)

    path = solve(start)

    if path is None:
        print("This puzzle configuration is unsolvable.")
    else:
        print(f"Solved in {len(path) - 1} moves:\n")
        print_solution(path)
