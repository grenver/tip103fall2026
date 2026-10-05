# Week 2 — Session 1 — Problem Set Version 1

Work through **Understand → Plan → Implement**. Before opening the implementation, trace the plan yourself. The concept map shows what each exercise adds.

## Concept progression

| Problem | Main concept | Prerequisite | Explain after solving |
| --- | --- | --- | --- |
| 1. Counting Treasure | Aggregate dictionary values | Dictionary keys versus values | Locations are labels; their values are the amounts to add. |
| 2. Pirate Message Check | Use a set for presence rather than frequency | Sets and subset membership | Every alphabet letter must occur at least once; repeats do not help. |
| 3. Find All Duplicate Treasure Chests | Count occurrences with a frequency map | Dictionary lookup with a default | The output asks which values occur twice, not merely which values exist. |
| 4. Booby Trap | Try a candidate and undo its change | Frequency maps and reversible updates | Exactly one deletion permits a small search over distinct letters, but every trial must start from the same counts. |
| 5. Overflowing With Gold | Search for a complement among earlier values | Dictionaries, indexes, and subtraction | x + y = target can be rewritten as y = target - x; the two indexes must be distinct. |

Build on the earlier exercises, but select an approach from the requirements rather than the story. A new collection or recursive call is useful only when its behavior serves those requirements.


## 1. Counting Treasure — `total_treasures(treasure_map)`

**Learning goal:** Use this idea in a solution and explain why it works: **Aggregate dictionary values**.

**Key concept and recognition clue:** Locations are labels; their values are the amounts to add.

### U — Understand

Given a dictionary whose location keys map to integer treasure counts, return the total treasure on the island.

```python
total_treasures({"Cove": 3, "Beach": 7, "Forest": 5})  # 15
```

**Before planning:** Identify the input, the exact return value or mutation, and the allowed operations from the statement above. Check whether order, object identity, or input mutation matters; do not substitute printing for returning.

### P — Plan

**Hints, in order:** First identify the rule that controls the next decision. Then decide what state must be remembered. Finally, try the concrete steps below on the trace before writing code.

Start at zero, visit each dictionary value, add it, and return the total.

**Trace:** Cove 3 -> total 3; Beach 7 -> 10; Forest 5 -> 15.

**Why this works and stops:** The total equals the sum of values processed so far; every location is visited once.

### I — Implement

<details>
<summary>Open the implementation after trying the plan</summary>

```python
def total_treasures(treasure_map):
    total = 0
    for amount in treasure_map.values():
        total += amount
    return total
```

</details>

**Connect code to plan:** Start at zero, visit each dictionary value, add it, and return the total.

**Check the solution:** Walk through the supplied examples and compare the result with the required output. Then use this small case to verify the decisive step: Cove 3 -> total 3; Beach 7 -> 10; Forest 5 -> 15. Try the questions below before opening their answers.

**Cost:** O(n) time for n locations; O(1) auxiliary space.

### Common mistakes

Iterating the dictionary directly yields keys rather than counts. Returning inside the loop totals only one location.

### Interview explanation

“Locations are labels; their values are the amounts to add. My plan is: Start at zero, visit each dictionary value, add it, and return the total. The reason it works is that the total equals the sum of values processed so far; every location is visited once. Its cost is O(n) time for n locations; O(1) auxiliary space.”

Use this as a model of reasoning, not a script. Say what each variable means and explain the decisive update before coding.

### Check your understanding

What does {} return? How would you find the richest location instead?

<details>
<summary>Reasoning and answers</summary>

0, the starting total. Track the largest amount and its key using items(), rather than summing values.

</details>

## 2. Pirate Message Check — `can_trust_message(message)`

**Learning goal:** Use this idea in a solution and explain why it works: **Use a set for presence rather than frequency**.

**Key concept and recognition clue:** Every alphabet letter must occur at least once; repeats do not help.

### U — Understand

Given a lowercase message that may contain whitespace, return `True` only when every English alphabet letter occurs at least once.

```python
can_trust_message("sphinx of black quartz judge my vow")  # True
can_trust_message("trust me")                             # False
```

**Before planning:** Identify the input, the exact return value or mutation, and the allowed operations from the statement above. Check whether order, object identity, or input mutation matters; do not substitute printing for returning.

### P — Plan

**Hints, in order:** First identify the rule that controls the next decision. Then decide what state must be remembered. Finally, try the concrete steps below on the trace before writing code.

Build the alphabet set and the message-character set. Test whether all required letters are present.

**Trace:** Repeated a characters leave one a in the set; missing z still makes the test false.

**Why this works and stops:** The set represents characters seen, and the subset test checks precisely the required alphabet.

### I — Implement

<details>
<summary>Open the implementation after trying the plan</summary>

```python
def can_trust_message(message):
    alphabet = set("abcdefghijklmnopqrstuvwxyz")
    return alphabet.issubset(set(message))
```

</details>

**Connect code to plan:** Build the alphabet set and the message-character set. Test whether all required letters are present.

