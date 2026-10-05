# Week 3 — Session 1 — Problem Set Version 1

Work through **Understand → Plan → Implement**. Before opening the implementation, trace the plan yourself. The concept map shows what each exercise adds.

## Concept progression

| Problem | Main concept | Prerequisite | Explain after solving |
| --- | --- | --- | --- |
| 1. Counting the Layers of a Sandwich | Recursive depth is one plus the deepest child | Nested lists and recursive returns | Nested lists form layers; siblings do not add to path depth. |
| 2. Reversing Deli Orders | Recursion must advance toward a base case | Base cases and index advancement | The required recursive reversal can process the last word, then the preceding one. |
| 3. Sharing the Coffee | Backtracking means choose, explore, undo | Recursive search and undo | Divisible total is necessary but whole batches must actually fit equal shares. |
| 4. Super Sandwich | Preserve the remainder while rewiring a link | Node references and recursive base cases | Alternation requires one current node followed by a merge with the list roles exchanged. |
| 5. Super Sandwich II | Separate time cost from call-stack cost | Link rewiring and stack frames | Two implementations can visit the same nodes but store different amounts of working state. |

Build on the earlier exercises, but select an approach from the requirements rather than the story. A new collection or recursive call is useful only when its behavior serves those requirements.


## Linked-node prerequisite

The supplied `Node` has `value` and `next` attributes. `next` references another node or is `None`. Linked-list merge solutions assume separate acyclic chains and mutate their next links; save a successor before replacing a link.

## 1. Counting the Layers of a Sandwich — `count_layers(sandwich)`

**Learning goal:** Use this idea in a solution and explain why it works: **Recursive depth is one plus the deepest child**.

**Key concept and recognition clue:** Nested lists form layers; siblings do not add to path depth.

### U — Understand

Each sandwich layer is a nested list. Write a **recursive** function that returns the total nesting depth.

```python
count_layers(["bread", ["lettuce", ["tomato", ["bread"]]]])  # 4
```

**Before planning:** Identify the input, the exact return value or mutation, and the allowed operations from the statement above. Check whether order, object identity, or input mutation matters; do not substitute printing for returning.

### P — Plan

**Hints, in order:** First identify the rule that controls the next decision. Then decide what state must be remembered. Finally, try the concrete steps below on the trace before writing code.

Start deepest child depth at zero. Recursively inspect list children and keep the largest depth. Return one plus that depth.

**Trace:** [bread,[lettuce,[tomato]]] returns 1+(1+(1+0))=3.

**Why this works and stops:** Every list adds one layer above its deepest child; finite nesting reaches lists without child lists.

### I — Implement

<details>
<summary>Open the implementation after trying the plan</summary>

```python
def count_layers(sandwich):
    deepest_child = 0
    for item in sandwich:
        if isinstance(item, list):
            deepest_child = max(deepest_child, count_layers(item))
    return 1 + deepest_child
```

</details>

**Connect code to plan:** Start deepest child depth at zero. Recursively inspect list children and keep the largest depth. Return one plus that depth.

**Check the solution:** Walk through the supplied examples and compare the result with the required output. Then use this small case to verify the decisive step: [bread,[lettuce,[tomato]]] returns 1+(1+(1+0))=3. Try the questions below before opening their answers.

**Cost:** O(N) time for all visited elements/list containers; O(d) stack for maximum nesting depth d.

### Common mistakes

Adding all child depths counts branches instead of nesting. Forgetting the current list loses one layer.

### Interview explanation

“Nested lists form layers; siblings do not add to path depth. My plan is: Start deepest child depth at zero. Recursively inspect list children and keep the largest depth. Return one plus that depth. The reason it works is that every list adds one layer above its deepest child; finite nesting reaches lists without child lists. Its cost is O(N) time for all visited elements/list containers; O(d) stack for maximum nesting depth d.”

Use this as a model of reasoning, not a script. Say what each variable means and explain the decisive update before coding.

### Check your understanding

What depth does [] have here? What is the depth of [[a],[b]]?

<details>
<summary>Reasoning and answers</summary>

