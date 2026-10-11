"""UPI solutions for Week 5, Session 1, Problem Set Version 1.

Problem 3 uses get_all_destinations; Problem 4 uses get_all_destinations_dfs
so both remain callable. Rename the latter to get_all_destinations when
submitting Problem 4 on its own.
"""

# Shared import: deque provides an efficient first-in, first-out queue.
from collections import deque


# ======================================================================
# Problem 1: There and Back — bidirectional_flights
# ======================================================================
# U — Understand: Every directed edge must have its reverse edge.
# P — Plan: Build neighbor sets; check each edge for its reverse.
# I — Implement
def bidirectional_flights(flights):
    neighbors = [set(destinations) for destinations in flights]
    for origin, destinations in enumerate(flights):
        for destination in destinations:
            if origin not in neighbors[destination]:
                return False
    return True


# ======================================================================
# Problem 2: Find Center of Airport — find_center
# ======================================================================
# U — Understand: The input is a valid undirected star graph.
# P — Plan: Return the endpoint shared by the first two edges.
# I — Implement
def find_center(terminals):
    first, second = terminals[0]
    if first in terminals[1]:
        return first
    return second


# ======================================================================
# Problem 3: Finding All Reachable Destinations — get_all_destinations (BFS)
# ======================================================================
# U — Understand: Include start; visit in increasing shortest flight count.
# P — Plan: Queue start; mark on enqueue; process neighbors in supplied order.
# I — Implement
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


# ======================================================================
# Problem 4: Finding All Reachable Destinations II — get_all_destinations_dfs
# ======================================================================
# U — Understand: Include start and return DFS discovery order.
# P — Plan: Mark and append each airport; fully explore each unseen neighbor.
# I — Implement
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


# ======================================================================
# Problem 5: Find Itinerary — find_itinerary
# ======================================================================
# U — Understand: Passes form one acyclic route; each airport is visited once.
# P — Plan: Map departures to arrivals; start where no flight arrives; follow.
# I — Implement
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


# ======================================================================
# Example checks — grouped by problem
# ======================================================================
if __name__ == "__main__":
    # Problem 1: There and Back
    assert bidirectional_flights([[1, 2], [0], [0, 3], [2]]) is True
    assert bidirectional_flights([[1, 2], [], [0], [2]]) is False

    # Problem 2: Find Center of Airport
    assert find_center([[1, 2], [2, 3], [4, 2]]) == 2
    assert find_center([[1, 2], [5, 1], [1, 3], [1, 4]]) == 1

    flights = {
        "Tokyo": ["Sydney"], "Sydney": ["Tokyo", "Beijing"],
        "Beijing": ["Mexico City", "Helsinki"],
        "Helsinki": ["Cairo", "New York"],
        "Cairo": ["Helsinki", "Reykjavik"],
        "Reykjavik": ["Cairo", "New York"],
        "Mexico City": ["Sydney"], "New York": ["Helsinki", "Reykjavik"],
    }
    # Problem 3: Finding All Reachable Destinations (BFS)
    assert get_all_destinations(flights, "Beijing") == [
        "Beijing", "Mexico City", "Helsinki", "Sydney", "Cairo", "New York",
        "Tokyo", "Reykjavik",
    ]
    assert get_all_destinations(flights, "Helsinki") == [
        "Helsinki", "Cairo", "New York", "Reykjavik",
    ]

    # Problem 4: Finding All Reachable Destinations II (DFS)
    dfs_flights = {key: value for key, value in flights.items() if key != "New York"}
    assert get_all_destinations_dfs(dfs_flights, "Beijing") == [
        "Beijing", "Mexico City", "Sydney", "Tokyo", "Helsinki", "Cairo",
        "Reykjavik", "New York",
    ]
    assert get_all_destinations_dfs(dfs_flights, "Helsinki") == [
        "Helsinki", "Cairo", "Reykjavik", "New York",
    ]

    # Problem 5: Find Itinerary
    assert find_itinerary([("JFK", "ATL"), ("SFO", "JFK"),
                           ("ATL", "ORD"), ("LAX", "SFO")]) == [
        "LAX", "SFO", "JFK", "ATL", "ORD",
    ]
    assert find_itinerary([("LAX", "DXB"), ("DFW", "JFK"),
                           ("LHR", "DFW"), ("JFK", "LAX")]) == [
        "LHR", "DFW", "JFK", "LAX", "DXB",
    ]
