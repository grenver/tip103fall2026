"""Unit 7, Session 2, Version 1: binary search.

Problem 1 keeps check_stock; Problem 2 uses check_stock_recursive so neither
implementation is overwritten. For a Problem 2 submission, rename it to
check_stock. Both use index bounds rather than making sliced search lists.
"""


# ======================================================================
# Problem 1: Find Millenium Falcon Part I -- check_stock (iterative)
# U -- Understand: Return a Boolean membership result for sorted integer IDs.
# P -- Plan: Check the midpoint, discard one half, stop when bounds cross.
# I -- Implement
def check_stock(inventory, part_id):
    left, right = 0, len(inventory) - 1
    while left <= right:
        middle = (left + right) // 2
        if inventory[middle] == part_id:
            return True
        if inventory[middle] < part_id:
            left = middle + 1
        else:
            right = middle - 1
    return False


# ======================================================================
# Problem 2: Find Millenium Falcon Part II -- check_stock_recursive
# U -- Understand: Same contract, now using recursion rather than a loop.
# P -- Plan: Pass shrinking index bounds; an empty range returns False.
# I -- Implement
def check_stock_recursive(inventory, part_id):
    def search(left, right):
        if left > right:
            return False
        middle = (left + right) // 2
        if inventory[middle] == part_id:
            return True
        if inventory[middle] < part_id:
            return search(middle + 1, right)
        return search(left, middle - 1)

    return search(0, len(inventory) - 1)


# ======================================================================
# Problem 3: Find First and Last Frequency Positions -- find_frequency_positions
# U -- Understand: Find both ends of a repeated value in logarithmic time.
# P -- Plan: Search for first >= target and first > target using half-open bounds.
# I -- Implement
def find_frequency_positions(transmissions, target_code):
    def boundary(strict):
        left, right = 0, len(transmissions)
        while left < right:
            middle = (left + right) // 2
            if transmissions[middle] < target_code or (
                strict and transmissions[middle] == target_code
            ):
                left = middle + 1
            else:
                right = middle
        return left

    first = boundary(False)
    if first == len(transmissions) or transmissions[first] != target_code:
        return (-1, -1)
    return (first, boundary(True) - 1)


# ======================================================================
# Problem 4: Smallest Letter Greater Than Target -- next_greatest_letter
# U -- Understand: Strictly greater; wrap to the first letter when needed.
# P -- Plan: Find first > target; index n means use index 0.
# I -- Implement
def next_greatest_letter(letters, target):
    left, right = 0, len(letters)
    while left < right:
        middle = (left + right) // 2
        if letters[middle] <= target:
            left = middle + 1
        else:
            right = middle
    return letters[left % len(letters)]


# ======================================================================
# Problem 5: Find K Closest Planets -- find_closest_planets
# U -- Understand: Sorted input/output; ties favor smaller distances; 0 <= k <= n.
# P -- Plan: Binary-search starts of length-k windows, then copy the best window.
# I -- Implement
def find_closest_planets(planets, target_distance, k):
    if k == 0:
        return []
    left, right = 0, len(planets) - k
    while left < right:
        middle = (left + right) // 2
        if target_distance - planets[middle] > planets[middle + k] - target_distance:
            left = middle + 1
        else:
            right = middle  # Equality keeps the smaller-valued window.
    return planets[left:left + k]


# Example and boundary checks -- one labeled block per problem.
if __name__ == '__main__':
    # Problem 1: Find Millenium Falcon Part I
    assert check_stock([1, 2, 5, 12, 20], 20) is True
    assert check_stock([1, 2, 5, 12, 20], 100) is False
    assert check_stock([], 1) is False
    assert check_stock([1], 1) is True
    assert check_stock([1, 1, 2], 1) is True
    print('Problem 1: Find Millenium Falcon Part I - passed')

    # Problem 2: Find Millenium Falcon Part II
    assert check_stock_recursive([1, 2, 5, 12, 20], 20) is True
    assert check_stock_recursive([1, 2, 5, 12, 20], 100) is False
    assert check_stock_recursive([], 1) is False
    assert check_stock_recursive([1], 0) is False
    assert check_stock_recursive([1, 1, 2], 1) is True
    print('Problem 2: Find Millenium Falcon Part II - passed')

    # Problem 3: Find First and Last Frequency Positions
    assert find_frequency_positions([5, 7, 7, 8, 8, 10], 8) == (3, 4)
    assert find_frequency_positions([5, 7, 7, 8, 8, 10], 6) == (-1, -1)
    assert find_frequency_positions([], 0) == (-1, -1)
    assert find_frequency_positions([8, 8, 8], 8) == (0, 2)
    assert find_frequency_positions([8], 8) == (0, 0)
    print('Problem 3: Find First and Last Frequency Positions - passed')

    # Problem 4: Smallest Letter Greater Than Target
    letters = ['a', 'a', 'b', 'c', 'c', 'c', 'e', 'h', 'w']
    assert next_greatest_letter(letters, 'a') == 'b'
    assert next_greatest_letter(letters, 'd') == 'e'
    assert next_greatest_letter(letters, 'y') == 'a'
    assert next_greatest_letter(letters, 'w') == 'a'
    assert next_greatest_letter(['c', 'f'], 'a') == 'c'
    print('Problem 4: Smallest Letter Greater Than Target - passed')

    # Problem 5: Find K Closest Planets
    assert find_closest_planets([100, 200, 300, 400, 500], 350, 3) == [200, 300, 400]
    assert find_closest_planets([10, 20, 30, 40, 50], 25, 2) == [20, 30]
    assert find_closest_planets([1, 2, 3, 4], 2.5, 1) == [2]
    assert find_closest_planets([1, 2, 3], -10, 2) == [1, 2]
    assert find_closest_planets([1, 2, 3], 10, 2) == [2, 3]
    assert find_closest_planets([1, 1, 2, 2], 2, 2) == [2, 2]
    assert find_closest_planets([1, 2], 1, 2) == [1, 2]
    assert find_closest_planets([], 0, 0) == []
    print('Problem 5: Find K Closest Planets - passed')
