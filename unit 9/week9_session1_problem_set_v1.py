"""Unit 9, Session 1, Version 1: Greedy algorithms.

Run this file for example and boundary assertions. Inputs are not mutated.
See the companion Markdown for assumptions, proofs, traces, and complexity.
"""


# Problem 1: Non-overlapping Intervals
# U: Cancel the fewest bookings; touching endpoints do not overlap.
# P / Pseudocode: Sort by finish time; keep compatible bookings, count others.
def erase_overlap_intervals(intervals):
    removed = 0
    previous_end = float("-inf")
    for start, end in sorted(intervals, key=lambda interval: interval[1]):
        if start >= previous_end:
            previous_end = end
        else:
            removed += 1
    return removed


# Problem 2: Gas Station
# U: Return a feasible starting index, or -1 if the trip is impossible.
# P / Pseudocode: Accumulate net fuel; restart after a negative running tank.
def can_complete_circuit(gas, cost):
    if not gas:
        return -1
    total = tank = start = 0
    for index in range(len(gas)):
        difference = gas[index] - cost[index]
        total += difference
        tank += difference
        if tank < 0:
            start = index + 1
            tank = 0
    return start if total >= 0 else -1


# Problem 3: Assign Cookies
# U: Maximize satisfied children, with at most one cookie per child.
# P / Pseudocode: Sort both lists; give each child the smallest fitting cookie.
def find_content_children(g, s):
    children = sorted(g)
    cookies = sorted(s)
    child = 0
    for cookie in cookies:
        if child == len(children):
            break
        if cookie >= children[child]:
            child += 1
    return child


# Problem 4: Jump Game II
# U: Find the fewest jumps; the nonempty input is guaranteed reachable.
# P / Pseudocode: Scan each jump's reachable range; expand to its farthest reach.
def jump(nums):
    jumps = current_end = farthest = 0
    for index in range(len(nums) - 1):
        farthest = max(farthest, index + nums[index])
        if index == current_end:
            jumps += 1
            current_end = farthest
    return jumps


# Problem 5: Partition Labels
# U: Make the most pieces while keeping every letter in only one piece.
# P / Pseudocode: Record last occurrences; close a piece at its required end.
def partition_labels(s):
    last = {letter: index for index, letter in enumerate(s)}
    sizes = []
    start = end = 0
    for index, letter in enumerate(s):
        end = max(end, last[letter])
        if index == end:
            sizes.append(end - start + 1)
            start = index + 1
    return sizes


if __name__ == "__main__":
    assert erase_overlap_intervals([[1, 2], [2, 3], [3, 4], [1, 3]]) == 1
    assert erase_overlap_intervals([[1, 2], [1, 2], [1, 2]]) == 2
    assert erase_overlap_intervals([[1, 2], [2, 3]]) == 0
    assert erase_overlap_intervals([]) == 0
    assert erase_overlap_intervals([[1, 10], [2, 3], [3, 4]]) == 1
    print("Problem 1: Non-overlapping Intervals -- checks passed")

    assert can_complete_circuit([1, 2, 3, 4, 5], [3, 4, 5, 1, 2]) == 3
    assert can_complete_circuit([2, 3, 4], [3, 4, 3]) == -1
    assert can_complete_circuit([1], [1]) == 0
    assert can_complete_circuit([0], [1]) == -1
    assert can_complete_circuit([], []) == -1
    print("Problem 2: Gas Station -- checks passed")

    assert find_content_children([1, 2, 3], [1, 1]) == 1
    assert find_content_children([1, 2], [1, 2, 3]) == 2
    assert find_content_children([], [1]) == 0
    assert find_content_children([1], []) == 0
    assert find_content_children([3, 1, 2], [3, 1]) == 2
    print("Problem 3: Assign Cookies -- checks passed")

    assert jump([2, 3, 1, 1, 4]) == 2
    assert jump([2, 3, 0, 1, 4]) == 2
    assert jump([0]) == 0
    assert jump([1, 1, 1, 1]) == 3
    assert jump([4, 0, 0, 0, 0]) == 1
    print("Problem 4: Jump Game II -- checks passed")

    assert partition_labels("ababcbacadefegdehijhklij") == [9, 7, 8]
    assert partition_labels("eccbbbbdec") == [10]
    assert partition_labels("") == []
    assert partition_labels("abc") == [1, 1, 1]
    assert partition_labels("aaaa") == [4]
    print("Problem 5: Partition Labels -- checks passed")