**Check the solution:** Walk through the supplied examples and compare the result with the required output. Then use this small case to verify the decisive step: Repeated a characters leave one a in the set; missing z still makes the test false. Try the questions below before opening their answers.

**Cost:** O(n) time for n characters. Space is O(k) for distinct characters; O(1) under a fixed lowercase-letter/whitespace alphabet.

### Common mistakes

Checking message length >= 26 does not ensure coverage. Set equality rejects harmless whitespace; use a subset test.

### Interview explanation

“Every alphabet letter must occur at least once; repeats do not help. My plan is: Build the alphabet set and the message-character set. Test whether all required letters are present. The reason it works is that the set represents characters seen, and the subset test checks precisely the required alphabet. Its cost is O(n) time for n characters. Space is O(k) for distinct characters; O(1) under a fixed lowercase-letter/whitespace alphabet.”

Use this as a model of reasoning, not a script. Say what each variable means and explain the decisive update before coding.

### Check your understanding

Can 26 copies of a pass? How would you support uppercase text?

<details>
<summary>Reasoning and answers</summary>

No: 25 letters are absent. Normalize with lower() before building the set.

</details>

## 3. Find All Duplicate Treasure Chests — `find_duplicate_chests(chests)`

**Learning goal:** Use this idea in a solution and explain why it works: **Count occurrences with a frequency map**.

**Key concept and recognition clue:** The output asks which values occur twice, not merely which values exist.

### U — Understand

`chests` has length `n`; values are in `[1, n]` and each appears once or twice. Return every value that appears twice.

```python
find_duplicate_chests([4, 3, 2, 7, 8, 2, 3, 1])  # [2, 3] (either order is fine)
find_duplicate_chests([1, 1, 2])                  # [1]
```

**Before planning:** Identify the input, the exact return value or mutation, and the allowed operations from the statement above. Check whether order, object identity, or input mutation matters; do not substitute printing for returning.

### P — Plan

**Hints, in order:** First identify the rule that controls the next decision. Then decide what state must be remembered. Finally, try the concrete steps below on the trace before writing code.

Count each number with a default of zero. Select count-two keys; the current implementation sorts that output.

**Trace:** [2,1,2]: counts change {2:1} -> {2:1,1:1} -> {2:2,1:1}; output [2].

**Why this works and stops:** Counts equal occurrences processed; filtering finds exactly count-two keys, and sorting changes only output order.

### I — Implement

<details>
<summary>Open the implementation after trying the plan</summary>

```python
def find_duplicate_chests(chests):
    frequencies = {}
    for chest in chests:
        frequencies[chest] = frequencies.get(chest, 0) + 1
    return sorted(chest for chest in frequencies if frequencies[chest] == 2)
```

</details>

**Connect code to plan:** Count each number with a default of zero. Select count-two keys; the current implementation sorts that output.

**Check the solution:** Walk through the supplied examples and compare the result with the required output. Then use this small case to verify the decisive step: [2,1,2]: counts change {2:1} -> {2:1,1:1} -> {2:2,1:1}; output [2]. Try the questions below before opening their answers.

**Cost:** O(n + d log d) time for n entries and d duplicate values because the Python solution sorts results; O(n) auxiliary space and O(d) output.

### Common mistakes

A set alone loses counts. Appending on every occurrence can repeat outputs outside the once-or-twice contract.

### Interview explanation

“The output asks which values occur twice, not merely which values exist. My plan is: Count each number with a default of zero. Select count-two keys; the current implementation sorts that output. The reason it works is that counts equal occurrences processed; filtering finds exactly count-two keys, and sorting changes only output order. Its cost is O(n + d log d) time for n entries and d duplicate values because the Python solution sorts results; O(n) auxiliary space and O(d) output.”

Use this as a model of reasoning, not a script. Say what each variable means and explain the decisive update before coding.

### Check your understanding

What does [1] return? How would you report counts as well?

<details>
<summary>Reasoning and answers</summary>

[]. Return the frequency dictionary or value/count pairs instead of filtering only the keys.

</details>

## 4. Booby Trap — `can_make_balanced(code)`

**Learning goal:** Use this idea in a solution and explain why it works: **Try a candidate and undo its change**.

**Key concept and recognition clue:** Exactly one deletion permits a small search over distinct letters, but every trial must start from the same counts.

### U — Understand

Given a lowercase code, return whether deleting **exactly one** letter can make the frequency of all remaining letters equal.

```python
can_make_balanced("arghh")  # True: remove one "h"
can_make_balanced("haha")   # False
```

**Before planning:** Identify the input, the exact return value or mutation, and the allowed operations from the statement above. Check whether order, object identity, or input mutation matters; do not substitute printing for returning.

### P — Plan

**Hints, in order:** First identify the rule that controls the next decision. Then decide what state must be remembered. Finally, try the concrete steps below on the trace before writing code.

Count letters. Decrement one candidate letter. Compare positive counts; restore the decrement before trying the next candidate if it fails.

**Trace:** arghh counts 1,1,1,2: deleting h gives 1,1,1,1, so return True.

**Why this works and stops:** Each trial tests exactly one deletion from the original counts; restoration keeps trials independent, and all distinct candidates are tried.