1 under the current list-as-one-layer convention. [[a],[b]] has depth 2, since the two child lists are siblings.

</details>

## 2. Reversing Deli Orders — `reverse_orders(orders)`

**Learning goal:** Use this idea in a solution and explain why it works: **Recursion must advance toward a base case**.

**Key concept and recognition clue:** The required recursive reversal can process the last word, then the preceding one.

### U — Understand

Given a space-separated order string, write a **recursive** function that returns the orders in reverse order.

```python
reverse_orders("Bagel Sandwich Coffee")  # "Coffee Sandwich Bagel"
```

**Before planning:** Identify the input, the exact return value or mutation, and the allowed operations from the statement above. Check whether order, object identity, or input mutation matters; do not substitute printing for returning.

### P — Plan

**Hints, in order:** First identify the rule that controls the next decision. Then decide what state must be remembered. Finally, try the concrete steps below on the trace before writing code.

Split words. A helper appends the word at its index and calls itself with index-1. Stop below zero; join the result.

**Trace:** Bagel Coffee: index 1 appends Coffee; index 0 appends Bagel; index -1 stops.

**Why this works and stops:** Each call lowers the index, eventually reaching -1; appends therefore occur in reverse order.

### I — Implement

<details>
<summary>Open the implementation after trying the plan</summary>

```python
def reverse_orders(orders):
    words = orders.split()
    reversed_words = []

    def add_in_reverse(index):
        if index < 0:
            return
        reversed_words.append(words[index])
        add_in_reverse(index - 1)

    add_in_reverse(len(words) - 1)
    return " ".join(reversed_words)
```

</details>

**Connect code to plan:** Split words. A helper appends the word at its index and calls itself with index-1. Stop below zero; join the result.

**Check the solution:** Walk through the supplied examples and compare the result with the required output. Then use this small case to verify the decisive step: Bagel Coffee: index 1 appends Coffee; index 0 appends Bagel; index -1 stops. Try the questions below before opening their answers.

**Cost:** O(C) time and O(C+w) space for C input characters and w words, including split/join and a stack of w calls.

### Common mistakes

Calling with the same index never progresses. Returning a reversed character string reverses letters rather than orders.

### Interview explanation

“The required recursive reversal can process the last word, then the preceding one. My plan is: Split words. A helper appends the word at its index and calls itself with index-1. Stop below zero; join the result. The reason it works is that each call lowers the index, eventually reaching -1; appends therefore occur in reverse order. Its cost is O(C) time and O(C+w) space for C input characters and w words, including split/join and a stack of w calls.”

Use this as a model of reasoning, not a script. Say what each variable means and explain the decisive update before coding.

### Check your understanding

What happens for an empty string? How could the helper produce the original order?

<details>
<summary>Reasoning and answers</summary>

The starting index is -1 and the output is empty. Visit indexes from zero upward with an end-of-list base case.

</details>

## 3. Sharing the Coffee — `can_split_coffee(coffee, n)`

**Learning goal:** Use this idea in a solution and explain why it works: **Backtracking means choose, explore, undo**.

**Key concept and recognition clue:** Divisible total is necessary but whole batches must actually fit equal shares.

### U — Understand

Coffee batches must remain whole. Return whether their volumes can be divided evenly among `n` staff members.

```python
can_split_coffee([4, 4, 8], 2)   # True
can_split_coffee([5, 10, 15], 4) # False
```

**Before planning:** Identify the input, the exact return value or mutation, and the allowed operations from the statement above. Check whether order, object identity, or input mutation matters; do not substitute printing for returning.

### P — Plan

**Hints, in order:** First identify the rule that controls the next decision. Then decide what state must be remembered. Finally, try the concrete steps below on the trace before writing code.

Reject a nondivisible total. Sort batches descending; try a fitting bucket, recurse on the next batch, and undo on failure. Stop when every batch is assigned.

**Trace:** [4,4,8], two people: target 8; put 8 in bucket 0 and both 4s in bucket 1. [2,2,2], two people has target 3 but cannot fit.

