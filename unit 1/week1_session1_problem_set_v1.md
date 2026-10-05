# Week 1 — Session 1 — Problem Set Version 1

Work through **Understand → Plan → Implement**. Before opening the implementation, trace the plan yourself. The concept map shows what each exercise adds.

## Concept progression

| Problem | Main concept | Prerequisite | Explain after solving |
| --- | --- | --- | --- |
| 1. Hunny Hunt | Search with an early return | Indexes and equality | The first matching index is requested, so left-to-right order matters. |
| 2. Bouncy, Flouncy, Trouncy, Pouncy | Maintain a running state | Variables and conditional updates | Each operation changes the same value, starting at 1. |
| 3. T-I-Double Guh-Er II | Normalize text before substring replacement | Strings, case normalization, and replacement | Removal is case insensitive and gg and er are multi-character pieces. |
| 4. Non-decreasing Array | Repair a decrease without breaking the prefix | Adjacent comparisons and list copying | One modification must make every adjacent pair ordered, not just the first bad pair. |
| 5. Missing Clues | Represent missing runs by their boundaries | Sorting and inclusive bounds | The shortest list of ranges asks for whole gaps rather than individual missing numbers. |

Build on the earlier exercises, but select an approach from the requirements rather than the story. A new collection or recursive call is useful only when its behavior serves those requirements.


## 1. Hunny Hunt

**Learning goal:** Use this idea in a solution and explain why it works: **Search with an early return**.

**Key concept and recognition clue:** The first matching index is requested, so left-to-right order matters.

### U — Understand

Write `linear_search()` to help Winnie the Pooh locate lost items. The function accepts a list `items` and a `target` value. Return the first index of `target` in `items`, or `-1` if the target is not present. Do not use built-in search functions.

```python
def linear_search(items, target):
    pass
```

Examples:

```python
linear_search(['haycorn', 'haycorn', 'haycorn', 'hunny', 'haycorn'], 'hunny')  # 3
linear_search(['bed', 'blue jacket', 'red shirt', 'hunny'], 'red balloon')     # -1
```

**Before planning:** Identify the input, the exact return value or mutation, and the allowed operations from the statement above. Check whether order, object identity, or input mutation matters; do not substitute printing for returning.

### P — Plan

**Hints, in order:** First identify the rule that controls the next decision. Then decide what state must be remembered. Finally, try the concrete steps below on the trace before writing code.

Visit indexes in order. Return on a match; return -1 only after the loop.

**Trace:** For [a, b, a], target a matches index 0; stop before index 2.

**Why this works and stops:** All earlier indexes were checked without a match; exhausting the finite list proves absence.

### I — Implement

<details>
<summary>Open the implementation after trying the plan</summary>

```python
def linear_search(items, target):
    """Return the first index of target in items, or -1 when absent."""
    for index in range(len(items)):
        if items[index] == target:
            return index
    return -1
```

</details>

**Connect code to plan:** Visit indexes in order. Return on a match; return -1 only after the loop.

**Check the solution:** Walk through the supplied examples and compare the result with the required output. Then use this small case to verify the decisive step: For [a, b, a], target a matches index 0; stop before index 2. Try the questions below before opening their answers.

**Cost:** O(n) worst-case time for n items; O(1) auxiliary space.

### Common mistakes

Returning -1 inside the loop rejects a target that appears later.

### Interview explanation

“The first matching index is requested, so left-to-right order matters. My plan is: Visit indexes in order. Return on a match; return -1 only after the loop. The reason it works is that all earlier indexes were checked without a match; exhausting the finite list proves absence. Its cost is O(n) worst-case time for n items; O(1) auxiliary space.”

Use this as a model of reasoning, not a script. Say what each variable means and explain the decisive update before coding.

### Check your understanding

What does searching [a, a] for a return? How would you return every matching index?

<details>
<summary>Reasoning and answers</summary>

