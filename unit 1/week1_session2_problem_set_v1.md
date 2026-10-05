# Week 1 — Session 2 — Problem Set Version 1

Work through **Understand → Plan → Implement**. Before opening the implementation, trace the plan yourself. The concept map shows what each exercise adds.

## Concept progression

| Problem | Main concept | Prerequisite | Explain after solving |
| --- | --- | --- | --- |
| 1. Transpose Matrix | Swap row and column roles | Nested lists and indexes | Transpose changes an r-by-c matrix into c-by-r, even when it is not square. |
| 2. Two-Pointer Reverse List | Two pointers shrink the unfinished region | Indexes and swapping | In-place reversal pairs the first value with the last, then works inward. |
| 3. Remove Duplicates | Separate reading from writing | Sorted adjacency and in-place writes | Sorted duplicates are adjacent, and in-place output must use the original list. |
| 4. Sort Array by Parity | Partition by a predicate | Remainder testing and swapping | Only even-before-odd matters; sorting numerically or preserving order is unnecessary. |
| 5. Container with Most Honey | Discard a limiting boundary safely | Indexes, minimum height, and area | Area is distance times the shorter height; the shorter boundary limits improvement. |

Build on the earlier exercises, but select an approach from the requirements rather than the story. A new collection or recursive call is useful only when its behavior serves those requirements.


## 1. Transpose Matrix

**Learning goal:** Use this idea in a solution and explain why it works: **Swap row and column roles**.

**Key concept and recognition clue:** Transpose changes an r-by-c matrix into c-by-r, even when it is not square.

### U — Understand

Write `transpose()` to accept a 2D integer array `matrix` and return its transpose. A transpose flips a matrix over its main diagonal, swapping rows and columns.

```python
def transpose(matrix):
    pass
```

Examples:

```python
transpose([
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
])
# [[1, 4, 7], [2, 5, 8], [3, 6, 9]]

transpose([
    [1, 2, 3],
    [4, 5, 6]
])
# [[1, 4], [2, 5], [3, 6]]
```

**Before planning:** Identify the input, the exact return value or mutation, and the allowed operations from the statement above. Check whether order, object identity, or input mutation matters; do not substitute printing for returning.

### P — Plan

**Hints, in order:** First identify the rule that controls the next decision. Then decide what state must be remembered. Finally, try the concrete steps below on the trace before writing code.

Create one output row per input column. Visit each cell and append it to the output row named by its column.

**Trace:** [[1,2,3],[4,5,6]]: column 0 becomes [1,4]; column 1 becomes [2,5]; column 2 becomes [3,6].

**Why this works and stops:** Each original cell appears in exactly its transposed output position; both finite index loops finish.

### I — Implement

<details>
<summary>Open the implementation after trying the plan</summary>

```python
def transpose(matrix):
    """Return a new matrix with the rows and columns swapped."""
    if not matrix:
        return []

    result = [[] for _ in range(len(matrix[0]))]
    for row in range(len(matrix)):
        for column in range(len(matrix[row])):
            result[column].append(matrix[row][column])
    return result
```

</details>

**Connect code to plan:** Create one output row per input column. Visit each cell and append it to the output row named by its column.

**Check the solution:** Walk through the supplied examples and compare the result with the required output. Then use this small case to verify the decisive step: [[1,2,3],[4,5,6]]: column 0 becomes [1,4]; column 1 becomes [2,5]; column 2 becomes [3,6]. Try the questions below before opening their answers.

**Cost:** O(rc) time and output space; O(c) list headers, with constant working state beyond the result.

### Common mistakes

Using the row count for both dimensions fails on rectangular matrices. Repeating the same inner list aliases output rows.

### Interview explanation

“Transpose changes an r-by-c matrix into c-by-r, even when it is not square. My plan is: Create one output row per input column. Visit each cell and append it to the output row named by its column. The reason it works is that each original cell appears in exactly its transposed output position; both finite index loops finish. Its cost is O(rc) time and output space; O(c) list headers, with constant working state beyond the result.”

Use this as a model of reasoning, not a script. Say what each variable means and explain the decisive update before coding.

### Check your understanding

What shape does a 2-by-3 input produce? What does a second transpose do?

<details>
<summary>Reasoning and answers</summary>

3-by-2. Transposing twice restores the original rectangular matrix. Assume rows have equal length.

</details>

## 2. Two-Pointer Reverse List

**Learning goal:** Use this idea in a solution and explain why it works: **Two pointers shrink the unfinished region**.

**Key concept and recognition clue:** In-place reversal pairs the first value with the last, then works inward.

### U — Understand

Write `reverse_list()` to reverse a list `lst` in-place without list slicing such as `lst[::-1]`. Use two pointers, one beginning at the front and the other at the end, moving inward as values are swapped.

```python
def reverse_list(lst):
    pass
```

Example:

```python
reverse_list(["pooh", "christopher robin", "piglet", "roo", "eeyore"])
# ["eeyore", "roo", "piglet", "christopher robin", "pooh"]
```

**Before planning:** Identify the input, the exact return value or mutation, and the allowed operations from the statement above. Check whether order, object identity, or input mutation matters; do not substitute printing for returning.

