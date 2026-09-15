# Week 1 — Session 2 — Problem Set Version 1

## 1. Transpose Matrix

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

## 2. Two-Pointer Reverse List

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

## 3. Remove Duplicates

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

## 4. Sort Array by Parity

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

## 5. Container with Most Honey

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