0, because it is the first match. Collect matching indexes and finish the scan instead of returning early.

</details>

## 2. Bouncy, Flouncy, Trouncy, Pouncy

**Learning goal:** Use this idea in a solution and explain why it works: **Maintain a running state**.

**Key concept and recognition clue:** Each operation changes the same value, starting at 1.

### U — Understand

Tigger's language has one variable, `tigger`, which begins at `1`.

- `bouncy` and `flouncy` increase `tigger` by 1.
- `trouncy` and `pouncy` decrease `tigger` by 1.

Given a list of operations, return the final value of `tigger`.

```python
def final_value_after_operations(operations):
    pass
```

Examples:

```python
final_value_after_operations(["trouncy", "flouncy", "flouncy"])  # 2
final_value_after_operations(["bouncy", "bouncy", "flouncy"])    # 4
```

**Before planning:** Identify the input, the exact return value or mutation, and the allowed operations from the statement above. Check whether order, object identity, or input mutation matters; do not substitute printing for returning.

### P — Plan

**Hints, in order:** First identify the rule that controls the next decision. Then decide what state must be remembered. Finally, try the concrete steps below on the trace before writing code.

Initialize 1. Apply exactly one increment or decrement per operation. Return after all operations.

**Trace:** trouncy: 1 -> 0; flouncy: 0 -> 1; flouncy: 1 -> 2.

**Why this works and stops:** The running value reflects exactly the operations processed so far; the finite scan processes each once.

### I — Implement

<details>
<summary>Open the implementation after trying the plan</summary>

```python
def final_value_after_operations(operations):
    """Return Tigger's value after performing every operation."""
    tigger = 1
    for operation in operations:
        if operation == "bouncy" or operation == "flouncy":
            tigger += 1
        else:
            tigger -= 1
    return tigger
```

</details>

**Connect code to plan:** Initialize 1. Apply exactly one increment or decrement per operation. Return after all operations.

**Check the solution:** Walk through the supplied examples and compare the result with the required output. Then use this small case to verify the decisive step: trouncy: 1 -> 0; flouncy: 0 -> 1; flouncy: 1 -> 2. Try the questions below before opening their answers.

**Cost:** O(n) time for n operations; O(1) auxiliary space.

### Common mistakes

Starting at 0 shifts every answer by one. Assume only the four valid operation names.

### Interview explanation

“Each operation changes the same value, starting at 1. My plan is: Initialize 1. Apply exactly one increment or decrement per operation. Return after all operations. The reason it works is that the running value reflects exactly the operations processed so far; the finite scan processes each once. Its cost is O(n) time for n operations; O(1) auxiliary space.”

Use this as a model of reasoning, not a script. Say what each variable means and explain the decisive update before coding.

### Check your understanding

What does an empty operation list return? How would a change of two per operation affect the plan?

<details>
<summary>Reasoning and answers</summary>

1: no updates occur. Change the update amount; the running-state structure stays the same.

</details>

## 3. T-I-Double Guh-Er II

**Learning goal:** Use this idea in a solution and explain why it works: **Normalize text before substring replacement**.

**Key concept and recognition clue:** Removal is case insensitive and gg and er are multi-character pieces.

### U — Understand

Write `tiggerfy()` to accept a string `word` and return a new string with the substrings `t`, `i`, `gg`, and `er` removed. The function must be case insensitive.

```python
def tiggerfy(word):
    pass
```

Examples:

```python
tiggerfy("Trigger")   # "r"
tiggerfy("eggplant")  # "eplan"
tiggerfy("Choir")     # "chor"
```

**Before planning:** Identify the input, the exact return value or mutation, and the allowed operations from the statement above. Check whether order, object identity, or input mutation matters; do not substitute printing for returning.

### P — Plan

**Hints, in order:** First identify the rule that controls the next decision. Then decide what state must be remembered. Finally, try the concrete steps below on the trace before writing code.

