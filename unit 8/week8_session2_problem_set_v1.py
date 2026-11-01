"""Unit 8, Session 2, Version 1: backtracking.

Each recursive branch chooses, explores, then undoes its temporary choice.
Run this file for labeled checks. Input lists are not changed.
"""


# ======================================================================
# Problem 1: Subsets -- subsets
# U -- Understand: Distinct integers; include the empty subset exactly once.
# P -- Plan: Save each path, then extend it using only later input indices.
# I -- Implement
def subsets(nums):
    result = []
    path = []

    def search(start):
        result.append(path.copy())
        for index in range(start, len(nums)):
            path.append(nums[index])
            search(index + 1)
            path.pop()

    search(0)
    return result


# ======================================================================
# Problem 2: Permutations -- permute
# U -- Understand: Every ordering must contain each distinct input item once.
# P -- Plan: At each position choose any item not already used in this path.
# I -- Implement
def permute(nums):
    result = []
    path = []
    used = [False] * len(nums)

    def search():
        if len(path) == len(nums):
            result.append(path.copy())
            return
        for index in range(len(nums)):
            if not used[index]:
                used[index] = True
                path.append(nums[index])
                search()
                path.pop()
                used[index] = False

    search()
    return result


# ======================================================================
# Problem 3: Combination Sum -- combination_sum
# U -- Understand: Distinct positive candidates; unlimited reuse; order irrelevant.
# P -- Plan: Keep indices nondecreasing; recurse at the same index for reuse.
# I -- Implement
def combination_sum(candidates, target):
    result = []
    path = []

    def search(start, remaining):
        if remaining == 0:
            result.append(path.copy())
            return
        for index in range(start, len(candidates)):
            value = candidates[index]
            if value <= remaining:
                path.append(value)
                search(index, remaining - value)
                path.pop()

    search(0, target)
    return result


# ======================================================================
# Problem 4: Generate Parentheses -- generate_parentheses
# U -- Understand: Generate balanced strings using exactly n pairs, n >= 0.
# P -- Plan: Add '(' if available; add ')' only if an unmatched '(' exists.
# I -- Implement
def generate_parentheses(n):
    result = []
    path = []

    def search(opened, closed):
        if len(path) == 2 * n:
            result.append("".join(path))
            return
        if opened < n:
            path.append("(")
            search(opened + 1, closed)
            path.pop()
        if closed < opened:
            path.append(")")
            search(opened, closed + 1)
            path.pop()

    search(0, 0)
    return result


# ======================================================================
# Problem 5: Letter Combinations of a Phone Number -- letter_combinations
# U -- Understand: One letter per digit from 2-9; empty digits returns [].
# P -- Plan: At position i, explore each letter mapped to digits[i].
# I -- Implement
def letter_combinations(digits):
    if not digits:
        return []
    keypad = {"2": "abc", "3": "def", "4": "ghi", "5": "jkl",
              "6": "mno", "7": "pqrs", "8": "tuv", "9": "wxyz"}
    result = []
    path = []

    def search(index):
        if index == len(digits):
            result.append("".join(path))
            return
        for letter in keypad[digits[index]]:
            path.append(letter)
            search(index + 1)
            path.pop()

    search(0)
    return result


# Shared example and boundary checks -- run only when executing this file.
if __name__ == "__main__":
    # Problem 1: Subsets
    assert subsets([1, 2, 3]) == [[], [1], [1, 2], [1, 2, 3], [1, 3], [2], [2, 3], [3]]
    assert subsets([]) == [[]]
    assert subsets([0]) == [[], [0]]
    print("Problem 1: Subsets -- checks passed")

    # Problem 2: Permutations
    assert permute([1, 2, 3]) == [[1, 2, 3], [1, 3, 2], [2, 1, 3],
                                 [2, 3, 1], [3, 1, 2], [3, 2, 1]]
    assert permute([]) == [[]]
    assert permute([5]) == [[5]]
    print("Problem 2: Permutations -- checks passed")

    # Problem 3: Combination Sum
    assert combination_sum([2, 3, 6, 7], 7) == [[2, 2, 3], [7]]
    assert combination_sum([2], 3) == []
    assert combination_sum([2], 0) == [[]]
    assert combination_sum([], 4) == []
    assert combination_sum([3, 2], 7) == [[3, 2, 2]]
    print("Problem 3: Combination Sum -- checks passed")

    # Problem 4: Generate Parentheses
    assert generate_parentheses(3) == ["((()))", "(()())", "(())()", "()(())", "()()()"]
    assert generate_parentheses(0) == [""]
    assert generate_parentheses(1) == ["()"]
    print("Problem 4: Generate Parentheses -- checks passed")

    # Problem 5: Letter Combinations of a Phone Number
    assert letter_combinations("23") == ["ad", "ae", "af", "bd", "be", "bf", "cd", "ce", "cf"]
    assert letter_combinations("") == []
    assert letter_combinations("7") == ["p", "q", "r", "s"]
    assert len(letter_combinations("79")) == 16
    print("Problem 5: Letter Combinations of a Phone Number -- checks passed")
