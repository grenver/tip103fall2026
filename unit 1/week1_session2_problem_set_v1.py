"""UPI solutions for Week 1, Session 2, Problem Set Version 1."""


# Problem 1: Transpose Matrix
# U - Understand
# 1. How do the dimensions change? An r-by-c matrix becomes a c-by-r matrix.
# 2. Where does matrix[row][column] go? It becomes result[column][row].
#
# P - Plan
# 2. Create one new row for each original column. For every row and column in
#    the original matrix, add its value to the corresponding flipped position.
# 3. Pseudocode:
#    IF matrix is empty: RETURN an empty list
#    CREATE a result with one empty row per original column
#    FOR each row index in matrix:
#        FOR each column index in that row:
#            ADD matrix[row][column] to result[column]
#    RETURN result
def transpose(matrix):
    """Return a new matrix with the rows and columns swapped."""
    if not matrix:
        return []

    result = [[] for _ in range(len(matrix[0]))]
    for row in range(len(matrix)):
        for column in range(len(matrix[row])):
            result[column].append(matrix[row][column])
    return result


# Problem 2: Two-Pointer Reverse List
# U - Understand
# 1. Must the original list be changed? Yes, it must be reversed in-place.
# 2. When do the pointers stop? When the left pointer reaches or passes right.
#
# P - Plan
# 2. Put one pointer at each end of the list. Swap their values, then move both
#    pointers inward until they meet.
# 3. Pseudocode:
#    SET left to 0
#    SET right to the last index of lst
#    WHILE left is less than right:
#        SWAP lst[left] and lst[right]
#        ADD 1 to left
#        SUBTRACT 1 from right
#    RETURN lst
def reverse_list(lst):
    """Reverse lst in-place using two pointers, then return it."""
    left = 0
    right = len(lst) - 1

    while left < right:
        lst[left], lst[right] = lst[right], lst[left]
        left += 1
        right -= 1
    return lst


# Problem 3: Remove Duplicates
# U - Understand
# 1. Why does sorting help? Duplicate values are next to each other.
# 2. What is returned? The number of unique elements left in items.
#
# P - Plan
# 2. Keep one pointer at the next open location for a unique item. Scan with a
#    second pointer; when a new value is found, write it at the open location.
# 3. Pseudocode:
#    IF items is empty: RETURN 0
#    SET write_index to 1
#    FOR read_index from 1 through the end of items:
#        IF items[read_index] differs from items[write_index - 1]:
#            SET items[write_index] to items[read_index]
#            ADD 1 to write_index
#    DELETE items from write_index through the end
#    RETURN write_index
def remove_dupes(items):
    """Remove duplicates from sorted items in-place and return its new length."""
    if not items:
        return 0

    write_index = 1
    for read_index in range(1, len(items)):
        if items[read_index] != items[write_index - 1]:
            items[write_index] = items[read_index]
            write_index += 1

    del items[write_index:]
    return write_index


# Problem 4: Sort Array by Parity
# U - Understand
# 1. Must even and odd values each stay in their original order? No.
# 2. How can we tell if a number is even? Its remainder after division by 2 is 0.
#
# P - Plan
# 2. Use pointers at both ends. Move the left pointer past even values and the
#    right pointer past odd values. When both are misplaced, swap them.
# 3. Pseudocode:
#    SET left to 0 and right to the last index
#    WHILE left is less than right:
#        MOVE left rightward while its value is even
#        MOVE right leftward while its value is odd
#        IF left is less than right: SWAP those values
#    RETURN nums
def sort_by_parity(nums):
    """Rearrange nums in-place so all even values precede all odd values."""
    left = 0
    right = len(nums) - 1

    while left < right:
        while left < right and nums[left] % 2 == 0:
            left += 1
        while left < right and nums[right] % 2 != 0:
            right -= 1
        if left < right:
            nums[left], nums[right] = nums[right], nums[left]
    return nums


# Problem 5: Container with Most Honey
# U - Understand
# 1. How is a container's honey amount calculated? Its width times the shorter
#    of its two line heights.
# 2. Which pointer should move after checking a container? Move the pointer at
#    the shorter line because that line limits the current container's height.
#
# P - Plan
# 2. Start with the widest possible container. Record its amount, then move the
#    shorter boundary inward and repeat until the pointers meet.
# 3. Pseudocode:
#    SET left to 0, right to the last index, and maximum_honey to 0
#    WHILE left is less than right:
#        CALCULATE width times the smaller boundary height
#        UPDATE maximum_honey if this amount is greater
#        MOVE the pointer at the shorter height inward
#    RETURN maximum_honey
def most_honey(heights):
    """Return the greatest area formed by two height lines and the x-axis."""
    left = 0
    right = len(heights) - 1
    maximum_honey = 0

    while left < right:
        width = right - left
        container_height = min(heights[left], heights[right])
        maximum_honey = max(maximum_honey, width * container_height)

        if heights[left] < heights[right]:
            left += 1
        else:
            right -= 1
    return maximum_honey


if __name__ == "__main__":
    assert transpose([[1, 2, 3], [4, 5, 6], [7, 8, 9]]) == [
        [1, 4, 7], [2, 5, 8], [3, 6, 9]
    ]
    assert transpose([[1, 2, 3], [4, 5, 6]]) == [[1, 4], [2, 5], [3, 6]]
    assert reverse_list(["pooh", "christopher robin", "piglet", "roo", "eeyore"]) == [
        "eeyore", "roo", "piglet", "christopher robin", "pooh"
    ]
    items_with_dupes = ["extract of malt", "haycorns", "honey", "thistle", "thistle"]
    assert remove_dupes(items_with_dupes) == 4
    assert items_with_dupes == ["extract of malt", "haycorns", "honey", "thistle"]
    assert remove_dupes(["extract of malt", "haycorns", "honey", "thistle"]) == 4
    parity_result = sort_by_parity([3, 1, 2, 4])
    assert all(number % 2 == 0 for number in parity_result[:2])
    assert all(number % 2 != 0 for number in parity_result[2:])
    assert sort_by_parity([0]) == [0]
    assert most_honey([1, 8, 6, 2, 5, 4, 8, 3, 7]) == 49
    assert most_honey([1, 1]) == 1
