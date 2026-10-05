# Week 4 — Session 2 — Problem Set Version 1

Work through **Understand → Plan → Implement**. Before opening the implementation, trace the plan yourself. The concept map shows what each exercise adds.

## Concept progression

| Problem | Main concept | Prerequisite | Explain after solving |
| --- | --- | --- | --- |
| 1. Ivy Cutting | Follow a specified path, not the whole tree | Child references and None | Only right children are requested, even when left children exist. |
| 2. Ivy Cutting II | Express path advancement as a recursive call | Path traversal and recursive base cases | The second version must use the opposite style while keeping identical behavior. |
| 3. Pruning Plans | Postorder processes children before their parent | Recursive calls and traversal order | The required sequence is left subtree, right subtree, root. |
| 4. Sum Inventory | Combine independently solved subtree results | Subtree results and addition | Every node contributes once, so the total is root plus left sum plus right sum. |
| 5. Calculating Yield II | Evaluate operands before applying an operator | Postorder evaluation and operand order | Internal nodes need values from both children; subtraction and division preserve left/right order. |

Build on the earlier exercises, but select an approach from the requirements rather than the story. A new collection or recursive call is useful only when its behavior serves those requirements.


## Tree prerequisites and notation

The supplied `TreeNode` stores its value in `.val` and child references in `.left` and `.right`; `None` means no child. Assume ordinary acyclic trees. Here n counts nodes, h counts nodes on the longest root-to-leaf path, and r counts nodes on the right-child path. A balanced tree has h=O(log n); a skewed tree can have h=O(n). Recursion keeps suspended calls in memory. `right_vine_recursive` is a local name preserving both solutions; submit it as `right_vine` when that is the requested interface.

## 1. Ivy Cutting — `right_vine(root)`

**Learning goal:** Use this idea in a solution and explain why it works: **Follow a specified path, not the whole tree**.

**Key concept and recognition clue:** Only right children are requested, even when left children exist.

### U — Understand

Return the values reached by starting at the root and following only right-child pointers. When the root has no right child, return only its value, even if a left subtree exists.

```python
right_vine(ivy1)  # ['Root', 'Node2', 'Leaf3']
right_vine(ivy2)  # ['Root']
```

**Before planning:** Identify the input, the exact return value or mutation, and the allowed operations from the statement above. Check whether order, object identity, or input mutation matters; do not substitute printing for returning.

### P — Plan

**Hints, in order:** First identify the rule that controls the next decision. Then decide what state must be remembered. Finally, try the concrete steps below on the trace before writing code.

Append the current value and advance to its right child until None.

**Trace:** Root has left L and right R; R has left X and no right: output [Root,R], never L or X.

**Why this works and stops:** The result contains precisely the nodes reached by successive right links; the finite tree path ends at None.

### I — Implement

<details>
<summary>Open the implementation after trying the plan</summary>

```python
def right_vine(root):
    values = []
    current = root
    while current is not None:
        values.append(current.val)
        current = current.right
    return values
```

</details>

**Connect code to plan:** Append the current value and advance to its right child until None.

**Check the solution:** Walk through the supplied examples and compare the result with the required output. Then use this small case to verify the decisive step: Root has left L and right R; R has left X and no right: output [Root,R], never L or X. Try the questions below before opening their answers.

**Cost:** O(r) time and O(r) output for r right-path nodes; O(1) auxiliary space.

### Common mistakes

Falling back to left visits a node outside the requested path. Confusing this with right-side view changes the task.

### Interview explanation

“Only right children are requested, even when left children exist. My plan is: Append the current value and advance to its right child until None. The reason it works is that the result contains precisely the nodes reached by successive right links; the finite tree path ends at None. Its cost is O(r) time and O(r) output for r right-path nodes; O(1) auxiliary space.”

Use this as a model of reasoning, not a script. Say what each variable means and explain the decisive update before coding.

### Check your understanding

What if root has only a left child? What does an empty root return?

<details>
<summary>Reasoning and answers</summary>

Only the root value; an empty tree returns []. Neither case permits a left fallback.

</details>

## 2. Ivy Cutting II — recursive `right_vine`

**Learning goal:** Use this idea in a solution and explain why it works: **Express path advancement as a recursive call**.

**Key concept and recognition clue:** The second version must use the opposite style while keeping identical behavior.

### U — Understand

Use the opposite implementation style from Problem 1. Since Problem 1 uses iteration, this solution uses recursion. The Python file names it `right_vine_recursive(root)` so both versions can be called; when submitting this problem separately, use the requested name `right_vine`.

**Before planning:** Identify the input, the exact return value or mutation, and the allowed operations from the statement above. Check whether order, object identity, or input mutation matters; do not substitute printing for returning.

### P — Plan

**Hints, in order:** First identify the rule that controls the next decision. Then decide what state must be remembered. Finally, try the concrete steps below on the trace before writing code.