Lowercase the word, then replace t, i, gg, and er with empty strings in the listed order.

**Trace:** Trigger -> trigger -> rigger -> rgger -> rer -> r.

**Why this works and stops:** Each saved string is the result of the replacements already performed; the fixed four passes terminate.

### I — Implement

<details>
<summary>Open the implementation after trying the plan</summary>

```python
def tiggerfy(word):
    """Return word lowercased with Tigger's spelling pieces removed."""
    result = word.lower()
    result = result.replace("t", "")
    result = result.replace("i", "")
    result = result.replace("gg", "")
    result = result.replace("er", "")
    return result
```

</details>

**Connect code to plan:** Lowercase the word, then replace t, i, gg, and er with empty strings in the listed order.

**Check the solution:** Walk through the supplied examples and compare the result with the required output. Then use this small case to verify the decisive step: Trigger -> trigger -> rigger -> rgger -> rer -> r. Try the questions below before opening their answers.

**Cost:** O(n) time and O(n) space for n characters: a fixed number of full-string passes.

### Common mistakes

Removing every g or e deletes letters that are not part of gg or er. Strings are immutable: save each replacement result.

### Interview explanation

“Removal is case insensitive and gg and er are multi-character pieces. My plan is: Lowercase the word, then replace t, i, gg, and er with empty strings in the listed order. The reason it works is that each saved string is the result of the replacements already performed; the fixed four passes terminate. Its cost is O(n) time and O(n) space for n characters: a fixed number of full-string passes.”

Use this as a model of reasoning, not a script. Say what each variable means and explain the decisive update before coding.

### Check your understanding

What happens to egg? Could replacement order matter on other words?

<details>
<summary>Reasoning and answers</summary>

egg becomes e. Yes: removing t from etr creates er. The current solution assumes sequential replacement in the listed order and lowercase output; clarify simultaneous-removal or case-preservation requirements if needed.

</details>

## 4. Non-decreasing Array

**Learning goal:** Use this idea in a solution and explain why it works: **Repair a decrease without breaking the prefix**.

**Key concept and recognition clue:** One modification must make every adjacent pair ordered, not just the first bad pair.

### U — Understand

Given an integer array `nums`, write `non_decreasing()` to determine whether it could become non-decreasing by modifying at most one element.

An array is non-decreasing when `nums[i] <= nums[i + 1]` for every valid index `i`.

```python
def non_decreasing(nums):
    pass
```

Examples:

```python
non_decreasing([4, 2, 3])  # True
non_decreasing([4, 2, 1])  # False
```

**Before planning:** Identify the input, the exact return value or mutation, and the allowed operations from the statement above. Check whether order, object identity, or input mutation matters; do not substitute printing for returning.

### P — Plan

**Hints, in order:** First identify the rule that controls the next decision. Then decide what state must be remembered. Finally, try the concrete steps below on the trace before writing code.

Copy the input. Count decreases. Lower the earlier value if its previous neighbor permits it; otherwise raise the later value. Reject a second required change.

**Trace:** [3,4,2,5]: lowering 4 to 2 breaks 3 <= 2, so raise 2 to 4, yielding [3,4,4,5].

**Why this works and stops:** The repaired prefix stays non-decreasing and uses at most one change; each step extends that prefix or rejects.

### I — Implement

<details>
<summary>Open the implementation after trying the plan</summary>

```python
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
```

</details>

**Connect code to plan:** Copy the input. Count decreases. Lower the earlier value if its previous neighbor permits it; otherwise raise the later value. Reject a second required change.

**Check the solution:** Walk through the supplied examples and compare the result with the required output. Then use this small case to verify the decisive step: [3,4,2,5]: lowering 4 to 2 breaks 3 <= 2, so raise 2 to 4, yielding [3,4,4,5]. Try the questions below before opening their answers.

**Cost:** O(n) time and O(n) auxiliary space for the defensive copy of n numbers.

