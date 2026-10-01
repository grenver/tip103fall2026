"""UPI solutions for Week 3, Session 2, Problem Set Version 1."""

from collections import deque


# 1. U: Lower complexity goes first. P: Move a front blueprint to the back
# if a simpler blueprint is waiting; otherwise approve it.
def blueprint_approval(blueprints):
    queue = deque(blueprints)
    approval_order = []
    while queue:
        simplest = min(queue)
        while queue[0] != simplest:
            queue.append(queue.popleft())
        approval_order.append(queue.popleft())
    return approval_order


# 2. U: A new floor can sit on the current skyscraper only when it is no taller
# than the previous floor. P: Count every upward change, which starts a new tower.
def build_skyscrapers(floors):
    if not floors:
        return 0
    skyscrapers = 1
    for index in range(1, len(floors)):
        if floors[index] > floors[index - 1]:
            skyscrapers += 1
    return skyscrapers


# 3. U: Area is distance times the shorter boundary. P: Check widest boundaries
# first, then move the shorter one inward.
def max_corridor_area(segments):
    left, right = 0, len(segments) - 1
    best = 0
    while left < right:
        best = max(best, (right - left) * min(segments[left], segments[right]))
        if segments[left] < segments[right]:
            left += 1
        else:
            right -= 1
    return best


# 4. U: Counts of [ and ] are equal. P: Count the greatest unmatched closing-wall
# deficit; one swap fixes two deficits.
def min_swaps(s):
    balance = 0
    lowest_balance = 0
    for wall in s:
        balance += 1 if wall == "[" else -1
        lowest_balance = min(lowest_balance, balance)
    return (-lowest_balance + 1) // 2


# 5. U: Keep letters and remove only parentheses that cannot be matched. P: Mark
# unmatched right parentheses on a forward pass, then unmatched left ones.
def make_balanced_room(s):
    remove = set()
    open_walls = []
    for index, character in enumerate(s):
        if character == "(":
            open_walls.append(index)
        elif character == ")":
            if open_walls:
                open_walls.pop()
            else:
                remove.add(index)
    remove.update(open_walls)
    return "".join(character for index, character in enumerate(s) if index not in remove)


if __name__ == "__main__":
    assert blueprint_approval([3, 5, 2, 1, 4]) == [1, 2, 3, 4, 5]
    assert blueprint_approval([7, 4, 6, 2, 5]) == [2, 4, 5, 6, 7]
    assert build_skyscrapers([10, 5, 8, 3, 7, 2, 9]) == 4
    assert build_skyscrapers([7, 3, 7, 3, 5, 1, 6]) == 4
    assert build_skyscrapers([8, 6, 4, 7, 5, 3, 2]) == 2
    assert max_corridor_area([1, 8, 6, 2, 5, 4, 8, 3, 7]) == 49
    assert max_corridor_area([1, 1]) == 1
    assert min_swaps("][][") == 1
    assert min_swaps("]]][[[") == 2
    assert min_swaps("[]") == 0
    assert make_balanced_room("art(t(d)e)sign)") == "art(t(d)e)sign"
    assert make_balanced_room("d)e(s)ign") == "de(s)ign"
    assert make_balanced_room("))((") == ""
