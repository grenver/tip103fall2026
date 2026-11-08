# Unit 9 · Session 2 · Problem Set Version 1

Peer mock interviews: binary trees. [Python solutions, tree helpers, and runnable checks](week9_session2_problem_set_v1.py).

| Problem | Callable | Main concept |
| --- | --- | --- |
| 1. Creating Cookie Orders from Descriptions | `build_cookie_tree` | Value-to-node map and child set |
| 2. Cookie Sum | `count_cookie_paths` | Root-to-leaf recursion with remaining target |
| 3. Most Popular Cookie Combo | `most_popular_cookie_combo` | Postorder subtree sums and frequency map |
| 4. Convert Binary Tree of Bakery Orders to Linked List | `flatten_orders` | Reverse preorder and pointer rewiring |
| 5. Check Bakery Order Completeness | `is_complete` | Level order and the first missing position |

## Shared setup and interview routine

Use UMPIRE: clarify the result (**Understand**), identify a traversal or data structure (**Match**), state what each recursive call returns (**Plan**), code (**Implement**), trace examples (**Review**), and explain costs (**Evaluate**). In a peer mock interview, ask whether the tree may be empty and whether the function may mutate nodes before coding.

The Python file provides one shared `TreeNode(val=0, left=None, right=None)`. The pasted classes use several constructor parameter names but all store their value in `.val`; the shared class supports every positional construction in the examples. Descriptions use flavor strings even though the prompt calls the array integer-valued. The implementation supports unique hashable values, including strings and integers.

The page referred to `build_tree()` and `print_tree()` without their source code. The companion supplies local helpers matching the shown examples:

- `build_tree(values)` reads level order, assigning the next two entries to each real parent's left/right children. `None` means a missing child. Assume a valid level-order encoding; missing children are not themselves expanded.
- `tree_to_list(root)` serializes the same way, retaining internal `None` gaps and trimming trailing gaps. An empty tree becomes `[]`.
- `print_tree(root)` prints that list. These helpers are for setup/display; their costs are separate from each problem function.

Let **n** be the number of nodes and **h** the height measured as the number of nodes on the longest root-to-leaf path. Balanced trees have h = O(log n); a chain has h = O(n). Recursion uses O(h) active calls and can hit Python's recursion limit on deep trees. Arithmetic and expected dictionary/set operations are treated as constant time.

## Problem 1: Creating Cookie Orders from Descriptions

### Understand

Each `[parent, child, is_left]` identifies an edge. `1` means left child; `0` means right child. Construct and return the root of the described tree. Assume descriptions form one valid binary tree with unique node values and no conflicting edges or cycles. This function does not validate malformed descriptions. Empty descriptions return `None`; an isolated root's value cannot be inferred from no edges.

Example 1: Chocolate Chip has left child Peanut Butter and right child Oatmeal Raisin; Peanut Butter has left child Sugar. Output: `['Chocolate Chip', 'Peanut Butter', 'Oatmeal Raisin', 'Sugar']`.

Example 2: Ginger Snap has right child Snickerdoodle and left child Shortbread. Output: `['Ginger Snap', 'Shortbread', 'Snickerdoodle']`.

### Match and approach

Use a dictionary from flavor to its single `TreeNode` object and a set of child values. For each description, create either node if absent, link the correct side, and record the child. Finally return the dictionary node whose value never appeared as a child.

**Trace:** After processing `Chocolate Chip -> Peanut Butter`, both objects exist. Processing `Peanut Butter -> Sugar` reuses the existing Peanut Butter object, so the new Sugar link is visible through Chocolate Chip. The child set contains Peanut Butter, Oatmeal Raisin, and Sugar; Chocolate Chip alone remains the root.

**Why it works:** Every edge is attached to the same unique parent/child objects regardless of description order. In a valid tree every non-root has a parent and the root has none. Therefore the only value outside the child set is exactly the root.

### Implement, review, and evaluate

Use `build_cookie_tree` in the Python companion. The checks include both examples, reversed description order, and empty input.

Let `d` be the number of descriptions. Expected **O(d + n) time** and **O(n) auxiliary space**, plus O(n) for created nodes. For a nonempty described tree, d = n - 1, giving O(n) time. Balanced and unbalanced trees have the same costs: construction uses dictionary lookups, not recursive traversal.

**Common mistakes:** Creating a fresh node every time a flavor appears disconnects earlier links. Taking the first described parent as the root fails for unordered descriptions.

