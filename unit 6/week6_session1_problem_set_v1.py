"""Week 6 Session 1, Version 1: grid problems. Inputs are preserved."""

# Shared import and helper: four-direction traversal for Problems 1, 2, and 5.
from collections import deque


def _neighbors(r, c, rows, cols):
    for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols:
            yield nr, nc


# ======================================================================
# Problem 1: Escape to the Safe Haven -- can_move_safely
# U -- Understand: The initial cell may be 0; every entered cell must be 1.
# P -- Plan: DFS from the start, marking cells when discovered.
# I -- Implement
def can_move_safely(position, grid):
    if not grid or not grid[0] or grid[-1][-1] != 1:
        return False
    rows, cols = len(grid), len(grid[0])
    r, c = position
    if not (0 <= r < rows and 0 <= c < cols):
        return False
    seen = {position}
    stack = [position]
    while stack:
        r, c = stack.pop()
        if (r, c) == (rows - 1, cols - 1):
            return True
        for nr, nc in _neighbors(r, c, rows, cols):
            if grid[nr][nc] == 1 and (nr, nc) not in seen:
                seen.add((nr, nc))
                stack.append((nr, nc))
    return False


# ======================================================================
# Problem 2: List All Escape Routes -- list_all_escape_routes
# U -- Understand: Return safe starting coordinates, not complete paths.
# P -- Plan: One DFS from the haven finds all connected safe cells.
# I -- Implement
def list_all_escape_routes(grid):
    if not grid or not grid[0] or grid[-1][-1] != 1:
        return []
    rows, cols = len(grid), len(grid[0])
    seen = {(rows - 1, cols - 1)}
    stack = list(seen)
    while stack:
        r, c = stack.pop()
        for nr, nc in _neighbors(r, c, rows, cols):
            if grid[nr][nc] == 1 and (nr, nc) not in seen:
                seen.add((nr, nc))
                stack.append((nr, nc))
    return [(r, c) for r in range(rows) for c in range(cols) if (r, c) in seen]


# ======================================================================
# Problem 3: Zombie Spread -- time_to_infect
# U -- Understand: Infection spreads simultaneously from every infected cell.
# P -- Plan: Multi-source BFS; one queue layer represents one hour.
# I -- Implement
def time_to_infect(grid):
    if not grid or not grid[0]:
        return 0
    city = [row[:] for row in grid]
    rows, cols = len(city), len(city[0])
    queue = deque((r, c) for r in range(rows) for c in range(cols) if city[r][c] == 2)
    humans = sum(cell == 1 for row in city for cell in row)
    hours = 0
    while queue and humans:
        for _ in range(len(queue)):
            r, c = queue.popleft()
            for nr, nc in _neighbors(r, c, rows, cols):
                if city[nr][nc] == 1:
                    city[nr][nc] = 2
                    humans -= 1
                    queue.append((nr, nc))
        hours += 1
    return hours if humans == 0 else -1


# ======================================================================
# Problem 4: Zombie Infested City Regions -- count_regions
# U -- Understand: Slashes divide cells into regions; spaces are open.
# P -- Plan: Expand each cell to 3x3; draw walls and flood-fill open pixels.
# I -- Implement
def count_regions(grid):
    size = 3 * len(grid)
    blocked = [[False] * size for _ in range(size)]
    for r, row in enumerate(grid):
        for c, char in enumerate(row):
            for offset in range(3):
                if char == '/':
                    blocked[3*r + offset][3*c + 2 - offset] = True
                elif char == '\\':
                    blocked[3*r + offset][3*c + offset] = True
    regions = 0
    for r in range(size):
        for c in range(size):
            if blocked[r][c]:
                continue
            regions += 1
            blocked[r][c] = True
            stack = [(r, c)]
            while stack:
                row, col = stack.pop()
                for nr, nc in _neighbors(row, col, size, size):
                    if not blocked[nr][nc]:
                        blocked[nr][nc] = True
                        stack.append((nr, nc))
    return regions


# ======================================================================
# Problem 5: Escape the Infected Zone -- escape_subzones
# U -- Understand: Find cells with downhill-or-level routes to both border groups.
# P -- Plan: Search uphill from each border group, then intersect the sets.
# I -- Implement
def escape_subzones(safety):
    if not safety or not safety[0]:
        return []
    rows, cols = len(safety), len(safety[0])

    def reverse_reachable(starts):
        seen = set(starts)
        stack = list(seen)
        while stack:
            r, c = stack.pop()
            for nr, nc in _neighbors(r, c, rows, cols):
                if (nr, nc) not in seen and safety[nr][nc] >= safety[r][c]:
                    seen.add((nr, nc))
                    stack.append((nr, nc))
        return seen

    pacific = reverse_reachable([(0, c) for c in range(cols)] + [(r, 0) for r in range(rows)])
    atlantic = reverse_reachable([(rows-1, c) for c in range(cols)] + [(r, cols-1) for r in range(rows)])
    return [[r, c] for r in range(rows) for c in range(cols)
            if (r, c) in pacific and (r, c) in atlantic]


# Example checks -- grouped by exact problem number and title.
if __name__ == '__main__':
    # Problem 1: Escape to the Safe Haven
    grid = [[1,0,1,1,0],[1,1,1,1,0],[0,0,1,1,0],[1,0,1,1,1]]
    assert [can_move_safely(p, grid) for p in [(0,0),(0,4),(3,0)]] == [True,True,False]
    assert can_move_safely((0,0), [[1]])
    assert not can_move_safely((0,0), [[0]])
    print('Problem 1: Escape to the Safe Haven - passed')

    # Problem 2: List All Escape Routes
    grid = [[1,0,1,0,1],[1,1,1,1,0],[0,0,1,0,0],[1,0,1,1,1]]
    assert list_all_escape_routes(grid) == [(0,0),(0,2),(1,0),(1,1),(1,2),(1,3),(2,2),(3,2),(3,3),(3,4)]
    assert list_all_escape_routes([[0]]) == []
    assert list_all_escape_routes([[1]]) == [(0,0)]
    print('Problem 2: List All Escape Routes - passed')

    # Problem 3: Zombie Spread
    grid = [[2,1,1],[1,1,0],[0,1,1]]
    assert time_to_infect(grid) == 4
    assert grid == [[2,1,1],[1,1,0],[0,1,1]]
    assert time_to_infect([[2,1,1],[0,1,1],[1,0,1]]) == -1
    assert time_to_infect([[0,2]]) == 0
    assert time_to_infect([[2,1,1,1,2]]) == 2
    print('Problem 3: Zombie Spread - passed')

    # Problem 4: Zombie Infested City Regions
    assert count_regions([' /','/ ']) == 2
    assert count_regions([' /','  ']) == 1
    assert count_regions(['/' + chr(92), chr(92) + '/']) == 5
    assert count_regions([' ']) == 1
    print('Problem 4: Zombie Infested City Regions - passed')

    # Problem 5: Escape the Infected Zone
    safety = [[1,2,2,3,5],[3,2,3,4,4],[2,4,5,3,1],[6,7,1,4,5],[5,1,1,2,4]]
    assert escape_subzones(safety) == [[0,4],[1,3],[1,4],[2,2],[3,0],[3,1],[4,0]]
    assert escape_subzones([[2,1],[1,2]]) == [[0,0],[0,1],[1,0],[1,1]]
    assert escape_subzones([[7]]) == [[0,0]]
    print('Problem 5: Escape the Infected Zone - passed')
