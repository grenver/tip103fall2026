"""Unit 8, Session 1, Version 1: Avatar dynamic programming.

Run this file to execute the labeled example and boundary checks.
Inputs follow the assumptions documented in the companion Markdown guide.
Functions return answers without changing their input lists.
"""


# ======================================================================
# Problem 1: Spirit World Wisdom Pyramid -- wisdom_pyramid
# U -- Understand: Return row wisdomLevel of Pascal's triangle, starting at 0.
# P -- Plan: Build each row from the previous row; both outside values are 1.
# I -- Implement
def wisdom_pyramid(wisdomLevel):
    row = [1]
    for level in range(1, wisdomLevel + 1):
        next_row = [1] * (level + 1)
        for index in range(1, level):
            next_row[index] = row[index - 1] + row[index]
        row = next_row
    return row


# ======================================================================
# Problem 2: Aang and Zuko's Elemental Duel -- aang_wins
# U -- Understand: For positive n, a player without a proper-divisor move loses.
# P -- Plan: A state wins if any legal move leaves a losing smaller state.
# I -- Implement
def aang_wins(n):
    wins = [False] * (n + 1)
    for strength in range(2, n + 1):
        divisor = 1
        while divisor * divisor <= strength:
            if strength % divisor == 0:
                partner = strength // divisor
                if not wins[strength - divisor]:
                    wins[strength] = True
                    break
                if partner < strength and not wins[strength - partner]:
                    wins[strength] = True
                    break
            divisor += 1
    return wins[n]


# ======================================================================
# Problem 3: Iroh's Tea Brewing -- strongest_tea
# U -- Understand: Return the maximum product of a nonempty contiguous subarray.
# P -- Plan: Track the largest AND smallest products ending at each position.
# I -- Implement
def strongest_tea(ingredients):
    largest = smallest = best = ingredients[0]
    for index in range(1, len(ingredients)):
        value = ingredients[index]
        # Both products must use the previous position's state.
        extend_largest = largest * value
        extend_smallest = smallest * value
        largest = max(value, extend_largest, extend_smallest)
        smallest = min(value, extend_largest, extend_smallest)
        best = max(best, largest)
    return best


# ======================================================================
# Problem 4: Toph and Katara's Training Synchronization -- training_synchronization
# U -- Understand: Return a common subsequence's maximum length, preserving order.
# P -- Plan: Fill a table of LCS lengths for every pair of string prefixes.
# I -- Implement
def training_synchronization(katara_moves, toph_moves):
    rows, columns = len(katara_moves), len(toph_moves)
    dp = [[0] * (columns + 1) for _ in range(rows + 1)]
    for row in range(1, rows + 1):
        for column in range(1, columns + 1):
            if katara_moves[row - 1] == toph_moves[column - 1]:
                dp[row][column] = dp[row - 1][column - 1] + 1
            else:
                dp[row][column] = max(dp[row - 1][column], dp[row][column - 1])
    return dp[rows][columns]


# ======================================================================
# Problem 5: Aang's Airbending Journey -- aang_journey
# U -- Understand: Nonempty platforms contains nonnegative maximum jump lengths.
# P -- Plan: Mark a position reachable if a reachable earlier position can jump to it.
# I -- Implement
def aang_journey(platforms):
    reachable = [False] * len(platforms)
    reachable[0] = True
    for destination in range(1, len(platforms)):
        for start in range(destination):
            if reachable[start] and start + platforms[start] >= destination:
                reachable[destination] = True
                break
    return reachable[-1]


# Shared example and boundary checks -- run only when executing this file.
if __name__ == "__main__":
    # Problem 1: Spirit World Wisdom Pyramid
    assert wisdom_pyramid(3) == [1, 3, 3, 1]
    assert wisdom_pyramid(0) == [1]
    assert wisdom_pyramid(5) == [1, 5, 10, 10, 5, 1]
    assert wisdom_pyramid(1) == [1, 1]
    print("Problem 1: Spirit World Wisdom Pyramid -- checks passed")

    # Problem 2: Aang and Zuko's Elemental Duel
    assert aang_wins(2) is True
    assert aang_wins(3) is False
    assert aang_wins(1) is False
    assert aang_wins(4) is True
    assert aang_wins(9) is False
    print("Problem 2: Aang and Zuko's Elemental Duel -- checks passed")

    # Problem 3: Iroh's Tea Brewing
    assert strongest_tea([1, 2, -3, 4]) == 4
    assert strongest_tea([-2, -1]) == 2
    assert strongest_tea([-2, 3, -4]) == 24
    assert strongest_tea([-2, 0, -1]) == 0
    assert strongest_tea([-3]) == -3
    print("Problem 3: Iroh's Tea Brewing -- checks passed")

    # Problem 4: Toph and Katara's Training Synchronization
    assert training_synchronization("waterbend", "earthbend") == 6
    assert training_synchronization("bend", "bend") == 4
    assert training_synchronization("fire", "air") == 2
    assert training_synchronization("", "bend") == 0
    assert training_synchronization("abc", "xyz") == 0
    assert training_synchronization("aaa", "aa") == 2
    print("Problem 4: Toph and Katara's Training Synchronization -- checks passed")

    # Problem 5: Aang's Airbending Journey
    assert aang_journey([2, 3, 1, 1, 4]) is True
    assert aang_journey([3, 2, 1, 0, 4]) is False
    assert aang_journey([0]) is True
    assert aang_journey([0, 1]) is False
    assert aang_journey([2, 0, 0]) is True
    print("Problem 5: Aang's Airbending Journey -- checks passed")
