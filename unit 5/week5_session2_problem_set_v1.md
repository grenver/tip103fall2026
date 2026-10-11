# Week 5 — Session 2 — Problem Set Version 1

## Problem index and concept map

| Problem | Callable | Main concept | Prerequisite | Explain to a student |
| --- | --- | --- | --- | --- |
| [Problem 1: Get Flight Cost](#problem-1-get-flight-cost) | `calculate_cost` | DFS carrying a path cost | Recursion, sets, weighted edges | Why any path cost is enough |
| [Problem 2: Expanding Flight Offerings](#problem-2-expanding-flight-offerings) | `min_flights_to_expand` | Count connected components | DFS and undirected reachability | Why k groups need k − 1 edges |
| [Problem 3: Get Flight Itinerary](#problem-3-get-flight-itinerary) | `get_itinerary` | BFS and parent reconstruction | FIFO queues and dictionaries | Why traversal order is not a path |
| [Problem 4: Pilot Training](#problem-4-pilot-training) | `can_complete_flight_training` | Topological processing with a queue | Indegree and prerequisite edges | How prerequisites release a course |
| [Problem 5: Reorient Flight Routes](#problem-5-reorient-flight-routes) | `min_reorient_flight_routes` | Direction flags on a rooted tree | Tree traversal and edge direction | Why unique paths force edge directions |

Solutions are visible for review. Each problem follows Understand, Plan, Implement; Python banners and example checks use the same labels.

## Problem 1: Get Flight Cost

**Callable:** `calculate_cost` · **Learning goal / concept:** DFS carrying a path cost.

### U — Understand

Weighted directed flights; return the cost of any path from start to dest, or -1 if unreachable.

**Recognition clue:** “Any” path cost is accepted, and the hint asks for DFS. There is no cheapest-path requirement.

**Prompt notes / assumptions:** Zero flights are needed when start equals dest, so return 0. A destination missing as a dictionary key has no outgoing flights. Internally, None signals failure so a valid zero cost is not mistaken for failure.

### P — Plan

Recursively explore unseen airports while carrying the cost of the current path; return on reaching dest.

**Trace:** LAX(0) → SFO(50) → ORD(150) → ERW(450). ERW has no unseen exit, so that branch returns. ORD then explores MIA(550). The ERW branch’s cost does not leak into MIA’s cost.

**Why it works:** Each recursive call carries the sum for the actual route used to reach that airport. Visiting an airport once is sufficient for reachability because its outgoing possibilities do not depend on the price accumulated. DFS exhausts reachable airports or returns a valid route cost.

### I — Implement

```python
def calculate_cost(flights, start, dest):
    visited = set()

    def search(airport, total):
        if airport == dest:
            return total
        visited.add(airport)
        for neighbor, price in flights.get(airport, []):
            if neighbor not in visited:
                result = search(neighbor, total + price)
                if result is not None:
                    return result
        return None

    result = search(start, 0)
    return -1 if result is None else result
```

**Code connection:** `total + price` creates the cost for one child’s route. `result is not None` accepts a result of zero. The public function translates internal failure into the required -1.

**Checks:** The example DFS returns 550 (960 is also allowed). Unreachable JFK returns -1; start-to-itself and a zero-price flight return 0.

**Cost:** Let Vᵣ be reachable airports and Eᵣ their outgoing flights. Expected O(Vᵣ + Eᵣ) time and O(Vᵣ) auxiliary space for visited and recursion. The result is a scalar.

**Common mistakes:** Using BFS to minimize ticket cost → number of flights does not measure price. Follow the required DFS and return any cost. Treating 0 as failure → rejects free paths; use None internally.

**Interview explanation:** Recursively explore unseen airports while carrying the cost of the current path; return on reaching dest. Each returned total belongs to an actual path. Expected O(Vᵣ + Eᵣ) time and O(Vᵣ) space.

**Check your understanding:** What is returned for start == dest? How would the goal change if the cheapest ticket cost were required?

<details>
<summary>Reasoning and answers</summary>

0: the empty route has no cost. Cheapest cost requires optimizing weights, such as Dijkstra’s algorithm when weights are nonnegative; plain DFS does not guarantee that.

</details>

## Problem 2: Expanding Flight Offerings

**Callable:** `min_flights_to_expand` · **Learning goal / concept:** Count connected components.

### U — Understand

Flights are bidirectional; return the fewest edges needed to connect all airports.

**Recognition clue:** Bidirectional flights group airports into connected components; one new edge can join two groups.

**Prompt notes / assumptions:** Assume the dictionary includes every airport as a key and represents reverse routes as stated. Each added edge is a bidirectional connection, matching the prompt’s graph model. The empty-graph extension returns 0.

### P — Plan

Count connected components with iterative DFS; return components minus one.

**Trace:** DFS from JFK visits JFK, LAX, SFO: component 1. DFS from ORD visits ORD, ATL: component 2. Add one edge between the groups.

**Why it works:** With k components, at least k − 1 edges are needed: each edge reduces the number of components by at most one. Connecting one component to each of the others achieves that bound.

### I — Implement

```python
def min_flights_to_expand(flights):
    visited = set()
    components = 0
    for airport in flights:
        if airport in visited:
            continue
        components += 1
        stack = [airport]
        visited.add(airport)
        while stack:
            current = stack.pop()
            for neighbor in flights.get(current, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    stack.append(neighbor)
    return max(0, components - 1)
```

**Code connection:** `stack.pop()` explores depth first; marking neighbors when pushed prevents repeated work. A new DFS starts only at an unseen airport.

**Checks:** The supplied two groups require 1 edge. Three isolated airports require 2; one airport requires 0.

**Cost:** Let V be airports and E adjacency entries. Expected O(V + E) time and O(V) auxiliary space for visited and the stack.

**Common mistakes:** Counting isolated airports only → misses disconnected multi-airport groups. Count whole components. Returning k → adds one edge too many; use k − 1 for a nonempty graph.

**Interview explanation:** Count connected components with iterative DFS; return components minus one. One bridge merges two components, giving the k − 1 minimum. Expected O(V + E) time and O(V) space.

**Check your understanding:** How many edges join four disconnected groups? What if flights are one-way?

<details>
<summary>Reasoning and answers</summary>

Three: each connection merges two groups. One-way graphs require reasoning about directed reachability; undirected component count alone is insufficient.

</details>

## Problem 3: Get Flight Itinerary

**Callable:** `get_itinerary` · **Learning goal / concept:** BFS and parent reconstruction.

### U — Understand

Return any source-to-destination path, including its endpoints.

**Recognition clue:** The path-reconstruction hint suggests retaining the airport from which each node was discovered.

**Prompt notes / assumptions:** The prompt does not specify an unreachable result; this solution assumes []. When source equals destination, return [source]. BFS also finds a route with the fewest flights, though that is not required.

### P — Plan

Use a FIFO BFS queue; record each discovered airport’s parent; reconstruct backward at the destination.

**Trace:** BFS records parent[SFO] = LAX, parent[ORD] = SFO, and parent[MIA] = ORD. Following parents gives MIA → ORD → SFO → LAX; reversing gives the itinerary.

**Why it works:** Each parent link records a real flight from an already reachable airport. Following those links reaches the source, and reversing them produces a valid forward path.

### I — Implement

```python
from collections import deque

def get_itinerary(flights, source, destination):
    queue = deque([source])
    parent = {source: None}
    while queue:
        airport = queue.popleft()
        if airport == destination:
            path = []
            current = destination
            while current is not None:
                path.append(current)
                current = parent[current]
            path.reverse()
            return path
        for neighbor in flights.get(airport, []):
            if neighbor not in parent:
                parent[neighbor] = airport
                queue.append(neighbor)
    return []
```

**Code connection:** `popleft()` removes the oldest queued airport. The parent dictionary doubles as the visited collection. `path.reverse()` changes the reconstructed list in place.

**Checks:** The example returns [LAX, SFO, ORD, MIA]. Unreachable JFK returns the documented []; identical endpoints return [LAX].

**Cost:** Let Vᵣ be reachable airports, Eᵣ their outgoing flights, and L the returned path length. Expected O(Vᵣ + Eᵣ) search time plus O(L) reconstruction; O(Vᵣ) auxiliary space and O(L) output space.

**Common mistakes:** Returning BFS visitation order → includes airports outside the final route. Follow parent links. Copying the full path into every queue entry → avoidable memory and copying; store one parent per airport.

**Interview explanation:** Use a FIFO BFS queue; record each discovered airport’s parent; reconstruct backward at the destination. Each parent records a real edge, so backtracking reconstructs the route. Expected O(Vᵣ + Eᵣ) time and O(Vᵣ) working space.

**Check your understanding:** Why reverse the reconstructed list? How could you return only the number of flights?

<details>
<summary>Reasoning and answers</summary>

Parents lead destination → source, opposite travel order. Count parent links instead of storing airports, or return len(path) − 1 after reconstruction.

</details>

## Problem 4: Pilot Training

**Callable:** `can_complete_flight_training` · **Learning goal / concept:** Topological processing with a queue.

### U — Understand

Return whether every course can be completed given prerequisite pairs [course, prerequisite].

**Recognition clue:** Courses can start only when their prerequisites are finished; a directed cycle prevents completion.

**Prompt notes / assumptions:** The stated contract labels courses 0 through num_courses − 1, but the examples use names. The implementation supports both: integer input includes all numeric courses; named input tracks names in the pairs, assuming any unnamed courses are isolated and the number of distinct names does not exceed num_courses. Labels are consistently numeric or named, not mixed.

### P — Plan

Queue courses with no remaining prerequisites; complete them and release dependent courses.

**Trace:** For [1, 0], remaining prerequisites are {0: 0, 1: 1}. Queue [0]; completing 0 makes course 1 ready. For [1, 0] and [0, 1], neither course is ready and the queue starts empty.

**Why it works:** Only ready courses enter the queue. If all courses are processed, every prerequisite was satisfied. Otherwise, the remaining finite dependency graph has a cycle preventing any further ready course.

### I — Implement

```python
from collections import deque

def can_complete_flight_training(num_courses, flight_prerequisites):
    # Named examples omit isolated course names; they cannot create a cycle.
    named_courses = any(isinstance(course, str)
                        for pair in flight_prerequisites for course in pair)
    courses = ({course for pair in flight_prerequisites for course in pair}
               if named_courses else set(range(num_courses)))
    dependents = {course: [] for course in courses}
    remaining = {course: 0 for course in courses}
    for course, prerequisite in flight_prerequisites:
        dependents[prerequisite].append(course)
        remaining[course] += 1
    queue = deque(course for course in courses if remaining[course] == 0)
    completed = 0
    while queue:
        course = queue.popleft()
        completed += 1
        for dependent in dependents[course]:
            remaining[dependent] -= 1
            if remaining[dependent] == 0:
                queue.append(dependent)
    return completed == len(courses)
```

**Code connection:** An edge goes from prerequisite to dependent. `remaining` is indegree: the number of prerequisite entries still outstanding. Decrementing it after completing a prerequisite releases a course only when the count reaches zero.

**Checks:** Both supplied named examples return True and False. Numeric equivalents, isolated courses, and self-dependency are also checked.

**Cost:** Let C = num_courses and P be prerequisite pairs. Expected O(C + P) time and O(C + P) auxiliary space; each course and dependency is processed at most once. For named examples, represented courses are at most C.

**Common mistakes:** Reversing [course, prerequisite] → models dependencies backward. Build prerequisite → course. Treating any visited node as a cycle in ordinary DFS → shared prerequisites are not necessarily cycles; the queue method checks whether all courses can finish.

**Interview explanation:** Queue courses with no remaining prerequisites; complete them and release dependent courses. Unprocessed courses are blocked by a cycle. Expected O(C + P) time and space.

**Check your understanding:** Can a course depend on itself? How would you also return a valid course order?

<details>
<summary>Reasoning and answers</summary>

A self-dependency is a cycle, so completion is impossible. Append each dequeued course to a list; return that list if all courses complete.

</details>

## Problem 5: Reorient Flight Routes

**Callable:** `min_reorient_flight_routes` · **Learning goal / concept:** Direction flags on a rooted tree.

### U — Understand

The underlying network is a tree; reverse the fewest edges so every airport reaches 0.

**Recognition clue:** The tree guarantee gives a unique path from every airport to 0, so each edge’s necessary direction is fixed.

**Prompt notes / assumptions:** The pasted explanation is truncated and names the wrong reversals. The correct reversals are [0, 1], [1, 3], [4, 5]; the answer remains 3. The input guarantees a tree and n ≥ 1, allowing a parent check instead of a visited set.

### P — Plan

Traverse outward from 0 in the undirected tree; count original edges pointing away from 0.

**Trace:** Root the tree at 0. Outward edges 0 → 1, 1 → 3, and 4 → 5 each need reversal. Edges 2 → 3 and 4 → 0 already point toward the root along their unique paths.

**Why it works:** On a tree, each airport has one route to 0. Every parent-child edge must point from child to parent; an edge facing the other way must be reversed. Counting precisely those edges is therefore minimal.

### I — Implement

```python
def min_reorient_flight_routes(n, connections):
    neighbors = [[] for _ in range(n)]
    for origin, destination in connections:
        neighbors[origin].append((destination, 1))
        neighbors[destination].append((origin, 0))
    reversals = 0
    stack = [(0, -1)]
    while stack:
        airport, parent = stack.pop()
        for neighbor, needs_reversal in neighbors[airport]:
            if neighbor != parent:
                reversals += needs_reversal
                stack.append((neighbor, airport))
    return reversals
```

**Code connection:** For original a → b, the traversal entry from a to b carries 1 (reverse if this goes outward), and b to a carries 0. The parent check skips the edge just used to arrive.

**Checks:** The supplied tree returns 3. An already inward chain returns 0; an outward chain of two edges returns 2; one airport returns 0.

**Cost:** Let n be airports. The tree has n − 1 edges, stored in both directions for traversal. O(n) time and O(n) auxiliary space for adjacency lists and the stack.

**Common mistakes:** Counting all original outgoing edges → direction is relative to the tree rooted at 0, not airport numbering. Removing the parent check → revisits both directions indefinitely.

**Interview explanation:** Traverse outward from 0 in the undirected tree; count original edges pointing away from 0. The unique route to the root forces each edge toward its parent. O(n) time and space.

**Check your understanding:** How many reversals does 2 → 1 → 0 need? Why can this argument fail if the network contains cycles?

<details>
<summary>Reasoning and answers</summary>

Zero: both edges already lead toward 0. Cycles provide alternative paths, so an outward edge need not be reversed to give every airport a route to the hub.

</details>