Create one result list. Stop on None; otherwise append the node value and recursively visit its right child.

**Trace:** visit Root appends Root; visit R appends R; visit None stops; calls return with [Root,R].

**Why this works and stops:** Each call appends one right-path node and advances to its child; None ends the finite path.

### I — Implement

<details>
<summary>Open the implementation after trying the plan</summary>

```python
def right_vine_recursive(root):
    values = []

    def visit(node):
        if node is None:
            return
        values.append(node.val)
        visit(node.right)

    visit(root)
    return values
```

</details>

**Connect code to plan:** Create one result list. Stop on None; otherwise append the node value and recursively visit its right child.

**Check the solution:** Walk through the supplied examples and compare the result with the required output. Then use this small case to verify the decisive step: visit Root appends Root; visit R appends R; visit None stops; calls return with [Root,R]. Try the questions below before opening their answers.

**Cost:** O(r) time, O(r) stack, and O(r) output for r path nodes; r is at most tree height.

### Common mistakes

Concatenating a new partial list at each call can add quadratic copying. Recursing left changes the route.

### Interview explanation

“The second version must use the opposite style while keeping identical behavior. My plan is: Create one result list. Stop on None; otherwise append the node value and recursively visit its right child. The reason it works is that each call appends one right-path node and advances to its child; None ends the finite path. Its cost is O(r) time, O(r) stack, and O(r) output for r path nodes; r is at most tree height.”

Use this as a model of reasoning, not a script. Say what each variable means and explain the decisive update before coding.

### Check your understanding

Do iterative and recursive versions return different values? Which handles a very deep path better?

<details>
<summary>Reasoning and answers</summary>

No: same path, same output. Iteration avoids Python recursion-depth limits and uses constant working space.

</details>

## 3. Pruning Plans — `survey_tree(root)`

**Learning goal:** Use this idea in a solution and explain why it works: **Postorder processes children before their parent**.

**Key concept and recognition clue:** The required sequence is left subtree, right subtree, root.

### U — Understand

Return all node values using **postorder traversal: left subtree, right subtree, root**.

```python
survey_tree(magnolia)  # ['Leaf1', 'Node1', 'Leaf2', 'Leaf3', 'Node2', 'Root']
```

**Before planning:** Identify the input, the exact return value or mutation, and the allowed operations from the statement above. Check whether order, object identity, or input mutation matters; do not substitute printing for returning.

### P — Plan

**Hints, in order:** First identify the rule that controls the next decision. Then decide what state must be remembered. Finally, try the concrete steps below on the trace before writing code.

Stop at None. Visit left, visit right, then append the current value to a shared list.

**Trace:** Root with leaves L and R: visit L and append it, then R, then Root -> [L,R,Root].

**Why this works and stops:** Each recursive subtree places its children before its root; the same property holds for the entire tree, and None stops descent.

### I — Implement

<details>
<summary>Open the implementation after trying the plan</summary>

```python
def survey_tree(root):
    values = []

    def visit(node):
        if node is None:
            return
        visit(node.left)
        visit(node.right)
        values.append(node.val)

    visit(root)
    return values
```

</details>

**Connect code to plan:** Stop at None. Visit left, visit right, then append the current value to a shared list.

**Check the solution:** Walk through the supplied examples and compare the result with the required output. Then use this small case to verify the decisive step: Root with leaves L and R: visit L and append it, then R, then Root -> [L,R,Root]. Try the questions below before opening their answers.

**Cost:** O(n) time for n nodes, O(h) stack for height h, and O(n) output.

### Common mistakes

Appending before recursion produces preorder. Swapping child calls reverses left/right order.

### Interview explanation

“The required sequence is left subtree, right subtree, root. My plan is: Stop at None. Visit left, visit right, then append the current value to a shared list. The reason it works is that each recursive subtree places its children before its root; the same property holds for the entire tree, and None stops descent. Its cost is O(n) time for n nodes, O(h) stack for height h, and O(n) output.”

Use this as a model of reasoning, not a script. Say what each variable means and explain the decisive update before coding.

### Check your understanding

What does a single-node tree produce? When could postorder help with a dependent task?

<details>
<summary>Reasoning and answers</summary>

A one-value list. Use it when a parent result needs its children completed, such as expression evaluation.

</details>

## 4. Sum Inventory — `sum_inventory(inventory)`

**Learning goal:** Use this idea in a solution and explain why it works: **Combine independently solved subtree results**.

**Key concept and recognition clue:** Every node contributes once, so the total is root plus left sum plus right sum.

### U — Understand

Return the sum of the stock values in every tree node. The supplied example returns `106`.

**Before planning:** Identify the input, the exact return value or mutation, and the allowed operations from the statement above. Check whether order, object identity, or input mutation matters; do not substitute printing for returning.

