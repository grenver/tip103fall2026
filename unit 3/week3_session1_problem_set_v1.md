# Week 3 — Session 1 — Problem Set Version 1

## 1. Counting the Layers of a Sandwich — `count_layers(sandwich)`

Each sandwich layer is a nested list. Write a **recursive** function that returns the total nesting depth.

```python
count_layers(["bread", ["lettuce", ["tomato", ["bread"]]]])  # 4
```

**Approach:** Treat the current list as one layer. Recursively find the maximum depth of any nested child list and add one.

**Why it works:** Every nested list represents one additional layer. The deepest child path therefore determines the total layer count. Time: O(n) for `n` list elements; space: O(d) call-stack space for nesting depth `d`.

## 2. Reversing Deli Orders — `reverse_orders(orders)`

Given a space-separated order string, write a **recursive** function that returns the orders in reverse order.

```python
reverse_orders("Bagel Sandwich Coffee")  # "Coffee Sandwich Bagel"
```

**Approach:** Split into words and use a helper that visits indexes from the last word down to the first, appending each word.

**Why it works:** The helper's first action takes the last order, and each recursive call takes the order directly before it, so all orders are produced in reverse. Time: O(n); space: O(n) for words, output, and recursion.

## 3. Sharing the Coffee — `can_split_coffee(coffee, n)`

Coffee batches must remain whole. Return whether their volumes can be divided evenly among `n` staff members.

```python
can_split_coffee([4, 4, 8], 2)   # True
can_split_coffee([5, 10, 15], 4) # False
```

**Approach:** First check that the total is divisible by `n`. Then recursively try assigning each batch to each person without exceeding the equal target volume.

**Why it works:** The recursion tries every valid assignment of whole batches. It returns true only if all batches form `n` equal totals. This is backtracking: worst-case time is exponential, O(n^m) for `m` batches and `n` people; space is O(m + n).

## 4. Super Sandwich — `merge_orders(sandwich_a, sandwich_b)`

Given two linked-list heads, recursively merge them in the pattern `a1 → b1 → a2 → b2 → …`. Keep the remainder when one list ends.

```python
# Bacon → Lettuce → Tomato and Turkey → Cheese → Mayo
# becomes Bacon → Turkey → Lettuce → Cheese → Tomato → Mayo
```

**Approach:** Link the current node from list A to a recursive merge beginning with the current node from B and A's next node.

**Why it works:** Each call places one A node, then switches the roles of the lists so the next call places B. The base cases attach any remaining nodes. Time: O(a + b); space: O(a + b) recursion stack.

## 5. Super Sandwich II — Compare Recursive and Iterative Merges

The provided iterative merge visits each node once and rewires next pointers in a loop.

**Comparison:** Both recursive and iterative versions take O(a + b) time. The iterative version uses O(1) extra space, while the recursive version uses O(a + b) call-stack space. The recursive version mirrors the alternating pattern neatly; the iterative version is generally preferable for long lists because it avoids recursion-depth limits.