### I — Implement

<details>
<summary>Open the implementation after trying the plan</summary>

```python
def can_make_balanced(code):
    frequencies = {}
    for letter in code:
        frequencies[letter] = frequencies.get(letter, 0) + 1

    for letter in frequencies:
        frequencies[letter] -= 1
        remaining_counts = [count for count in frequencies.values() if count > 0]
        if len(set(remaining_counts)) <= 1:
            return True
        frequencies[letter] += 1
    return False
```

</details>

**Connect code to plan:** Count letters. Decrement one candidate letter. Compare positive counts; restore the decrement before trying the next candidate if it fails.

**Check the solution:** Walk through the supplied examples and compare the result with the required output. Then use this small case to verify the decisive step: arghh counts 1,1,1,2: deleting h gives 1,1,1,1, so return True. Try the questions below before opening their answers.

**Cost:** O(n + k²) time for n characters and k distinct letters; O(k) auxiliary space. Counting input is not free.

### Common mistakes

Keeping zero counts treats an absent letter as unbalanced. Not restoring a failed trial accidentally tests multiple deletions.

### Interview explanation

“Exactly one deletion permits a small search over distinct letters, but every trial must start from the same counts. My plan is: Count letters. Decrement one candidate letter. Compare positive counts; restore the decrement before trying the next candidate if it fails. The reason it works is that each trial tests exactly one deletion from the original counts; restoration keeps trials independent, and all distinct candidates are tried. Its cost is O(n + k²) time for n characters and k distinct letters; O(k) auxiliary space. Counting input is not free.”

Use this as a model of reasoning, not a script. Say what each variable means and explain the decisive update before coding.

### Check your understanding

Why does haha fail? Why must an already-balanced string still be tested?

<details>
<summary>Reasoning and answers</summary>

Deleting one letter from counts 2,2 leaves 1,2. Exactly one deletion is mandatory; zero deletions is not a valid solution.

</details>

## 5. Overflowing With Gold — `find_treasure_indices(gold_amounts, target)`

**Learning goal:** Use this idea in a solution and explain why it works: **Search for a complement among earlier values**.

**Key concept and recognition clue:** x + y = target can be rewritten as y = target - x; the two indexes must be distinct.

### U — Understand

Return indices of two distinct gold locations whose amounts sum to `target`. Exactly one answer exists; the order may vary.

```python
find_treasure_indices([2, 7, 11, 15], 9)  # [0, 1]
find_treasure_indices([3, 2, 4], 6)       # [1, 2]
find_treasure_indices([3, 3], 6)          # [0, 1]
```

**Before planning:** Identify the input, the exact return value or mutation, and the allowed operations from the statement above. Check whether order, object identity, or input mutation matters; do not substitute printing for returning.

### P — Plan

**Hints, in order:** First identify the rule that controls the next decision. Then decide what state must be remembered. Finally, try the concrete steps below on the trace before writing code.

Scan amounts. Look up the complement in a value-to-index dictionary before storing the current amount. Return the saved and current indexes on a match.

**Trace:** [3,3], target 6: first 3 is saved at 0; second finds complement 3 and returns [0,1].

**Why this works and stops:** The map contains earlier indexes only; a found complement is a valid distinct pair. The second member of the guaranteed pair eventually finds the first.

### I — Implement

<details>
<summary>Open the implementation after trying the plan</summary>

```python
def find_treasure_indices(gold_amounts, target):
    seen = {}
    for index, amount in enumerate(gold_amounts):
        complement = target - amount
        if complement in seen:
            return [seen[complement], index]
        seen[amount] = index
    return []
```

</details>

**Connect code to plan:** Scan amounts. Look up the complement in a value-to-index dictionary before storing the current amount. Return the saved and current indexes on a match.

**Check the solution:** Walk through the supplied examples and compare the result with the required output. Then use this small case to verify the decisive step: [3,3], target 6: first 3 is saved at 0; second finds complement 3 and returns [0,1]. Try the questions below before opening their answers.

**Cost:** O(n) expected time and O(n) auxiliary space for n amounts, assuming average constant-time dictionary operations.

### Common mistakes

Storing before checking can pair an item with itself. Returning values rather than indexes violates the interface.

### Interview explanation

“x + y = target can be rewritten as y = target - x; the two indexes must be distinct. My plan is: Scan amounts. Look up the complement in a value-to-index dictionary before storing the current amount. Return the saved and current indexes on a match. The reason it works is that the map contains earlier indexes only; a found complement is a valid distinct pair. The second member of the guaranteed pair eventually finds the first. Its cost is O(n) expected time and O(n) auxiliary space for n amounts, assuming average constant-time dictionary operations.”

Use this as a model of reasoning, not a script. Say what each variable means and explain the decisive update before coding.

### Check your understanding

Why does [3,3] work? How would you handle a prompt with no guaranteed pair?

<details>
<summary>Reasoning and answers</summary>

The dictionary holds the earlier 3. Clarify the no-answer return and keep a fallback such as []; current code uses [].

</details>