### P — Plan

**Hints, in order:** First identify the rule that controls the next decision. Then decide what state must be remembered. Finally, try the concrete steps below on the trace before writing code.

Place indexes at both ends. Swap values, increment left and decrement right; stop when they meet or cross.

**Trace:** [a,b,c,d] -> [d,b,c,a] -> [d,c,b,a].

**Why this works and stops:** Values outside the two pointers are already in final positions; the unfinished interval shrinks after every swap.

### I — Implement

<details>
<summary>Open the implementation after trying the plan</summary>

```python
def reverse_list(lst):
    """Reverse lst in-place using two pointers, then return it."""
    left = 0
    right = len(lst) - 1

    while left < right:
        lst[left], lst[right] = lst[right], lst[left]
        left += 1
        right -= 1
    return lst
```

</details>

**Connect code to plan:** Place indexes at both ends. Swap values, increment left and decrement right; stop when they meet or cross.

**Check the solution:** Walk through the supplied examples and compare the result with the required output. Then use this small case to verify the decisive step: [a,b,c,d] -> [d,b,c,a] -> [d,c,b,a]. Try the questions below before opening their answers.

**Cost:** O(n) time for n items; O(1) auxiliary space.

### Common mistakes

Failing to move both pointers can repeat work forever. Slicing makes a new list instead of performing the requested swaps.

### Interview explanation

“In-place reversal pairs the first value with the last, then works inward. My plan is: Place indexes at both ends. Swap values, increment left and decrement right; stop when they meet or cross. The reason it works is that values outside the two pointers are already in final positions; the unfinished interval shrinks after every swap. Its cost is O(n) time for n items; O(1) auxiliary space.”

Use this as a model of reasoning, not a script. Say what each variable means and explain the decisive update before coding.

### Check your understanding

Does the middle item of an odd-length list move? How could you reverse only a specified range?

<details>
<summary>Reasoning and answers</summary>

The middle item stays in place. Start the pointers at the range boundaries and use the same loop.

</details>

## 3. Remove Duplicates

**Learning goal:** Use this idea in a solution and explain why it works: **Separate reading from writing**.

**Key concept and recognition clue:** Sorted duplicates are adjacent, and in-place output must use the original list.

### U — Understand

Write `remove_dupes()` to remove duplicate values from a sorted array `items` in-place, leaving each value once. Return the length of the modified array. Do not create another array.

```python
def remove_dupes(items):
    pass
```

Examples:

```python
remove_dupes(["extract of malt", "haycorns", "honey", "thistle", "thistle"])
# 4

remove_dupes(["extract of malt", "haycorns", "honey", "thistle"])
# 4
```

**Before planning:** Identify the input, the exact return value or mutation, and the allowed operations from the statement above. Check whether order, object identity, or input mutation matters; do not substitute printing for returning.

### P — Plan

**Hints, in order:** First identify the rule that controls the next decision. Then decide what state must be remembered. Finally, try the concrete steps below on the trace before writing code.

Keep a write position after the first unique value. Scan with a read position, writing only new values. Delete the unused tail and return the write position.

**Trace:** [a,a,b,b,c]: write b at 1 and c at 2; keep [a,b,c] and return 3.

**Why this works and stops:** The prefix before write_index contains exactly the distinct values read so far; read advances to the end.

### I — Implement

<details>
<summary>Open the implementation after trying the plan</summary>

```python
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
```

</details>

**Connect code to plan:** Keep a write position after the first unique value. Scan with a read position, writing only new values. Delete the unused tail and return the write position.

**Check the solution:** Walk through the supplied examples and compare the result with the required output. Then use this small case to verify the decisive step: [a,a,b,b,c]: write b at 1 and c at 2; keep [a,b,c] and return 3. Try the questions below before opening their answers.

**Cost:** O(n) time, including tail deletion; O(1) auxiliary space for n items.

### Common mistakes

Deleting elements during the scan shifts indexes. Returning len(items) before trimming counts stale values.

### Interview explanation

“Sorted duplicates are adjacent, and in-place output must use the original list. My plan is: Keep a write position after the first unique value. Scan with a read position, writing only new values. Delete the unused tail and return the write position. The reason it works is that the prefix before write_index contains exactly the distinct values read so far; read advances to the end. Its cost is O(n) time, including tail deletion; O(1) auxiliary space for n items.”

Use this as a model of reasoning, not a script. Say what each variable means and explain the decisive update before coding.

### Check your understanding

What happens for [a,a,a]? Would the same adjacent comparison work on [a,b,a]?

<details>
<summary>Reasoning and answers</summary>

It becomes [a] and returns 1. No: sorted order is essential for adjacent duplicate detection.

</details>

## 4. Sort Array by Parity

**Learning goal:** Use this idea in a solution and explain why it works: **Partition by a predicate**.

**Key concept and recognition clue:** Only even-before-odd matters; sorting numerically or preserving order is unnecessary.

### U — Understand

Given an integer array `nums`, write `sort_by_parity()` to move all even integers to the beginning, followed by all odd integers. Return any array that satisfies that condition.