**Interview explanation:** “I create each node once, attach every edge, and identify the root as the only node never listed as a child.”

## Problem 2: Cookie Sum

### Understand

Count root-to-leaf paths whose node values sum to `target_sum`. Paths must begin at the root and end at a leaf. Two different paths count separately even if their values are identical. A leaf has neither child. Empty trees have zero paths, even for target zero.

Examples: `[10,5,8,3,7,12,4]`, target 22, has two paths: `10 -> 5 -> 7` and `10 -> 8 -> 4`. `[8,4,12,2,6,None,10]`, target 14, has one: `8 -> 4 -> 2`.

### Match and approach

Each call asks: how many paths from this node to a leaf supply the remaining sum? Return 0 for a missing node. Subtract this node's value. At a leaf return 1 if the remainder is zero, otherwise 0. At other nodes, add the answers from the two children.

```text
count(root=10, target=22)
  left:  node 5, remaining target 12
    leaf 3: needs 7 after subtracting 5 -> no match
    leaf 7: needs 7 after subtracting 5 -> match
  right: node 8, remaining target 12
    leaf 12: needs 4 after subtracting 8 -> no match
    leaf 4:  needs 4 after subtracting 8 -> match
total = 1 + 1 = 2
```

**Why it works:** At a leaf, the remaining target checks the complete root-to-leaf sum. At an internal node every valid path continues through exactly one child, so adding the child counts counts every valid path once. The empty-node case contributes no paths.

### Implement, review, and evaluate

Use `count_cookie_paths`. Passing a reduced target keeps each branch independent without shared mutable state. The checks include negative values, duplicate-valued paths, and a target reached at a non-leaf; the non-leaf alone must not count.

**O(n) time** because every node is visited once. **O(h) auxiliary space** for the call stack: O(log n) balanced, O(n) unbalanced. Time remains O(n) in both shapes.

**Common mistakes:** Returning a match before checking for a leaf; counting a missing child as a zero-sum path; pruning when the remaining target is negative even though later negative values may restore the sum.

**Interview explanation:** “Each call counts completions of the current root prefix. Only leaves can finish a path, and the two child counts add.”

## Problem 3: Most Popular Cookie Combo

### Understand

A node's combo is the sum of all values in its entire subtree, including itself. Return every sum with the highest frequency, in any order. This is frequency of subtree sums, not the greatest subtree sum or most common individual value. Empty input returns `[]`.

Examples: `[5,2,-3]` has subtree sums `2,-3,4`, each once, so all three are returned. `[5,2,-5]` has sums `2,-5,2`, so return `[2]`.

### Match and approach

Use postorder: calculate the left sum and right sum before the current sum. A missing subtree contributes 0. Compute `total = node.val + left_sum + right_sum`, increment its frequency, and return that total to the parent. After traversal, find the maximum frequency and collect all sums attaining it.

**Trace:** In `[5,2,-5]`, leaf 2 adds one occurrence of 2. Leaf -5 adds one occurrence of -5. The root sums to `5 + 2 - 5 = 2`, adding the second occurrence of 2.

**Why it works:** The empty subtree sum is correct. If both child sums are correct, adding them and the node gives exactly its whole subtree's sum. Every real node contributes exactly one frequency update. Selecting the highest frequency therefore returns precisely the modes.

### Implement, review, and evaluate

Use `most_popular_cookie_combo`. The nested helper returns a **sum** to its parent; the outer function returns the **list of modes**. `Counter` stores frequencies. Example checks sort tied results because any order is allowed.

Expected **O(n) time**, including the frequency scans. With `k <= n` distinct sums, **O(k + h) auxiliary space**, plus O(k) worst-case output. Overall worst-case space is O(n) for both balanced and unbalanced trees because of the map. The stack alone is O(log n) balanced and O(n) unbalanced.

**Common mistake:** Recalculating a fresh subtree traversal at every node can take O(n²) on a chain. Return each computed sum so parents reuse it.

**Interview explanation:** “Postorder gives each subtree sum once; a frequency map then lets me collect every tied most common sum.”

## Problem 4: Convert Binary Tree of Bakery Orders to Linked List

### Understand

Rewire the original nodes into a right-child chain in preorder (node, left subtree, right subtree). Every left pointer must become `None`. Return the original root so the provided `print_tree(flatten_orders(orders))` usage works. Empty input returns `None`.

