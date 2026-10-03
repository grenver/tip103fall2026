# Week 4 — Session 2 — Problem Set Version 1

For the complexity analyses below, `n` is the number of tree nodes, `h` is the tree height, and `r` is the number of nodes on the right-child path. A balanced tree has `h = O(log n)` and `r <= h`. Space for returned results is distinguished from auxiliary working space.

## 1. Ivy Cutting — `right_vine(root)`

Return the values reached by starting at the root and following only right-child pointers. When the root has no right child, return only its value, even if a left subtree exists.

```python
right_vine(ivy1)  # ['Root', 'Node2', 'Leaf3']
right_vine(ivy2)  # ['Root']
```

**Approach:** Iteratively append the current value and move to `current.right` until it is `None`.

**Why it works:** Each appended node is the next node on the specified right-child path. It never switches to a left child. An empty tree returns `[]`.

**Complexity:** O(r) time and O(r) output space because each path node is visited and stored once; O(1) auxiliary space. For a balanced tree, time and total space are O(log n) upper bounds.

## 2. Ivy Cutting II — recursive `right_vine`

Use the opposite implementation style from Problem 1. Since Problem 1 uses iteration, this solution uses recursion. The Python file names it `right_vine_recursive(root)` so both versions can be called; when submitting this problem separately, use the requested name `right_vine`.

**Approach:** A recursive helper appends a node's value to one shared result list and visits its right child. `None` is the base case.

**Why it works:** Each recursive call advances one step along the same right-child path as the iterative solution.

**Complexity:** O(r) time, O(r) recursion space, and O(r) output space. These are O(log n) upper bounds for a balanced tree. Appending to one list avoids repeatedly copying partial lists during recursion.

## 3. Pruning Plans — `survey_tree(root)`

Return all node values using **postorder traversal: left subtree, right subtree, root**.

```python
survey_tree(magnolia)  # ['Leaf1', 'Node1', 'Leaf2', 'Leaf3', 'Node2', 'Root']
```

**Approach:** Recursively visit the left and right children before appending the current value to one result list.

**Why it works:** Every subtree is processed in the required order, so a parent is added after both of its subtrees. An empty tree returns `[]`.

**Complexity:** O(n) time because every node is visited once. Auxiliary recursion space is O(h), or O(log n) for a balanced tree. Output space and total space are O(n) because all values are returned.

## 4. Sum Inventory — `sum_inventory(inventory)`

Return the sum of the stock values in every tree node. The supplied example returns `106`.

**Approach:** An empty subtree contributes zero. Otherwise return the node value plus the recursively calculated sums of both children.

**Why it works:** Each subtree's sum includes its root and every descendant exactly once.

**Complexity:** O(n) time because each node contributes once. O(h) auxiliary stack space, or O(log n) for a balanced tree. The scalar result takes O(1) space.

## 5. Calculating Yield II — `calculate_yield(root)`

Leaves contain integers. Every non-leaf node contains `+`, `-`, `*`, or `/` and has two children. Evaluate both children and apply the node's operator to the left result and then the right result. The supplied expression `(4 - 2) + (10 * 2)` evaluates to `22`.

**Approach:** Return a leaf's value directly. For an internal node, recursively evaluate both operands, then apply its operator. Python `/` performs ordinary division; the prompt does not request floor division.

**Why it works:** Children are fully evaluated before their parent operation, matching the expression tree's grouping. Operand order is preserved for subtraction and division.

**Complexity:** O(n) time and O(h) auxiliary stack space, or O(log n) space for a balanced tree, assuming each arithmetic operation takes constant time. The function assumes the valid, nonempty expression tree described in the prompt and nonzero divisors.
