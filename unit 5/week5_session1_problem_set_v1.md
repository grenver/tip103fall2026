# Week 5 — Session 1 — Problem Set Version 1

## Problem index and concept map

| Problem | Callable | Main concept | Prerequisite | Explain to a student |
| --- | --- | --- | --- | --- |
| [Problem 1: There and Back](#problem-1-there-and-back) | `bidirectional_flights` | Check reverse edges | Lists, sets, membership | Why a return path is not enough |
| [Problem 2: Find Center of Airport](#problem-2-find-center-of-airport) | `find_center` | Use the star graph guarantee | Edges and endpoints | Why two edges identify the center |
| [Problem 3: Finding All Reachable Destinations](#problem-3-finding-all-reachable-destinations) | `get_all_destinations` | BFS with a FIFO queue | Sets and queue operations | Why FIFO gives distance order |
| [Problem 4: Finding All Reachable Destinations II](#problem-4-finding-all-reachable-destinations-ii) | `get_all_destinations_dfs` | DFS in neighbor order | Recursion and visited sets | Why one branch finishes first |
| [Problem 5: Find Itinerary](#problem-5-find-itinerary) | `find_itinerary` | Find the route head, then follow links | Dictionaries and sets | How to locate the first departure |

Solutions are visible for review. U and P come before I. Python banners and check blocks use the same problem numbers and titles.

## Problem 1: There and Back

**Callable:** `bidirectional_flights` · **Learning goal / concept:** Check reverse edges.

### U — Understand

Input: a 0-indexed adjacency list. Return a boolean indicating whether every flight has a reverse flight. Check each individual edge; this is different from checking whether airports can eventually reach each other.

**Recognition clue:** “For every flight … there also exists” asks for a reverse-edge check.

### P — Plan

Convert each adjacency list to a set for efficient membership checks. For every edge i → j, check whether i belongs to j’s neighbor set. Return False on the first missing reverse edge; otherwise return True.

**Trace:** In [[1, 2], [], [0], [2]], checking 0 → 1 fails because flights[1] does not contain 0.

**Why it works:** Every edge is checked against exactly its reverse, so True means the requirement holds everywhere.

### I — Implement

```python
def bidirectional_flights(flights):
    neighbors = [set(destinations) for destinations in flights]
    for origin, destinations in enumerate(flights):
        for destination in destinations:
            if origin not in neighbors[destination]:
                return False
    return True
```

**Code connection:** `set(...)` supports efficient reverse-edge membership tests; no traversal or sorting is needed.

**Checks:** The supplied examples return True and False; the second catches an absent reverse edge.

**Cost:** Let V be airports and E be listed flights. Expected O(V + E) time and O(V + E) auxiliary space for the neighbor sets.

**Common mistake:** Checking only that j has some outgoing flight → a different destination does not establish j → i. Check membership of i specifically.

**Interview explanation:** Every edge is checked against exactly its reverse, so True means the requirement holds everywhere. Let V be airports and E be listed flights. Expected O(V + E) time and O(V + E) auxiliary space for the neighbor sets.

**Check your understanding:** Does [[1], [2], [0]] pass? How would you return missing reverse flights instead?

<details>
<summary>Reasoning and answers</summary>

No: a cycle provides indirect return routes, not reverse edges. Collect (j, i) whenever i → j lacks its reverse.

</details>

## Problem 2: Find Center of Airport

**Callable:** `find_center` · **Learning goal / concept:** Use the star graph guarantee.

### U — Understand

Input: edges of a valid undirected star graph, with terminals labeled 1 through n. Return the center terminal. Assume at least two edges so the center is uniquely identifiable.

**Recognition clue:** The star guarantee means every edge shares the center.

**Prompt correction:** The supplied hint says the center appears in “all but one” edge. It actually appears in every edge.

### P — Plan

Read the first edge’s two endpoints. The endpoint also present in the second edge is the center.

**Trace:** For [1, 2] and [2, 3], the shared endpoint is 2.

**Why it works:** Every star edge touches the center, and distinct outer terminals cannot be the shared endpoint of two different edges.

### I — Implement

```python
def find_center(terminals):
    first, second = terminals[0]
    if first in terminals[1]:
        return first
    return second
```

**Code connection:** `first in terminals[1]` checks just two endpoints, so input size does not affect the work.

**Checks:** Both supplied examples return 2 and 1; reversed endpoint order should produce the same center.

**Cost:** O(1) time and auxiliary space: inspect only two edges, each with two endpoints.

**Common mistake:** Counting every terminal’s degree works but misses the constant-time property. Use the shared endpoint when the star guarantee is given.

**Interview explanation:** Every star edge touches the center, and distinct outer terminals cannot be the shared endpoint of two different edges. O(1) time and auxiliary space: inspect only two edges, each with two endpoints.

**Check your understanding:** If the first edge is reversed to [2, 1], does the answer change? Would this method work on any graph?

<details>
<summary>Reasoning and answers</summary>

No; either endpoint order still finds 2. It does not work on arbitrary graphs because two edges may share a node that is not a universal center.

</details>

## Problem 3: Finding All Reachable Destinations

**Callable:** `get_all_destinations` · **Learning goal / concept:** BFS with a FIFO queue.

### U — Understand

Input: a directed adjacency dictionary and starting airport. Return reachable airports, including start as shown in the examples, ordered by minimum flights from start (equivalently, minimum layovers for other destinations). Keep supplied neighbor order to reproduce the examples.

**Recognition clue:** “Ascending order by number of layovers” points to breadth-first search.

### P — Plan

Put start in a deque and visited set. Remove the front airport and append it to the result. Enqueue unseen neighbors at the back, marking them visited immediately. Stop when the queue is empty.

**Trace:** From Beijing: queue [Beijing] → [Mexico City, Helsinki] → [Helsinki, Sydney] → [Sydney, Cairo, New York]. Direct destinations leave the queue before destinations requiring another flight.

**Why it works:** A FIFO queue processes all airports at one distance before the next distance. Marking on enqueue prevents repeated entries when routes converge or contain cycles.

### I — Implement

```python
def get_all_destinations(flights, start):
    queue = deque([start])
    visited = {start}
    destinations = []
    while queue:
        airport = queue.popleft()
        destinations.append(airport)
        for neighbor in flights.get(airport, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    return destinations
```

**Code connection:** `popleft()` removes and returns the oldest queued airport; `append()` schedules a neighbor at the back. Neither operation sorts.

**Checks:** The supplied Beijing and Helsinki results match; cycles must not duplicate airports.

**Cost:** Let Vᵣ be reachable airports and Eᵣ their outgoing edges. Expected O(Vᵣ + Eᵣ) time, O(Vᵣ) auxiliary space, and O(Vᵣ) output space.

**Common mistake:** Sorting airport names → alphabetical order loses the distance requirement. Use BFS. Marking only after removal → duplicate queue entries; mark on enqueue.

**Interview explanation:** A FIFO queue processes all airports at one distance before the next distance. Marking on enqueue prevents repeated entries when routes converge or contain cycles. Let Vᵣ be reachable airports and Eᵣ their outgoing edges. Expected O(Vᵣ + Eᵣ) time, O(Vᵣ) auxiliary space, and O(Vᵣ) output space.

**Check your understanding:** Why is Beijing returned first? What changes if flight connections have different travel times?

<details>
<summary>Reasoning and answers</summary>

The examples include start at distance zero. BFS minimizes the number of equal-cost edges; differing travel times require an algorithm that accounts for those weights.

</details>

## Problem 4: Finding All Reachable Destinations II

**Callable:** `get_all_destinations_dfs` · **Learning goal / concept:** DFS in neighbor order.

### U — Understand

Input: the same kind of directed adjacency dictionary. Return reachable airports including start, in DFS discovery order. The prompt calls this function get_all_destinations; the Python file uses get_all_destinations_dfs to keep Problem 3 callable. Rename it for a standalone submission.

**Recognition clue:** The prompt explicitly requires DFS visitation order.

**Missing dictionary key:** The supplied DFS example lists New York as a destination but omits its key. Treat it as having no outgoing flights using `flights.get(airport, [])`.

### P — Plan

Use a recursive helper. Mark and append the current airport, then recursively explore each unseen neighbor in supplied order. Return when there are no unseen neighbors; continue the preceding airport’s remaining neighbors.

**Trace:** From Beijing: Beijing → Mexico City → Sydney → Tokyo. Tokyo leads to visited Sydney, so recursion returns to explore Beijing’s next branch: Helsinki → Cairo → Reykjavik → New York.

**Why it works:** Each call explores an airport’s unseen descendants before returning to the next sibling branch. The visited set prevents cycles.

### I — Implement

```python
def get_all_destinations_dfs(flights, start):
    visited = set()
    destinations = []

    def visit(airport):
        visited.add(airport)
        destinations.append(airport)
        for neighbor in flights.get(airport, []):
            if neighbor not in visited:
                visit(neighbor)

    visit(start)
    return destinations
```

**Code connection:** The helper marks the airport before recursion. `get(..., [])` lets destination-only airports terminate naturally.

**Checks:** Both supplied DFS orders match, including destination-only New York.

**Cost:** With Vᵣ reachable airports and Eᵣ outgoing edges, expected O(Vᵣ + Eᵣ) time. Visited storage and worst-case recursion use O(Vᵣ) auxiliary space; output uses O(Vᵣ).

**Common mistake:** Using BFS → different discovery order. Forgetting visited → recursion loops on Tokyo ↔ Sydney. Mark before exploring children.

**Interview explanation:** Each call explores an airport’s unseen descendants before returning to the next sibling branch. The visited set prevents cycles. With Vᵣ reachable airports and Eᵣ outgoing edges, expected O(Vᵣ + Eᵣ) time. Visited storage and worst-case recursion use O(Vᵣ) auxiliary space; output uses O(Vᵣ).

**Check your understanding:** Why does Tokyo precede Helsinki here? What happens if Beijing’s neighbor order is reversed?

<details>
<summary>Reasoning and answers</summary>

DFS finishes the Mexico City branch before the Helsinki branch. Reversing neighbors explores Helsinki first and changes discovery order without changing which airports are reachable.

</details>

## Problem 5: Find Itinerary

**Callable:** `find_itinerary` · **Learning goal / concept:** Find the route head, then follow links.

### U — Understand

Input: unordered (departure, arrival) pairs forming one route with no repeated airport or cycle. Return all airports in travel order. The empty-input extension returns [].

**Recognition clue:** “Each airport is visited only once” gives a single chain to follow.

### P — Plan

Build a departure-to-arrival dictionary and a set of arrivals. Find the departure that never appears as an arrival. Append it, then follow dictionary links until the current airport has no departure.

**Trace:** Arrivals are ATL, JFK, ORD, SFO. LAX is the only departure outside that set. Follow LAX → SFO → JFK → ATL → ORD, then stop.

**Why it works:** Only the first airport has no incoming flight. Each mapping gives its unique next stop, so following links reconstructs the entire guaranteed route.

### I — Implement

```python
def find_itinerary(boarding_passes):
    if not boarding_passes:
        return []
    next_airport = dict(boarding_passes)
    arrivals = {arrival for _, arrival in boarding_passes}
    start = next(airport for airport in next_airport if airport not in arrivals)
    itinerary = [start]
    while itinerary[-1] in next_airport:
        itinerary.append(next_airport[itinerary[-1]])
    return itinerary
```

**Code connection:** `dict(boarding_passes)` maps each departure to its next stop; the arrivals set identifies which departure can begin the route.

**Checks:** Both supplied routes match, even though the passes are shuffled.

**Cost:** Let E be boarding passes. Expected O(E) time and O(E) auxiliary space; output stores E + 1 airports.

**Common mistake:** Starting with the first boarding pass → input order is shuffled. Find the airport with no incoming flight. Sorting names → does not preserve connections.

**Interview explanation:** Only the first airport has no incoming flight. Each mapping gives its unique next stop, so following links reconstructs the entire guaranteed route. Let E be boarding passes. Expected O(E) time and O(E) auxiliary space; output stores E + 1 airports.

**Check your understanding:** Why does the result have one more airport than boarding passes? Would a single departure-to-arrival mapping handle branching routes?

<details>
<summary>Reasoning and answers</summary>

Each of E flights adds one airport after the starting airport. Branching violates this input contract; one dictionary value would overwrite another departure’s destination.

</details>