```python
def sort_by_parity(nums):
    pass
```

Examples:

```python
sort_by_parity([3, 1, 2, 4])  # One valid result: [2, 4, 3, 1]
sort_by_parity([0])           # [0]
```

**Before planning:** Identify the input, the exact return value or mutation, and the allowed operations from the statement above. Check whether order, object identity, or input mutation matters; do not substitute printing for returning.

### P — Plan

**Hints, in order:** First identify the rule that controls the next decision. Then decide what state must be remembered. Finally, try the concrete steps below on the trace before writing code.

Move left past evens and right past odds. Swap misplaced values; repeat until pointers meet.

**Trace:** [3,1,2,4]: swap 3 and 4 -> [4,1,2,3]; swap 1 and 2 -> [4,2,1,3].

**Why this works and stops:** Values before left are even and after right are odd; pointer movement or a swap makes progress.

### I — Implement

<details>
<summary>Open the implementation after trying the plan</summary>

```python
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
```

</details>

**Connect code to plan:** Move left past evens and right past odds. Swap misplaced values; repeat until pointers meet.

**Check the solution:** Walk through the supplied examples and compare the result with the required output. Then use this small case to verify the decisive step: [3,1,2,4]: swap 3 and 4 -> [4,1,2,3]; swap 1 and 2 -> [4,2,1,3]. Try the questions below before opening their answers.

**Cost:** O(n) time: each pointer moves only inward; O(1) auxiliary space.

### Common mistakes

Treating 0 as odd violates remainder testing. Assuming stable ordering imposes a rule the prompt does not require.

### Interview explanation

“Only even-before-odd matters; sorting numerically or preserving order is unnecessary. My plan is: Move left past evens and right past odds. Swap misplaced values; repeat until pointers meet. The reason it works is that values before left are even and after right are odd; pointer movement or a swap makes progress. Its cost is O(n) time: each pointer moves only inward; O(1) auxiliary space.”

Use this as a model of reasoning, not a script. Say what each variable means and explain the decisive update before coding.

### Check your understanding

Can [4,2,1,3] be valid? What changes if original order within each group must stay?

<details>
<summary>Reasoning and answers</summary>

Yes. Stability is a new requirement; a simple separate even/odd collection preserves order but uses O(n) memory.

</details>

## 5. Container with Most Honey

**Learning goal:** Use this idea in a solution and explain why it works: **Discard a limiting boundary safely**.

**Key concept and recognition clue:** Area is distance times the shorter height; the shorter boundary limits improvement.

### U — Understand

Given an integer array `heights`, where `heights[i]` is the height of a vertical line at index `i`, write `most_honey()` to find two lines that, with the x-axis, form the container holding the most honey. Containers cannot be slanted. Return the maximum amount of honey it can store.

```python
def most_honey(heights):
    pass
```

Examples:

```python
most_honey([1, 8, 6, 2, 5, 4, 8, 3, 7])  # 49
most_honey([1, 1])                        # 1
```

**Before planning:** Identify the input, the exact return value or mutation, and the allowed operations from the statement above. Check whether order, object identity, or input mutation matters; do not substitute printing for returning.

### P — Plan

**Hints, in order:** First identify the rule that controls the next decision. Then decide what state must be remembered. Finally, try the concrete steps below on the trace before writing code.

Start at both ends. Record the area and move the shorter boundary inward. Keep the best area until the pointers meet.

**Trace:** [1,8,6,2,5,4,8,3,7]: first area 1*8=8; move left; next area 7*7=49.

**Why this works and stops:** With the shorter boundary fixed, a narrower pair cannot improve on its widest checked pair. Discarding it loses no better candidate; the interval shrinks.

### I — Implement

<details>
<summary>Open the implementation after trying the plan</summary>

```python
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
```

</details>

**Connect code to plan:** Start at both ends. Record the area and move the shorter boundary inward. Keep the best area until the pointers meet.

**Check the solution:** Walk through the supplied examples and compare the result with the required output. Then use this small case to verify the decisive step: [1,8,6,2,5,4,8,3,7]: first area 1*8=8; move left; next area 7*7=49. Try the questions below before opening their answers.

**Cost:** O(n) time for n heights; O(1) auxiliary space.

### Common mistakes

Using the taller height overestimates capacity. Distance is right - left, not the number of included entries.

### Interview explanation

“Area is distance times the shorter height; the shorter boundary limits improvement. My plan is: Start at both ends. Record the area and move the shorter boundary inward. Keep the best area until the pointers meet. The reason it works is that with the shorter boundary fixed, a narrower pair cannot improve on its widest checked pair. Discarding it loses no better candidate; the interval shrinks. Its cost is O(n) time for n heights; O(1) auxiliary space.”

Use this as a model of reasoning, not a script. Say what each variable means and explain the decisive update before coding.

### Check your understanding

What is the area for [1,1]? Why can the shorter boundary be discarded?

<details>
<summary>Reasoning and answers</summary>

1. Keeping that boundary while shrinking width cannot beat its widest checked pair, since the minimum height cannot increase above that boundary.

</details>