### Common mistakes

Counting decreases in the original list alone misses [3,4,2,3], which has one decrease but cannot be repaired with one change.

### Interview explanation

“One modification must make every adjacent pair ordered, not just the first bad pair. My plan is: Copy the input. Count decreases. Lower the earlier value if its previous neighbor permits it; otherwise raise the later value. Reject a second required change. The reason it works is that the repaired prefix stays non-decreasing and uses at most one change; each step extends that prefix or rejects. Its cost is O(n) time and O(n) auxiliary space for the defensive copy of n numbers.”

Use this as a model of reasoning, not a script. Say what each variable means and explain the decisive update before coding.

### Check your understanding

Why is [4,2,3] repairable? Why is [3,4,2,3] not?

<details>
<summary>Reasoning and answers</summary>

Lower 4 to 2 in the first list. In the second, lowering 4 breaks the prefix and raising 2 breaks the next pair.

</details>

## 5. Missing Clues

**Learning goal:** Use this idea in a solution and explain why it works: **Represent missing runs by their boundaries**.

**Key concept and recognition clue:** The shortest list of ranges asks for whole gaps rather than individual missing numbers.

### U — Understand

Christopher Robin's clues are numbered within the inclusive range `[lower, upper]`. Write `find_missing_clues()` to return the shortest sorted list of inclusive ranges that covers exactly the numbers missing from the unique integer list `clues`.

```python
def find_missing_clues(clues, lower, upper):
    pass
```

Examples:

```python
find_missing_clues([0, 1, 3, 50, 75], 0, 99)
# [[2, 2], [4, 49], [51, 74], [76, 99]]

find_missing_clues([-1], -1, -1)
# []
```

**Before planning:** Identify the input, the exact return value or mutation, and the allowed operations from the statement above. Check whether order, object identity, or input mutation matters; do not substitute printing for returning.

### P — Plan

**Hints, in order:** First identify the rule that controls the next decision. Then decide what state must be remembered. Finally, try the concrete steps below on the trace before writing code.

Sort clues. Track the next expected number. Emit the gap before each clue, then the final gap through upper.

**Trace:** Bounds 0..5, clues [1,4]: emit [0,0], then [2,3], then [5,5].

**Why this works and stops:** next_number marks the first not-yet-covered value; sorted clues delimit maximal gaps, and the final check covers the upper boundary.

### I — Implement

<details>
<summary>Open the implementation after trying the plan</summary>

```python
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
```

</details>

**Connect code to plan:** Sort clues. Track the next expected number. Emit the gap before each clue, then the final gap through upper.

**Check the solution:** Walk through the supplied examples and compare the result with the required output. Then use this small case to verify the decisive step: Bounds 0..5, clues [1,4]: emit [0,0], then [2,3], then [5,5]. Try the questions below before opening their answers.

**Cost:** O(n log n) time for sorting n clues; O(n) auxiliary sorting space and O(n+1) output ranges.

### Common mistakes

Using clue rather than clue - 1 includes a present number. Forgetting the trailing gap loses missing values at the end.

### Interview explanation

“The shortest list of ranges asks for whole gaps rather than individual missing numbers. My plan is: Sort clues. Track the next expected number. Emit the gap before each clue, then the final gap through upper. The reason it works is that next_number marks the first not-yet-covered value; sorted clues delimit maximal gaps, and the final check covers the upper boundary. Its cost is O(n log n) time for sorting n clues; O(n) auxiliary sorting space and O(n+1) output ranges.”

Use this as a model of reasoning, not a script. Say what each variable means and explain the decisive update before coding.

### Check your understanding

What if clues is empty for bounds 2..4? How would already-sorted input change cost?

<details>
<summary>Reasoning and answers</summary>

Return [[2,4]]. Guaranteed sorted input removes the sorting step. Assume supplied clues lie within the bounds.

</details>
