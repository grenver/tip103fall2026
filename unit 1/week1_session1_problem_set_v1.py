"""UPI solutions for Problem Set Version 1."""


# Problem 1: Hunny Hunt
# U - Understand
# 1. Should the function return the first matching index when the target appears
#    more than once? Yes.
# 2. What should it return if the target does not appear? -1.
#
# P - Plan
# 2. Look at every item from left to right. Return its index as soon as it
#    matches the target; otherwise return -1 after checking the whole list.
# 3. Pseudocode:
#    FOR each index in items:
#        IF the item at that index equals target:
#            RETURN the index
#    RETURN -1
def linear_search(items, target):
    """Return the first index of target in items, or -1 when absent."""
    for index in range(len(items)):
        if items[index] == target:
            return index
    return -1


# Problem 2: Bouncy, Flouncy, Trouncy, Pouncy
# U - Understand
# 1. What value does tigger begin with? It begins at 1.
# 2. Which operations increase the value? "bouncy" and "flouncy."
#
# P - Plan
# 2. Start at 1 and update the value once for each operation. Add one for an
#    increment operation and subtract one for a decrement operation.
# 3. Pseudocode:
#    SET tigger to 1
#    FOR each operation in operations:
#        IF operation is "bouncy" OR "flouncy":
#            ADD 1 to tigger
#        ELSE:
#            SUBTRACT 1 from tigger
#    RETURN tigger
def final_value_after_operations(operations):
    """Return Tigger's value after performing every operation."""
    tigger = 1
    for operation in operations:
        if operation == "bouncy" or operation == "flouncy":
            tigger += 1
        else:
            tigger -= 1
    return tigger


# Problem 3: T-I-Double Guh-Er II
# U - Understand
# 1. Should uppercase letters be treated like lowercase letters? Yes; removal
#    is case insensitive.
# 2. Are "gg" and "er" removed as two-character substrings? Yes.
#
# P - Plan
# 2. Convert the word to lowercase, then remove t, i, gg, and er in that order.
# 3. Pseudocode:
#    CONVERT word to lowercase
#    REMOVE every "t" from word
#    REMOVE every "i" from word
#    REMOVE every "gg" from word
#    REMOVE every "er" from word
#    RETURN word
def tiggerfy(word):
    """Return word lowercased with Tigger's spelling pieces removed."""
    result = word.lower()
    result = result.replace("t", "")
    result = result.replace("i", "")
    result = result.replace("gg", "")
    result = result.replace("er", "")
    return result


# Problem 4: Non-decreasing Array
# U - Understand
# 1. Does modifying at most one element include modifying no elements? Yes.
# 2. When a pair is out of order, may either number be changed? Yes, as long as
#    the entire array can be non-decreasing with only one modification.
#
# P - Plan
# 2. Scan adjacent pairs. At the first decrease, use one allowed change. Change
#    the earlier value when it can fit before its previous neighbor; otherwise
#    raise the later value. A second decrease means the answer is False.
# 3. Pseudocode:
#    SET changes to 0
#    MAKE a copy of nums
#    FOR each index from 1 through the end of nums:
#        IF current value is less than previous value:
#            ADD 1 to changes
#            IF changes is greater than 1: RETURN False
#            IF there is no value before previous OR current >= value two spots back:
#                SET previous value to current value
#            ELSE:
#                SET current value to previous value
#    RETURN True
def non_decreasing(nums):
    """Return whether nums can be made non-decreasing with at most one change."""
    values = nums[:]
    changes = 0

    for index in range(1, len(values)):
        if values[index] < values[index - 1]:
            changes += 1
            if changes > 1:
                return False

            if index == 1 or values[index] >= values[index - 2]:
                values[index - 1] = values[index]
            else:
                values[index] = values[index - 1]
    return True


# Problem 5: Missing Clues
# U - Understand
# 1. What does each returned inner list represent? The inclusive beginning and
#    end of one consecutive range of missing clue numbers.
# 2. What should be returned when no clues are missing? An empty list.
#
# P - Plan
# 2. Sort the clues and keep track of the next number that should appear. Each
#    gap before a clue is a missing range. Finally, add a range after the last
#    clue if the upper bound has not been reached.
# 3. Pseudocode:
#    SET missing_ranges to an empty list
#    SET next_number to lower
#    FOR each clue in sorted clues:
#        IF clue is greater than next_number:
#            ADD [next_number, clue - 1] to missing_ranges
#        SET next_number to clue + 1
#    IF next_number is less than or equal to upper:
#        ADD [next_number, upper] to missing_ranges
#    RETURN missing_ranges
def find_missing_clues(clues, lower, upper):
    """Return inclusive ranges that cover exactly the missing clue numbers."""
    missing_ranges = []
    next_number = lower

    for clue in sorted(clues):
        if clue > next_number:
            missing_ranges.append([next_number, clue - 1])
        next_number = clue + 1

    if next_number <= upper:
        missing_ranges.append([next_number, upper])
    return missing_ranges


if __name__ == "__main__":
    assert linear_search(["haycorn", "hunny", "haycorn"], "hunny") == 1
    assert linear_search(["bed", "blue jacket"], "hunny") == -1
    assert final_value_after_operations(["trouncy", "flouncy", "flouncy"]) == 2
    assert final_value_after_operations(["bouncy", "bouncy", "flouncy"]) == 4
    assert tiggerfy("Trigger") == "r"
    assert tiggerfy("eggplant") == "eplan"
    assert tiggerfy("Choir") == "chor"
    assert non_decreasing([4, 2, 3]) is True
    assert non_decreasing([4, 2, 1]) is False
    assert find_missing_clues([0, 1, 3, 50, 75], 0, 99) == [
        [2, 2], [4, 49], [51, 74], [76, 99]
    ]
    assert find_missing_clues([-1], -1, -1) == []