**Why this works and stops:** Each branch represents whole-batch assignments respecting target capacity; recursive index advancement finishes a candidate, and undo permits all alternatives.

### I — Implement

<details>
<summary>Open the implementation after trying the plan</summary>

```python
def can_split_coffee(coffee, n):
    total = sum(coffee)
    if total % n != 0:
        return False
    target = total // n
    buckets = [0] * n
    coffee = sorted(coffee, reverse=True)

    def assign_batch(index):
        if index == len(coffee):
            return all(amount == target for amount in buckets)
        for person in range(n):
            if buckets[person] + coffee[index] <= target:
                buckets[person] += coffee[index]
                if assign_batch(index + 1):
                    return True
                buckets[person] -= coffee[index]
            if buckets[person] == 0:
                break
        return False

    return assign_batch(0)
```

</details>

**Connect code to plan:** Reject a nondivisible total. Sort batches descending; try a fitting bucket, recurse on the next batch, and undo on failure. Stop when every batch is assigned.

**Check the solution:** Walk through the supplied examples and compare the result with the required output. Then use this small case to verify the decisive step: [4,4,8], two people: target 8; put 8 in bucket 0 and both 4s in bucket 1. [2,2,2], two people has target 3 but cannot fit. Try the questions below before opening their answers.

**Cost:** For m batches and p people: exponential O(p^(m+1) + m log m) conservative bound including per-state bucket work/base checks; O(m+p) auxiliary space including sorted input and stack.

### Common mistakes

Checking only divisibility ignores indivisible batches. Forgetting undo leaks one branch into the next.

### Interview explanation

“Divisible total is necessary but whole batches must actually fit equal shares. My plan is: Reject a nondivisible total. Sort batches descending; try a fitting bucket, recurse on the next batch, and undo on failure. Stop when every batch is assigned. The reason it works is that each branch represents whole-batch assignments respecting target capacity; recursive index advancement finishes a candidate, and undo permits all alternatives. Its cost is For m batches and p people: exponential O(p^(m+1) + m log m) conservative bound including per-state bucket work/base checks; O(m+p) auxiliary space including sorted input and stack.”

Use this as a model of reasoning, not a script. Say what each variable means and explain the decisive update before coding.

### Check your understanding

Why can [2,2,2] fail despite divisibility? Why stop after failing one empty bucket?

<details>
<summary>Reasoning and answers</summary>

Whole 2s cannot sum to 3. Empty buckets are interchangeable, so trying another identical empty bucket repeats the same search. Assume n>0 and nonnegative batch volumes.

</details>

## 4. Super Sandwich — `merge_orders(sandwich_a, sandwich_b)`

**Learning goal:** Use this idea in a solution and explain why it works: **Preserve the remainder while rewiring a link**.

**Key concept and recognition clue:** Alternation requires one current node followed by a merge with the list roles exchanged.

### U — Understand

Given two linked-list heads, recursively merge them in the pattern `a1 → b1 → a2 → b2 → …`. Keep the remainder when one list ends.

```python
# Bacon → Lettuce → Tomato and Turkey → Cheese → Mayo
# becomes Bacon → Turkey → Lettuce → Cheese → Tomato → Mayo
```

**Before planning:** Identify the input, the exact return value or mutation, and the allowed operations from the statement above. Check whether order, object identity, or input mutation matters; do not substitute printing for returning.

### P — Plan

**Hints, in order:** First identify the rule that controls the next decision. Then decide what state must be remembered. Finally, try the concrete steps below on the trace before writing code.

If a head is missing return the other remainder. Save A.next, link A to merge(B, saved next A), and return A.

**Trace:** A1->A2 and B1->B2: A1 links to merge(B1,A2), which places B1 before A2, then B2.

**Why this works and stops:** A call places the current A node before a merge with exchanged roles; at least one node is consumed per call until a remainder is attached.

### I — Implement

<details>
<summary>Open the implementation after trying the plan</summary>

```python
def merge_orders(sandwich_a, sandwich_b):
    if not sandwich_a:
        return sandwich_b
    if not sandwich_b:
        return sandwich_a
    next_a = sandwich_a.next
    sandwich_a.next = merge_orders(sandwich_b, next_a)
    return sandwich_a
```

