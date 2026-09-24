# Week 2 — Session 1 — Problem Set Version 1

## 1. Counting Treasure — `total_treasures(treasure_map)`

Given a dictionary whose location keys map to integer treasure counts, return the total treasure on the island.

```python
total_treasures({"Cove": 3, "Beach": 7, "Forest": 5})  # 15
```

**Approach:** Loop through `treasure_map.values()` and add each amount to a running total.

**Why it works:** Every dictionary value represents exactly one location's treasure count, so adding all values gives the requested total. Time: O(n); extra space: O(1).

## 2. Pirate Message Check — `can_trust_message(message)`

Given a lowercase message that may contain whitespace, return `True` only when every English alphabet letter occurs at least once.

```python
can_trust_message("sphinx of black quartz judge my vow")  # True
can_trust_message("trust me")                             # False
```

**Approach:** Put the message characters in a set, then check whether the alphabet set is a subset of it.

**Why it works:** A set stores each character once; the subset test is true precisely when all 26 required letters were seen. Whitespace does not affect that test. Time: O(n); extra space: O(1), since the alphabet is fixed.

## 3. Find All Duplicate Treasure Chests — `find_duplicate_chests(chests)`

`chests` has length `n`; values are in `[1, n]` and each appears once or twice. Return every value that appears twice.

```python
find_duplicate_chests([4, 3, 2, 7, 8, 2, 3, 1])  # [2, 3] (either order is fine)
find_duplicate_chests([1, 1, 2])                  # [1]
```

**Approach:** Build a frequency map by counting every chest number, then return the keys whose count is 2.

**Why it works:** The frequency map records the exact number of appearances for each chest, so filtering for count 2 selects exactly the duplicates. Time: O(n); extra space: O(n).

## 4. Booby Trap — `can_make_balanced(code)`

Given a lowercase code, return whether deleting **exactly one** letter can make the frequency of all remaining letters equal.

```python
can_make_balanced("arghh")  # True: remove one "h"
can_make_balanced("haha")   # False
```

**Approach:** Count letters. For each distinct letter, temporarily remove one occurrence, compare all remaining positive frequencies, then restore it if needed.

**Why it works:** Any valid deletion removes one occurrence of one of the distinct letters. Trying each possible letter covers every possible deletion; the frequency comparison confirms balance. Time: O(k²), where `k` is the number of distinct letters (at most 26); extra space: O(k).

## 5. Overflowing With Gold — `find_treasure_indices(gold_amounts, target)`

Return indices of two distinct gold locations whose amounts sum to `target`. Exactly one answer exists; the order may vary.

```python
find_treasure_indices([2, 7, 11, 15], 9)  # [0, 1]
find_treasure_indices([3, 2, 4], 6)       # [1, 2]
find_treasure_indices([3, 3], 6)          # [0, 1]
```

**Approach:** Scan left to right. For amount `x`, look in a dictionary for `target - x`; if found, return its saved index and the current index. Otherwise save `x`.

**Why it works:** A pair summing to target consists of a number and its complement. Saving only earlier indices prevents using the same location twice. Time: O(n); extra space: O(n).