### P — Plan

**Hints, in order:** First identify the rule that controls the next decision. Then decide what state must be remembered. Finally, try the concrete steps below on the trace before writing code.

Return zero for None. Recursively sum both subtrees and add the current value.

**Trace:** Root 4 with left 2 and right 3 returns 4+2+3=9; missing children contribute 0.

**Why this works and stops:** The two child subtrees and root partition the nodes, so no stock is omitted or counted twice; empty children end recursion.

### I — Implement

<details>
<summary>Open the implementation after trying the plan</summary>

```python
def sum_inventory(inventory):
    if inventory is None:
        return 0
    return inventory.val + sum_inventory(inventory.left) + sum_inventory(inventory.right)
```

</details>

**Connect code to plan:** Return zero for None. Recursively sum both subtrees and add the current value.

**Check the solution:** Walk through the supplied examples and compare the result with the required output. Then use this small case to verify the decisive step: Root 4 with left 2 and right 3 returns 4+2+3=9; missing children contribute 0. Try the questions below before opening their answers.

**Cost:** O(n) time, O(h) auxiliary stack space, and O(1) scalar output.

### Common mistakes

Returning zero for a leaf loses its stock. Visiting one child only omits part of the tree.

### Interview explanation

“Every node contributes once, so the total is root plus left sum plus right sum. My plan is: Return zero for None. Recursively sum both subtrees and add the current value. The reason it works is that the two child subtrees and root partition the nodes, so no stock is omitted or counted twice; empty children end recursion. Its cost is O(n) time, O(h) auxiliary stack space, and O(1) scalar output.”

Use this as a model of reasoning, not a script. Say what each variable means and explain the decisive update before coding.

### Check your understanding

What does an empty tree return? How would you count nodes instead of stock?

<details>
<summary>Reasoning and answers</summary>

0. Use 1 + count(left) + count(right) for a nonempty node.

</details>

## 5. Calculating Yield II — `calculate_yield(root)`

**Learning goal:** Use this idea in a solution and explain why it works: **Evaluate operands before applying an operator**.

**Key concept and recognition clue:** Internal nodes need values from both children; subtraction and division preserve left/right order.

### U — Understand

Leaves contain integers. Every non-leaf node contains `+`, `-`, `*`, or `/` and has two children. Evaluate both children and apply the node's operator to the left result and then the right result. The supplied expression `(4 - 2) + (10 * 2)` evaluates to `22`.

**Before planning:** Identify the input, the exact return value or mutation, and the allowed operations from the statement above. Check whether order, object identity, or input mutation matters; do not substitute printing for returning.

### P — Plan

**Hints, in order:** First identify the rule that controls the next decision. Then decide what state must be remembered. Finally, try the concrete steps below on the trace before writing code.

Return an integer leaf directly. Evaluate left and right recursively, then apply the node operator to those results.

**Trace:** (4-2)+(10*2): left returns 2, right returns 20, root returns 22.

**Why this works and stops:** Each child returns its expression value before the parent combines it; leaf values end descent and preserve expression grouping.

### I — Implement

<details>
<summary>Open the implementation after trying the plan</summary>

```python
def calculate_yield(root):
    if root.left is None and root.right is None:
        return root.val
    left = calculate_yield(root.left)
    right = calculate_yield(root.right)
    if root.val == "+":
        return left + right
    if root.val == "-":
        return left - right
    if root.val == "*":
        return left * right
    if root.val == "/":
        return left / right
    raise ValueError("Unsupported operator")
```

</details>

**Connect code to plan:** Return an integer leaf directly. Evaluate left and right recursively, then apply the node operator to those results.

**Check the solution:** Walk through the supplied examples and compare the result with the required output. Then use this small case to verify the decisive step: (4-2)+(10*2): left returns 2, right returns 20, root returns 22. Try the questions below before opening their answers.

**Cost:** O(n) time and O(h) stack for n nodes and height h, under constant-cost arithmetic.

### Common mistakes

Reversing operands changes subtraction/division. Using // instead of / changes ordinary division.

### Interview explanation

“Internal nodes need values from both children; subtraction and division preserve left/right order. My plan is: Return an integer leaf directly. Evaluate left and right recursively, then apply the node operator to those results. The reason it works is that each child returns its expression value before the parent combines it; leaf values end descent and preserve expression grouping. Its cost is O(n) time and O(h) stack for n nodes and height h, under constant-cost arithmetic.”

Use this as a model of reasoning, not a script. Say what each variable means and explain the decisive update before coding.

### Check your understanding

What does 9/2 yield? Why not apply the root operator first?

<details>
<summary>Reasoning and answers</summary>

4.5 with Python /. Its operands are subtree results that must be computed first. Assume a valid nonempty expression tree and nonzero divisors.

</details>