</details>

**Connect code to plan:** If a head is missing return the other remainder. Save A.next, link A to merge(B, saved next A), and return A.

**Check the solution:** Walk through the supplied examples and compare the result with the required output. Then use this small case to verify the decisive step: A1->A2 and B1->B2: A1 links to merge(B1,A2), which places B1 before A2, then B2. Try the questions below before opening their answers.

**Cost:** O(a+b) worst-case time and stack space for lists of a and b nodes.

### Common mistakes

Overwriting next before saving it can lose a chain. Treating this as a sorted merge changes the required order.

### Interview explanation

“Alternation requires one current node followed by a merge with the list roles exchanged. My plan is: If a head is missing return the other remainder. Save A.next, link A to merge(B, saved next A), and return A. The reason it works is that a call places the current A node before a merge with exchanged roles; at least one node is consumed per call until a remainder is attached. Its cost is O(a+b) worst-case time and stack space for lists of a and b nodes.”

Use this as a model of reasoning, not a script. Say what each variable means and explain the decisive update before coding.

### Check your understanding

What if B is empty? Are new nodes required?

<details>
<summary>Reasoning and answers</summary>

Return A unchanged. No: the algorithm reuses nodes and mutates links; assume separate acyclic input chains.

</details>

## 5. Super Sandwich II — Compare Recursive and Iterative Merges

**Learning goal:** Use this idea in a solution and explain why it works: **Separate time cost from call-stack cost**.

**Key concept and recognition clue:** Two implementations can visit the same nodes but store different amounts of working state.

### U — Understand

The provided iterative merge visits each node once and rewires next pointers in a loop.

**Before planning:** Identify the input, the exact return value or mutation, and the allowed operations from the statement above. Check whether order, object identity, or input mutation matters; do not substitute printing for returning.

### P — Plan

**Hints, in order:** First identify the rule that controls the next decision. Then decide what state must be remembered. Finally, try the concrete steps below on the trace before writing code.

Compare visits, then account for suspended recursive calls versus a fixed number of loop references. Both must retain the unconsumed tails.

**Trace:** For A1->A2 and B1, either style gives A1->B1->A2; recursion keeps pending calls while a loop keeps a few references.

**Why this works and stops:** Both styles retain the next unconsumed node before rewiring and consume nodes without repetition; only their working storage differs.

### I — Implement

<details>
<summary>Open the implementation after trying the plan</summary>

This exercise compares implementations rather than introducing another required function. Explain the recursive merge above and the supplied iterative version using the cost comparison below; preserve the original alternating order.

</details>

**Connect code to plan:** Compare visits, then account for suspended recursive calls versus a fixed number of loop references. Both must retain the unconsumed tails.

**Check the solution:** Walk through the supplied examples and compare the result with the required output. Then use this small case to verify the decisive step: For A1->A2 and B1, either style gives A1->B1->A2; recursion keeps pending calls while a loop keeps a few references. Try the questions below before opening their answers.

**Cost:** Both O(a+b) time; iterative O(1) auxiliary space, recursive O(a+b) stack upper bound.

### Common mistakes

Calling recursion O(1) space ignores its stack. Measuring only a short example does not establish asymptotic cost.

### Interview explanation

“Two implementations can visit the same nodes but store different amounts of working state. My plan is: Compare visits, then account for suspended recursive calls versus a fixed number of loop references. Both must retain the unconsumed tails. The reason it works is that both styles retain the next unconsumed node before rewiring and consume nodes without repetition; only their working storage differs. Its cost is Both O(a+b) time; iterative O(1) auxiliary space, recursive O(a+b) stack upper bound.”

Use this as a model of reasoning, not a script. Say what each variable means and explain the decisive update before coding.

### Check your understanding

Which style is safer for a very long chain? Does O(1) auxiliary space mean no input nodes exist?

<details>
<summary>Reasoning and answers</summary>

Iteration avoids recursion-depth limits. Auxiliary space excludes the already-existing input nodes.

</details>
