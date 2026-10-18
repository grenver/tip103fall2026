# Week 6 - Session 2 - Problem Set Version 1

Use **Understand → Plan → Implement**. Read the plan and trace, predict a result, then open the solution. All implementations preserve their inputs.

| Problem | Callable | Main concept | Prerequisite |
| --- | --- | --- | --- |
| [Problem 1: Crafting Survival Gear](#problem-1-crafting-survival-gear) | `craftable_gear` | Topological dependency processing | Adjacency lists, queues, sets |
| [Problem 2: Spread the Zombie Cure](#problem-2-spread-the-zombie-cure) | `spread_cure` | Dijkstra shortest paths | Adjacency lists, queues, sets |
| [Problem 3: Number of Survival Camps](#problem-3-number-of-survival-camps) | `num_camps` | Union Find / disjoint sets | Adjacency lists, queues, sets |
| [Problem 4: Find Eventual Safe Locations](#problem-4-find-eventual-safe-locations) | `eventual_safe_locations` | Reverse topological elimination | Adjacency lists, queues, sets |
| [Problem 5: Maximizing Zombie Avoidance](#problem-5-maximizing-zombie-avoidance) | `max_survival_probability` | Maximum-product Dijkstra | Adjacency lists, queues, sets |

**Toolbox:** `set` stores unique items and supports expected constant-time membership. `stack.pop()` removes the newest item (DFS); `deque.popleft()` removes the oldest (BFS). `heapq.heappop()` removes the smallest priority, with logarithmic push/pop cost. The Python file includes shared imports/helpers; copy those too when submitting one function.

## Problem 1: Crafting Survival Gear

**Callable:** `craftable_gear` · **Learning goal:** Explain and apply topological dependency processing.

**Key concept / recognition clue:** A recipe becomes usable when its missing-component count reaches zero. Reverse dependency lists tell us which counts to update when an item becomes available.

### U — Understand

Return craftable gear names in any order. Supplies are unlimited. Assume unique gear names and matching gear/components lists; repeated components need only one available material type.

### P — Plan

Build component-to-recipe lists and distinct-component counts. Announce initial supplies and empty recipes once through a queue. Each announcement decreases dependent counts; newly ready recipes become available.

**Trace:** metal and wood release weapon; weapon and wire release trap; trap, wood, and metal release shelter. A cycle a -> b -> a without a supplied seed releases neither.

**Why it works:** A recipe reaches zero only after every required material has been announced. Conversely, any recipe whose materials become available is eventually released. Missing materials and unseeded cycles remain blocked.

### I — Implement

<details>
<summary>Show solution after trying the plan</summary>

```python
def craftable_gear(gear, components, supplies):
    dependents = defaultdict(list)
    remaining = {}
    for item, recipe in zip(gear, components):
        required = set(recipe)
        remaining[item] = len(required)
        for component in required:
            dependents[component].append(item)
    available = set(supplies)
    available.update(item for item in gear if remaining[item] == 0)
    queue = deque(available)
    while queue:
        component = queue.popleft()
        for item in dependents[component]:
            remaining[item] -= 1
            if remaining[item] == 0 and item not in available:
                available.add(item)
                queue.append(item)
    return [item for item in gear if remaining[item] == 0]
```

</details>

**Code connection:** `remaining` counts unannounced required types; `available` prevents announcing an item more than once.

**Cost:** Let G be gear, S supplies, and D total component entries. Expected O(G+S+D) time and auxiliary space; each dependency is processed at most once.

**Common mistake → correction:** Treating every zero-indegree material as available invents supplies. Only initial supplies and craftable recipes may seed the queue.

**Interview explanation:** Build component-to-recipe lists and distinct-component counts. Announce initial supplies and empty recipes once through a queue. Each announcement decreases dependent counts; newly ready recipes become available. A recipe reaches zero only after every required material has been announced. Conversely, any recipe whose materials become available is eventually released. Missing materials and unseeded cycles remain blocked. Let G be gear, S supplies, and D total component entries. Expected O(G+S+D) time and auxiliary space; each dependency is processed at most once.

**Check your understanding:** Can an empty recipe be crafted? What if one ingredient never appears in supplies or any recipe?

<details>
<summary>Reasoning and answers</summary>

An empty recipe is immediately ready. A permanently missing ingredient blocks that recipe and any chain depending on it.

</details>

## Problem 2: Spread the Zombie Cure

**Callable:** `spread_cure` · **Learning goal:** Explain and apply dijkstra shortest paths.

**Key concept / recognition clue:** A minimum heap removes the smallest tentative arrival time. Weighted travel requires comparing elapsed time rather than number of edges.

### U — Understand

Return the maximum of the earliest arrival times, or -1 if a camp is unreachable. Assume n >= 1, labels 1..n, and nonnegative travel times. Prompt correction: the first call must be spread_cure(4, times_1, 2), not n=1, to produce 2.

### P — Plan

Initialize k at time 0 and others at infinity. Pop the earliest entry, skip outdated entries, and relax outgoing edges whenever a faster arrival is found. Return the largest finite distance.

**Trace:** From camp 2, distances to 1 and 3 become 1; processing camp 3 sets camp 4 to 2. The maximum is 2, not the sum 4.

**Why it works:** With nonnegative weights, extending a route cannot improve a smaller already-finalized arrival. Thus the minimum current heap entry has its optimal time. The last earliest arrival determines when everyone has the cure.

### I — Implement

<details>
<summary>Show solution after trying the plan</summary>

```python
def spread_cure(n, times, k):
    neighbors = [[] for _ in range(n + 1)]
    for u, v, weight in times:
        neighbors[u].append((v, weight))
    distance = [float('inf')] * (n + 1)
    distance[k] = 0
    heap = [(0, k)]
    while heap:
        elapsed, camp = heapq.heappop(heap)
        if elapsed != distance[camp]:
            continue
        for neighbor, weight in neighbors[camp]:
            arrival = elapsed + weight
            if arrival < distance[neighbor]:
                distance[neighbor] = arrival
                heapq.heappush(heap, (arrival, neighbor))
    answer = max(distance[1:])
    return -1 if answer == float('inf') else answer
```

</details>

**Code connection:** An infinity distance means unreachable. A heap entry differing from the current distance is outdated and can be skipped.

**Cost:** Let V=n and E=len(times). O(V+E log(E+2)) time and O(V+E) auxiliary space for adjacency, distances, and a lazy heap. The heap may hold multiple entries per vertex.

**Common mistake → correction:** Using FIFO BFS ignores different edge weights. Summing distances measures total individual waiting, not when the last camp is reached.

**Interview explanation:** Initialize k at time 0 and others at infinity. Pop the earliest entry, skip outdated entries, and relax outgoing edges whenever a faster arrival is found. Return the largest finite distance. With nonnegative weights, extending a route cannot improve a smaller already-finalized arrival. Thus the minimum current heap entry has its optimal time. The last earliest arrival determines when everyone has the cure. Let V=n and E=len(times). O(V+E log(E+2)) time and O(V+E) auxiliary space for adjacency, distances, and a lazy heap. The heap may hold multiple entries per vertex.

**Check your understanding:** What is returned for one camp and no edges? Can the cure travel backward along a listed edge?

<details>
<summary>Reasoning and answers</summary>

0 when k=1. No: edges are directed, so a reverse edge must be explicitly present.

</details>

## Problem 3: Number of Survival Camps

**Callable:** `num_camps` · **Learning goal:** Explain and apply union find / disjoint sets.

**Key concept / recognition clue:** A parent array assigns each cell to a representative root. find follows parents; path compression shortens future searches. Union by size attaches the smaller tree to the larger.

### U — Understand

Return the number of connected groups of integer 1s, using Union Find as requested. Only horizontal and vertical connections count; preserve city.

### P — Plan

Map (r,c) to r*cols+c. Count land cells as separate groups. Compare each land cell with right/down land neighbors; merge different roots and subtract one group.

**Trace:** A 2x2 all-land grid starts at 4. Three successful merges reduce it to 1. The final edge connects roots already equal, so the count stays 1.

**Why it works:** Initially each land cell is a separate component. A merge of two different components reduces the count by exactly one; an edge inside one component does not. Right/down examines every undirected adjacency once.

### I — Implement

<details>
<summary>Show solution after trying the plan</summary>

```python
def num_camps(city):
    if not city or not city[0]:
        return 0
    rows, cols = len(city), len(city[0])
    parent = list(range(rows * cols))
    size = [1] * (rows * cols)
    count = sum(cell == 1 for row in city for cell in row)

    def find(node):
        while node != parent[node]:
            parent[node] = parent[parent[node]]
            node = parent[node]
        return node

    for r in range(rows):
        for c in range(cols):
            if city[r][c] != 1:
                continue
            for nr, nc in ((r + 1, c), (r, c + 1)):
                if nr < rows and nc < cols and city[nr][nc] == 1:
                    a, b = find(r * cols + c), find(nr * cols + nc)
                    if a != b:
                        if size[a] < size[b]:
                            a, b = b, a
                        parent[b] = a
                        size[a] += size[b]
                        count -= 1
    return count
```

</details>

**Code connection:** `r * cols + c` gives each cell a unique integer ID. Parent halving compresses paths while `size` keeps trees shallow.

**Cost:** Let N=RC. O(N alpha(N)) amortized time and O(N) auxiliary space, where inverse Ackermann alpha grows extremely slowly. Initialization is O(N).

**Common mistake → correction:** Subtracting for every adjacent pair overcounts merges in a cycle. Subtract only when the two roots differ.

**Interview explanation:** Map (r,c) to r*cols+c. Count land cells as separate groups. Compare each land cell with right/down land neighbors; merge different roots and subtract one group. Initially each land cell is a separate component. A merge of two different components reduces the count by exactly one; an edge inside one component does not. Right/down examines every undirected adjacency once. Let N=RC. O(N alpha(N)) amortized time and O(N) auxiliary space, where inverse Ackermann alpha grows extremely slowly. Initialization is O(N).

**Check your understanding:** How many camps in [[1,0],[0,1]]? Why do water cells not affect the count despite having parent slots?

<details>
<summary>Reasoning and answers</summary>

Two: diagonal contact is insufficient. Water is never counted or merged; its allocated parent entries are unused.

</details>

## Problem 4: Find Eventual Safe Locations

**Callable:** `eventual_safe_locations` · **Learning goal:** Explain and apply reverse topological elimination.

**Key concept / recognition clue:** Begin with nodes having no exits. Once every exit of a predecessor leads to confirmed-safe nodes, that predecessor is also safe.

### U — Understand

Return sorted safe node indices. Every possible path must terminate. A node with both a terminal route and a cycle route is unsafe.

### P — Plan

Build reverse edges and outgoing counts. Queue terminal nodes; remove their incoming dependencies by decrementing predecessor counts. Release predecessors at zero, then scan indices in ascending order.

**Trace:** In [[1,2],[1],[]], node 2 is terminal. Removing its edge from 0 leaves the exit to 1; the self-cycle at 1 remains. Only [2] is safe.

**Why it works:** A node enters the queue only after all its successors are safe. Cycles retain unresolved exits, as do nodes that can reach them. Processing each edge once eventually discovers every safe node.

### I — Implement

<details>
<summary>Show solution after trying the plan</summary>

```python
def eventual_safe_locations(city):
    reverse = [[] for _ in city]
    exits = [len(neighbors) for neighbors in city]
    for node, neighbors in enumerate(city):
        for neighbor in neighbors:
            reverse[neighbor].append(node)
    queue = deque(node for node, count in enumerate(exits) if count == 0)
    safe = [False] * len(city)
    while queue:
        node = queue.popleft()
        safe[node] = True
        for previous in reverse[node]:
            exits[previous] -= 1
            if exits[previous] == 0:
                queue.append(previous)
    return [node for node in range(len(city)) if safe[node]]
```

</details>

**Code connection:** `exits` counts unresolved outgoing edges, not incoming edges. Reverse lists let a safe node notify its predecessors.

**Cost:** O(V+E) time and auxiliary space for V nodes and E adjacency entries. An ascending index scan supplies sorted output without sorting.

**Common mistake → correction:** Checking for any terminal path accepts nodes that also reach cycles. Require all outgoing paths to be safe.

**Interview explanation:** Build reverse edges and outgoing counts. Queue terminal nodes; remove their incoming dependencies by decrementing predecessor counts. Release predecessors at zero, then scan indices in ascending order. A node enters the queue only after all its successors are safe. Cycles retain unresolved exits, as do nodes that can reach them. Processing each edge once eventually discovers every safe node. O(V+E) time and auxiliary space for V nodes and E adjacency entries. An ascending index scan supplies sorted output without sorting.

**Check your understanding:** Is an isolated node safe? What about a node with a self-loop and an edge to a terminal node?

<details>
<summary>Reasoning and answers</summary>

The isolated node is terminal and safe. The second is unsafe because repeatedly taking its self-loop never terminates.

</details>

## Problem 5: Maximizing Zombie Avoidance

**Callable:** `max_survival_probability` · **Learning goal:** Explain and apply maximum-product dijkstra.

**Key concept / recognition clue:** Independent road success probabilities multiply along a route. Negating priorities lets Python's minimum heap retrieve the largest probability first.

### U — Understand

Return the best probability rounded to two decimal places, or 0 if disconnected. Assume probabilities in [0,1], node labels 0..n-1, and matching edges/probability lists. Numeric 0.3 and 0.30 are the same return value.

### P — Plan

Store roads in both directions. Begin with probability 1 at start. Pop the highest candidate, skip obsolete entries, and update neighbors when multiplication improves their best value. Round only when returning.

**Trace:** For chances 0.5, 0.5, and direct 0.2, via node 1 gives 0.25 and replaces 0.2. If the direct edge is 0.3, that direct route wins.

**Why it works:** Multiplying by a number at most 1 cannot improve a path probability. Therefore the highest current candidate cannot later be improved through a lower candidate; reaching end at that priority is optimal.

### I — Implement

<details>
<summary>Show solution after trying the plan</summary>

```python
def max_survival_probability(n, edges, succ_prob, start, end):
    neighbors = [[] for _ in range(n)]
    for (a, b), probability in zip(edges, succ_prob):
        neighbors[a].append((b, probability))
        neighbors[b].append((a, probability))
    best = [0.0] * n
    best[start] = 1.0
    heap = [(-1.0, start)]
    while heap:
        negative, node = heapq.heappop(heap)
        probability = -negative
        if probability < best[node]:
            continue
        if node == end:
            return round(probability, 2)
        for neighbor, chance in neighbors[node]:
            candidate = probability * chance
            if candidate > best[neighbor]:
                best[neighbor] = candidate
                heapq.heappush(heap, (-candidate, neighbor))
    return 0.0
```

</details>

**Code connection:** Negative priorities put larger probabilities first. `best` retains unrounded values throughout the search.

**Cost:** Let V=n and E=len(edges). O(V+E log(E+2)) time and O(V+E) auxiliary space, including multiple tentative heap entries.

**Common mistake → correction:** Adding probabilities can exceed 1 and misrank routes. Multiplication is required. Rounding partial routes can change rankings; defer it to the end.

**Interview explanation:** Store roads in both directions. Begin with probability 1 at start. Pop the highest candidate, skip obsolete entries, and update neighbors when multiplication improves their best value. Round only when returning. Multiplying by a number at most 1 cannot improve a path probability. Therefore the highest current candidate cannot later be improved through a lower candidate; reaching end at that priority is optimal. Let V=n and E=len(edges). O(V+E log(E+2)) time and O(V+E) auxiliary space, including multiple tentative heap entries.

**Check your understanding:** What if start equals end? What if the only road has probability 0?

<details>
<summary>Reasoning and answers</summary>

The empty route succeeds with probability 1. A zero-probability route returns 0, matching the required failure probability.

</details>

## Run the example checks

Run `python "unit 6/week6_session2_problem_set_v1.py"` from the repository root. Checks cover supplied examples and targeted boundary cases. A successful run prints one labeled confirmation per problem.
