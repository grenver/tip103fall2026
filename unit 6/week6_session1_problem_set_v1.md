# Week 6 - Session 1 - Problem Set Version 1

Use **Understand → Plan → Implement**. Read the plan and trace, predict a result, then open the solution. All implementations preserve their inputs.

| Problem | Callable | Main concept | Prerequisite |
| --- | --- | --- | --- |
| [Problem 1: Escape to the Safe Haven](#problem-1-escape-to-the-safe-haven) | `can_move_safely` | DFS reachability | Loops, tuples, sets |
| [Problem 2: List All Escape Routes](#problem-2-list-all-escape-routes) | `list_all_escape_routes` | Reverse reachability | Loops, tuples, sets |
| [Problem 3: Zombie Spread](#problem-3-zombie-spread) | `time_to_infect` | Multi-source BFS | Loops, tuples, sets |
| [Problem 4: Zombie Infested City Regions](#problem-4-zombie-infested-city-regions) | `count_regions` | Expand geometry, then flood-fill | Loops, tuples, sets |
| [Problem 5: Escape the Infected Zone](#problem-5-escape-the-infected-zone) | `escape_subzones` | Reverse traversal and set intersection | Loops, tuples, sets |

**Toolbox:** `set` stores unique items and supports expected constant-time membership. `stack.pop()` removes the newest item (DFS); `deque.popleft()` removes the oldest (BFS). `heapq.heappop()` removes the smallest priority, with logarithmic push/pop cost. The Python file includes shared imports/helpers; copy those too when submitting one function.

## Problem 1: Escape to the Safe Haven

**Callable:** `can_move_safely` · **Learning goal:** Explain and apply dfs reachability.

**Key concept / recognition clue:** A stack explores one branch at a time; a set prevents revisiting cells. Four-way movement makes each safe cell a graph vertex.

### U — Understand

Return a Boolean indicating whether position can reach the bottom-right through 1s. The supplied second example permits an initial 0; only subsequent cells must be safe. Assume a rectangular binary grid and a valid coordinate. Empty grids return False as an extension.

### P — Plan

Start with the supplied coordinate in the stack and seen set. Pop a cell, check the destination, then push unseen safe neighbors. Stop on success or an empty stack.

**Trace:** From (0,4), enter (0,3), then (1,3), (2,3), (3,3), and (3,4). Starting at 0 is permitted; entering another 0 is not.

**Why it works:** Each discovered cell has a legal route from the start. Exploring every eligible neighbor exhausts all possible routes, and marking on discovery ensures termination.

### I — Implement

<details>
<summary>Show solution after trying the plan</summary>

```python
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
```

</details>

**Code connection:** The shared `_neighbors` generator yields only in-bounds coordinates. Marking a coordinate before pushing it prevents duplicate work.

**Cost:** O(RC) time and auxiliary space for an R-by-C grid: each cell is discovered once and has at most four neighbors.

**Common mistake → correction:** Rejecting an initial 0 contradicts the example. Allow it only at initialization; never allow later infected cells.

**Interview explanation:** Start with the supplied coordinate in the stack and seen set. Pop a cell, check the destination, then push unseen safe neighbors. Stop on success or an empty stack. Each discovered cell has a legal route from the start. Exploring every eligible neighbor exhausts all possible routes, and marking on discovery ensures termination. O(RC) time and auxiliary space for an R-by-C grid: each cell is discovered once and has at most four neighbors.

**Check your understanding:** Would [[0,1]] from (0,0) succeed? What changes if diagonal moves are allowed?

<details>
<summary>Reasoning and answers</summary>

Yes. Add diagonal offsets to the neighbor helper; the graph then has up to eight neighbors per cell.

</details>

## Problem 2: List All Escape Routes

**Callable:** `list_all_escape_routes` · **Learning goal:** Explain and apply reverse reachability.

**Key concept / recognition clue:** Safe adjacency is bidirectional: if A reaches B, B reaches A. Therefore one search from the destination finds every valid start.

### U — Understand

Return a list of coordinate tuples, not lists of paths. Unlike Problem 1, a starting 0 is disallowed. Return coordinates in row-major order to match the example; preserve the input.

### P — Plan

If the haven is blocked, return []. Otherwise search its safe connected component, then scan the grid in row-major order to collect visited coordinates.

**Trace:** For [[1,0],[1,1]], search (1,1) -> (1,0) -> (0,0). Return [(0,0),(1,0),(1,1)].

**Why it works:** Reversing a safe path preserves every edge. Exactly the cells found from the haven can reach it. Each cell is marked once.

### I — Implement

<details>
<summary>Show solution after trying the plan</summary>

```python
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
```

</details>

**Code connection:** The shared `_neighbors` generator yields only in-bounds coordinates. Marking a coordinate before pushing it prevents duplicate work.

**Cost:** O(RC) time and auxiliary space; the final scan is linear, and output has at most RC tuples.

**Common mistake → correction:** Running a fresh search from every cell repeats work and can cost O((RC)^2). Search once from the shared destination.

**Interview explanation:** If the haven is blocked, return []. Otherwise search its safe connected component, then scan the grid in row-major order to collect visited coordinates. Reversing a safe path preserves every edge. Exactly the cells found from the haven can reach it. Each cell is marked once. O(RC) time and auxiliary space; the final scan is linear, and output has at most RC tuples.

**Check your understanding:** What does [[1]] return? Would this reversal work unchanged on directed roads?

<details>
<summary>Reasoning and answers</summary>

[(0,0)]. Directed roads require reversing the edges before searching from the destination.

</details>

## Problem 3: Zombie Spread

**Callable:** `time_to_infect` · **Learning goal:** Explain and apply multi-source bfs.

**Key concept / recognition clue:** A FIFO queue processes cells in discovery order. Put every initial zombie in it so all infection fronts advance together.

### U — Understand

Return hours until no 1 remains, or -1 if humans are unreachable. Zero is an obstacle, not a human. The implementation copies the grid, preserving the original.

### P — Plan

Count humans and enqueue all zombies. Process exactly the current queue length per hour. Mark each newly infected cell immediately and queue it for the next hour.

**Trace:** On [[2,1,1]], hour 1 infects the middle cell; hour 2 infects the last. Capturing len(queue) prevents both infections occurring in hour 1.

**Why it works:** Every layer contains cells infected at the same earliest time. Immediate marking prevents two zombies from counting one human twice. With humans left and no frontier, further spread is impossible.

### I — Implement

<details>
<summary>Show solution after trying the plan</summary>

```python
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
```

</details>

**Code connection:** `range(len(queue))` fixes the current frontier size; newly enqueued cells wait until the next hour.

**Cost:** O(RC) time and auxiliary space: scanning, copying, and processing all cells are linear.

**Common mistake → correction:** Processing a growing queue as one hour makes infection travel arbitrarily far instantly. Freeze the layer length before processing.

**Interview explanation:** Count humans and enqueue all zombies. Process exactly the current queue length per hour. Mark each newly infected cell immediately and queue it for the next hour. Every layer contains cells infected at the same earliest time. Immediate marking prevents two zombies from counting one human twice. With humans left and no frontier, further spread is impossible. O(RC) time and auxiliary space: scanning, copying, and processing all cells are linear.

**Check your understanding:** What does [[0,2]] return? Why can ordinary DFS give wrong infection times?

<details>
<summary>Reasoning and answers</summary>

0, because no humans remain. DFS explores depth before comparing simultaneous fronts; BFS layers model earliest arrival.

</details>

## Problem 4: Zombie Infested City Regions

**Callable:** `count_regions` · **Learning goal:** Explain and apply expand geometry, then flood-fill.

**Key concept / recognition clue:** A 3x3 block draws each slash as three wall pixels while leaving room on each side. Open connected components represent regions.

### U — Understand

Input is an n-by-n array of strings containing slash, backslash, or space. Return the number of open regions. In Python a literal backslash must be escaped. The prompt incorrectly mixes four-triangle and 3x3 methods; this solution uses nine pixels per cell.

### P — Plan

Draw / on the anti-diagonal and backslash on the main diagonal of each 3x3 block. Scan open pixels; each unvisited one starts a new flood-fill and increments the count.

**Trace:** A single / becomes rows 001, 010, 100 (1 means wall). Its two open sides cannot connect through four-way movement, so the answer is 2.

**Why it works:** The expansion preserves which sides of a cell connect around its fence. Flood-fill visits exactly one connected open region; visited pixels cannot start another count.

### I — Implement

<details>
<summary>Show solution after trying the plan</summary>

```python
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
```

</details>

**Code connection:** The expanded `blocked` matrix stores walls first, then also marks visited pixels. The backslash literal uses two backslashes in Python source to represent one character.

**Cost:** O(n^2) time and auxiliary space: the expanded grid has 9n^2 pixels, a constant-factor increase.

**Common mistake → correction:** Allowing diagonal flood-fill crosses fence corners and merges separate regions. Use only up, down, left, and right.

**Interview explanation:** Draw / on the anti-diagonal and backslash on the main diagonal of each 3x3 block. Scan open pixels; each unvisited one starts a new flood-fill and increments the count. The expansion preserves which sides of a cell connect around its fence. Flood-fill visits exactly one connected open region; visited pixels cannot start another count. O(n^2) time and auxiliary space: the expanded grid has 9n^2 pixels, a constant-factor increase.

**Check your understanding:** How many regions does one space make? How many does a single backslash make?

<details>
<summary>Reasoning and answers</summary>

One and two respectively. An empty cell has no wall; either slash separates its two sides.

</details>

## Problem 5: Escape the Infected Zone

**Callable:** `escape_subzones` · **Learning goal:** Explain and apply reverse traversal and set intersection.

**Key concept / recognition clue:** A forward move goes downhill or stays level. Reverse it to go uphill or stay level, starting at all boundary cells of each safety zone.

### U — Understand

Return coordinate lists for cells that can reach both border groups, potentially using two different paths. Pacific is top/left; Atlantic is bottom/right. Assume a rectangular integer matrix.

### P — Plan

Search from top and left with the reversed >= rule. Search independently from bottom and right. Return the intersection in row-major order.

**Trace:** For [[2,1],[1,2]], all four cells qualify: the low cells already touch both border groups, and each high cell can descend to them.

**Why it works:** A reversed path corresponds exactly to a permitted forward escape. Membership in both sets proves an escape to each border group. Seen sets prevent cycles on equal-height plateaus.

### I — Implement

<details>
<summary>Show solution after trying the plan</summary>

```python
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
```

</details>

**Code connection:** The shared `_neighbors` generator yields only in-bounds coordinates. Marking a coordinate before pushing it prevents duplicate work.

**Cost:** O(RC) time and auxiliary space: two searches each visit a cell at most once; output is at most RC coordinates.

**Common mistake → correction:** Using <= in the reverse search follows the original direction and identifies the wrong cells. Reverse both the starting perspective and the height comparison.

**Interview explanation:** Search from top and left with the reversed >= rule. Search independently from bottom and right. Return the intersection in row-major order. A reversed path corresponds exactly to a permitted forward escape. Membership in both sets proves an escape to each border group. Seen sets prevent cycles on equal-height plateaus. O(RC) time and auxiliary space: two searches each visit a cell at most once; output is at most RC coordinates.

**Check your understanding:** Does [[7]] qualify? What happens on a flat grid?

<details>
<summary>Reasoning and answers</summary>

[[0,0]] qualifies because it touches both groups. Every flat-grid cell qualifies because equal-height moves connect the entire grid.

</details>

## Run the example checks

Run `python "unit 6/week6_session1_problem_set_v1.py"` from the repository root. Checks cover supplied examples and targeted boundary cases. A successful run prints one labeled confirmation per problem.
