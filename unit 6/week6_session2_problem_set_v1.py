"""Week 6 Session 2, Version 1: advanced graph problems."""

# Shared imports: dependency queues and minimum-priority heaps.
from collections import defaultdict, deque
import heapq


# ======================================================================
# Problem 1: Crafting Survival Gear -- craftable_gear
# U -- Understand: Supplies are unlimited; completed recipes become available.
# P -- Plan: Count distinct dependencies and release recipes as items arrive.
# I -- Implement
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


# ======================================================================
# Problem 2: Spread the Zombie Cure -- spread_cure
# U -- Understand: Directed nonnegative weights; camp labels are 1 through n.
# P -- Plan: Dijkstra finds earliest arrivals; return the largest, or -1.
# I -- Implement
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


# ======================================================================
# Problem 3: Number of Survival Camps -- num_camps
# U -- Understand: Count horizontal/vertical land groups using Union Find.
# P -- Plan: Start with one group per land cell; subtract only successful merges.
# I -- Implement
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


# ======================================================================
# Problem 4: Find Eventual Safe Locations -- eventual_safe_locations
# U -- Understand: Every path must terminate; one safe path is insufficient.
# P -- Plan: Remove terminal nodes backward; release predecessors with no exits.
# I -- Implement
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


# ======================================================================
# Problem 5: Maximizing Zombie Avoidance -- max_survival_probability
# U -- Understand: Undirected edges; maximize the product, rounding only the result.
# P -- Plan: Dijkstra with highest probability first via negative heap priorities.
# I -- Implement
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


# Example checks -- grouped by exact problem number and title.
if __name__ == '__main__':
    # Problem 1: Crafting Survival Gear
    gear = ['weapon','trap','shelter']
    components = [['metal','wood'],['weapon','wire'],['trap','wood','metal']]
    for count in (1,2,3):
        assert craftable_gear(gear[:count], components[:count], ['metal','wood','wire']) == gear[:count]
    assert craftable_gear(['a','b'], [['b'],['a']], []) == []
    assert craftable_gear(['a'], [[]], []) == ['a']
    assert craftable_gear(['a'], [['missing']], []) == []
    print('Problem 1: Crafting Survival Gear - passed')

    # Problem 2: Spread the Zombie Cure
    # Prompt correction: n=4, not n=1, for the first example.
    assert spread_cure(4, [(2,1,1),(2,3,1),(3,4,1)], 2) == 2
    assert spread_cure(3, [(1,2,1),(2,3,2),(1,3,4)], 1) == 3
    assert spread_cure(2, [(1,2,1)], 2) == -1
    assert spread_cure(1, [], 1) == 0
    assert spread_cure(3, [(1,2,0),(2,3,0),(1,3,5)], 1) == 0
    print('Problem 2: Spread the Zombie Cure - passed')

    # Problem 3: Number of Survival Camps
    assert num_camps([[1,1,1,1,0],[1,1,0,1,0],[1,1,0,0,0],[0,0,0,0,0]]) == 1
    assert num_camps([[1,1,0,0,0],[1,1,0,0,0],[0,0,1,0,0],[0,0,0,1,1]]) == 3
    assert num_camps([[1,1],[1,1]]) == 1
    assert num_camps([[0]]) == 0
    print('Problem 3: Number of Survival Camps - passed')

    # Problem 4: Find Eventual Safe Locations
    assert eventual_safe_locations([[1,2],[2,3],[5],[0],[5],[],[]]) == [2,4,5,6]
    assert eventual_safe_locations([[1,2,3,4],[1,2],[3,4],[0,4],[]]) == [4]
    assert eventual_safe_locations([[0,1],[]]) == [1]
    assert eventual_safe_locations([[]]) == [0]
    print('Problem 4: Find Eventual Safe Locations - passed')

    # Problem 5: Maximizing Zombie Avoidance
    edges = [[0,1],[1,2],[0,2]]
    assert max_survival_probability(3, edges, [0.5,0.5,0.2], 0, 2) == 0.25
    assert max_survival_probability(3, edges, [0.5,0.5,0.3], 0, 2) == 0.3
    assert max_survival_probability(2, [[0,1]], [0.5], 0, 1) == 0.5
    assert max_survival_probability(3, [[0,1]], [0.5], 0, 2) == 0.0
    assert max_survival_probability(1, [], [], 0, 0) == 1.0
    print('Problem 5: Maximizing Zombie Avoidance - passed')
