# Week 1 — Session 1 — Problem Set Version 1

Use the UPI approach for each problem: Understand, Plan, and Implement.

## 1. Hunny Hunt

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

## 2. Bouncy, Flouncy, Trouncy, Pouncy

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

## 3. T-I-Double Guh-Er II

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

## 4. Non-decreasing Array

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

## 5. Missing Clues

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
