"""UPI solutions for Week 5, Session 2, Problem Set Version 1."""

# Shared import: FIFO queues for Problems 3 and 4.
from collections import deque


# ======================================================================
# Problem 1: Get Flight Cost — calculate_cost
# ======================================================================
# U — Understand: Weighted directed flights; return the cost of any path from start to dest, or -1 if unreachable.
# P — Plan: Recursively explore unseen airports while carrying the cost of the current path; return on reaching dest.
# I — Implement
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


# ======================================================================
# Problem 2: Expanding Flight Offerings — min_flights_to_expand
# ======================================================================
# U — Understand: Flights are bidirectional; return the fewest edges needed to connect all airports.
# P — Plan: Count connected components with iterative DFS; return components minus one.
# I — Implement
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


# ======================================================================
# Problem 3: Get Flight Itinerary — get_itinerary
# ======================================================================
# U — Understand: Return any source-to-destination path, including its endpoints.
# P — Plan: Use a FIFO BFS queue; record each discovered airport’s parent; reconstruct backward at the destination.
# I — Implement
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


# ======================================================================
# Problem 4: Pilot Training — can_complete_flight_training
# ======================================================================
# U — Understand: Return whether every course can be completed given prerequisite pairs [course, prerequisite].
# P — Plan: Queue courses with no remaining prerequisites; complete them and release dependent courses.
# I — Implement
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


# ======================================================================
# Problem 5: Reorient Flight Routes — min_reorient_flight_routes
# ======================================================================
# U — Understand: The underlying network is a tree; reverse the fewest edges so every airport reaches 0.
# P — Plan: Traverse outward from 0 in the undirected tree; count original edges pointing away from 0.
# I — Implement
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


# ======================================================================
# Example checks — grouped by problem
# ======================================================================
if __name__ == "__main__":
    weighted_flights = {
        "LAX": [("SFO", 50)],
        "SFO": [("LAX", 50), ("ORD", 100), ("ERW", 210)],
        "ERW": [("SFO", 210), ("ORD", 300)],
        "ORD": [("ERW", 300), ("SFO", 100), ("MIA", 400)],
        "MIA": [("ORD", 400)],
    }
    # Problem 1: Get Flight Cost
    assert calculate_cost(weighted_flights, "LAX", "MIA") in (550, 960)
    assert calculate_cost(weighted_flights, "LAX", "JFK") == -1
    assert calculate_cost(weighted_flights, "LAX", "LAX") == 0
    assert calculate_cost({"A": [("B", 0)]}, "A", "B") == 0

    # Problem 2: Expanding Flight Offerings
    assert min_flights_to_expand({
        "JFK": ["LAX", "SFO"], "LAX": ["JFK", "SFO"],
        "SFO": ["JFK", "LAX"], "ORD": ["ATL"], "ATL": ["ORD"],
    }) == 1
    assert min_flights_to_expand({"A": [], "B": [], "C": []}) == 2
    assert min_flights_to_expand({"A": []}) == 0

    # Problem 3: Get Flight Itinerary
    flights = {airport: [neighbor for neighbor, _ in routes]
               for airport, routes in weighted_flights.items()}
    assert get_itinerary(flights, "LAX", "MIA") == ["LAX", "SFO", "ORD", "MIA"]
    assert get_itinerary(flights, "LAX", "JFK") == []
    assert get_itinerary(flights, "LAX", "LAX") == ["LAX"]

    # Problem 4: Pilot Training — numeric contract and named examples
    assert can_complete_flight_training(2, [[1, 0]]) is True
    assert can_complete_flight_training(2, [[1, 0], [0, 1]]) is False
    assert can_complete_flight_training(4, [[1, 0]]) is True
    assert can_complete_flight_training(1, [[0, 0]]) is False
    assert can_complete_flight_training(2, [
        ["Advanced Maneuvers", "Basic Navigation"],
    ]) is True
    assert can_complete_flight_training(2, [
        ["Advanced Maneuvers", "Basic Navigation"],
        ["Basic Navigation", "Advanced Maneuvers"],
    ]) is False

    # Problem 5: Reorient Flight Routes
    assert min_reorient_flight_routes(6, [
        [0, 1], [1, 3], [2, 3], [4, 0], [4, 5],
    ]) == 3
    assert min_reorient_flight_routes(3, [[1, 0], [2, 1]]) == 0
    assert min_reorient_flight_routes(3, [[0, 1], [1, 2]]) == 2
    assert min_reorient_flight_routes(1, []) == 0