The supplied example flattens to `Croissant -> Cupcake -> Cake -> Pie -> Bagel -> Blondies`. Its serialized output is `['Croissant', None, 'Cupcake', None, 'Cake', None, 'Pie', None, 'Bagel', None, 'Blondies']`.

### Match and approach

Construct the chain backward with reverse preorder: process right subtree, then left subtree, then the node. Keep `previous`, the head of the chain already built. After processing both children, set the current node's right pointer to `previous`, clear its left pointer, and move `previous` to the node.

```text
Processing order: Blondies, Bagel, Pie, Cake, Cupcake, Croissant
Built suffixes:
  Blondies
  Bagel -> Blondies
  Pie -> Bagel -> Blondies
  Cake -> Pie -> Bagel -> Blondies
  Cupcake -> Cake -> Pie -> Bagel -> Blondies
  Croissant -> Cupcake -> Cake -> Pie -> Bagel -> Blondies
```

**Why it works:** Reverse preorder visits the desired list from its end to its beginning. Before each node is linked, `previous` heads the correct suffix that follows it. Prepending the node preserves that order. Processing both children before rewiring preserves the original links while they are needed. Every visited node has its left pointer cleared.

### Implement, review, and evaluate

Use `flatten_orders`. `nonlocal previous` allows the helper to update the variable shared across recursive calls. `previous` is initialized fresh for every public function call. This is the only problem function here that mutates its input tree.

**O(n) time** and **O(h) auxiliary space**: O(log n) stack for a balanced input, O(n) for an unbalanced input. No new tree nodes are allocated; reusing nodes does not eliminate the recursion stack. The checks verify the exact original node identities, order, cleared left pointers, chain termination, and empty/single/left-chain cases.

**Common mistakes:** Overwriting a child before traversing it; allocating replacement nodes instead of reusing the original ones; claiming O(1) space while using recursion.

**Interview explanation:** “I build the preorder chain backward. Each node points to the completed suffix, so every original node is reused once.”

## Problem 5: Check Bakery Order Completeness

### Understand

A complete tree fills every level before the last, and packs the last level from left to right. This differs from a balanced tree: similar heights alone do not ensure left packing. Return a Boolean. This implementation treats an empty tree as complete.

Examples: `['Croissant','Cupcake','Bagel','Cake','Pie','Blondies'] -> True`; replacing the last level with `['Cake','Pie',None,'Blondies'] -> False` because Blondies appears after a gap.

### Match and approach

Use breadth-first search with a `deque`, visiting positions left to right and including missing children. Once a `None` position is seen, set `seen_gap`. If any real node appears afterward, return `False`. If traversal ends without that violation, return `True`.

**Trace:** `[1,2,3,4,5,None,6]` visits `1,2,3,4,5,None,6,...`. The `None` starts the gap; the following 6 proves incompleteness. `[1,2]` is complete: the root's absent right child and all later missing positions have no real node after them.

**Why it works:** A complete tree has an uninterrupted prefix of real positions in level order, followed only by absent positions. A real node after a missing position witnesses a level filled too late or a hole before a node on the last level. Conversely, with no such hole all earlier levels are filled and the last is left packed, which is exactly completeness.

### Implement, review, and evaluate

Use `is_complete`. Enqueue left before right. Missing nodes set the flag but do not enqueue children. `deque.popleft()` avoids shifting a list on each removal.

Worst-case **O(n) time** and **O(w) auxiliary space**, where `w` is maximum tree width (up to O(n)). Missing-child entries change this by only a constant factor. A broad balanced tree can need O(n) queue space; a chain has constant width, uses O(1) queue space, and a sufficiently long chain is rejected early. Balanced/unbalanced height labels alone do not determine width: a general unbalanced tree may still have O(n) width. O(n) time/space are valid overall upper bounds, and early rejection can do less work.

**Common mistakes:** Ignoring missing positions; checking only for a right child without a left child, which misses deeper gaps; confusing complete with perfect (every level fully filled).

**Interview explanation:** “In level order a complete tree cannot have any real node after the first empty position, so I scan for exactly that violation.”

## Run the checks

From the repository root:

```powershell
python "unit 9/week9_session2_problem_set_v1.py"
```

The file checks every supplied example and the structural edge cases described above. The session overview also mentions mirroring and subtree identification, but those were not among the five supplied problems, so no additional problems are invented here.
