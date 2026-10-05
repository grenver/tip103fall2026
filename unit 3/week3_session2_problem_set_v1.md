# Week 3 — Session 2 — Problem Set Version 1

Work through **Understand → Plan → Implement**. Before opening the implementation, trace the plan yourself. The concept map shows what each exercise adds.

## Concept progression

| Problem | Main concept | Prerequisite | Explain after solving |
| --- | --- | --- | --- |
| 1. Blueprint Approval Process | Queue removal is not approval | FIFO operations and minimum search | A higher complexity must wait while any smaller one is pending. |
| 2. Build the Tallest Skyscraper | Count forced breaks between adjacent items | Adjacent comparisons and counters | Given order matters: a taller next floor cannot sit on the current smaller top. |
| 3. Dream Corridor Design | Discard the shorter boundary safely | Two pointers and area | The shorter width/height limits area, while the distance is an index difference. |
| 4. Dream Building Layout | Track the worst prefix deficit | Running balance and integer rounding | Balanced brackets require every prefix to have at least as many openings as closings. Equal total counts alone are insufficient. |
| 5. Designing a Balanced Room | Match openings and remove only unmatched parentheses | Stacks, indexes, and string rebuilding | Letters must remain; a closing wall needs an earlier unused opening wall. |

Build on the earlier exercises, but select an approach from the requirements rather than the story. A new collection or recursive call is useful only when its behavior serves those requirements.


## 1. Blueprint Approval Process — `blueprint_approval(blueprints)`

**Learning goal:** Use this idea in a solution and explain why it works: **Queue removal is not approval**.

**Key concept and recognition clue:** A higher complexity must wait while any smaller one is pending.

### U — Understand

Given submitted blueprint complexity levels in submission order, simulate approval using a queue. Lower complexities must be approved before higher complexities. Return the complexity values in approval order.

```python
blueprint_approval([3, 5, 2, 1, 4])  # [1, 2, 3, 4, 5]
blueprint_approval([7, 4, 6, 2, 5])  # [2, 4, 5, 6, 7]
```

**Before planning:** Identify the input, the exact return value or mutation, and the allowed operations from the statement above. Check whether order, object identity, or input mutation matters; do not substitute printing for returning.

### P — Plan

**Hints, in order:** First identify the rule that controls the next decision. Then decide what state must be remembered. Finally, try the concrete steps below on the trace before writing code.

Build a deque and an approved list. Find the pending minimum, rotate front items to the back until it reaches front, approve it, and repeat.

**Trace:** [3,1,2] -> rotate 3 -> [1,2,3]; approve 1 -> [2,3]; approve 2, then 3.

**Why this works and stops:** Every approval removes a pending minimum. That minimum is reached within one queue rotation; each approval shrinks the queue.

### I — Implement

<details>
<summary>Open the implementation after trying the plan</summary>

```python
from collections import deque

def blueprint_approval(blueprints):
    queue = deque(blueprints)
    approval_order = []
    while queue:
        simplest = min(queue)
        while queue[0] != simplest:
            queue.append(queue.popleft())
        approval_order.append(queue.popleft())
    return approval_order
```

</details>

**Connect code to plan:** Build a deque and an approved list. Find the pending minimum, rotate front items to the back until it reaches front, approve it, and repeat.

**Check the solution:** Walk through the supplied examples and compare the result with the required output. Then use this small case to verify the decisive step: [3,1,2] -> rotate 3 -> [1,2,3]; approve 1 -> [2,3]; approve 2, then 3. Try the questions below before opening their answers.

**Cost:** O(n²) time for repeated scans/rotations of n blueprints; O(n) queue and output space.

### Common mistakes

popleft() returns one item and never sorts. Putting every removed item into approved immediately preserves submission order rather than priority.

### Interview explanation

“A higher complexity must wait while any smaller one is pending. My plan is: Build a deque and an approved list. Find the pending minimum, rotate front items to the back until it reaches front, approve it, and repeat. The reason it works is that every approval removes a pending minimum. That minimum is reached within one queue rotation; each approval shrinks the queue. Its cost is O(n²) time for repeated scans/rotations of n blueprints; O(n) queue and output space.”

Use this as a model of reasoning, not a script. Say what each variable means and explain the decisive update before coding.

### Check your understanding

What happens to [2,1,2]? Could a priority queue avoid rotation?

<details>
<summary>Reasoning and answers</summary>

Output [1,2,2], preserving both copies. A heap can select the minimum directly, but its behavior differs from a regular FIFO queue simulation.

</details>

## 2. Build the Tallest Skyscraper — `build_skyscrapers(floors)`

**Learning goal:** Use this idea in a solution and explain why it works: **Count forced breaks between adjacent items**.

**Key concept and recognition clue:** Given order matters: a taller next floor cannot sit on the current smaller top.

### U — Understand

Floors are processed in their given order. A new floor can be added to the current skyscraper only when it is no taller than the floor below it; otherwise begin a new skyscraper. Return the number built.

```python
build_skyscrapers([10, 5, 8, 3, 7, 2, 9])  # 4
```

**Before planning:** Identify the input, the exact return value or mutation, and the allowed operations from the statement above. Check whether order, object identity, or input mutation matters; do not substitute printing for returning.

### P — Plan

**Hints, in order:** First identify the rule that controls the next decision. Then decide what state must be remembered. Finally, try the concrete steps below on the trace before writing code.

Return zero for no floors. Otherwise start at one tower and add one whenever a height exceeds its predecessor.

**Trace:** [10,5,8,3]: 5 fits on 10; 8 forces tower 2; 3 fits on 8 -> 2 towers.

**Why this works and stops:** A rise forces a new tower, while an equal or smaller floor fits; counting exactly those rises is necessary and sufficient.

### I — Implement

<details>
<summary>Open the implementation after trying the plan</summary>

```python
def build_skyscrapers(floors):
    if not floors:
        return 0
    skyscrapers = 1
    for index in range(1, len(floors)):
        if floors[index] > floors[index - 1]:
            skyscrapers += 1
    return skyscrapers
```

</details>

**Connect code to plan:** Return zero for no floors. Otherwise start at one tower and add one whenever a height exceeds its predecessor.

**Check the solution:** Walk through the supplied examples and compare the result with the required output. Then use this small case to verify the decisive step: [10,5,8,3]: 5 fits on 10; 8 forces tower 2; 3 fits on 8 -> 2 towers. Try the questions below before opening their answers.

**Cost:** O(n) time for n floors; O(1) auxiliary space.

### Common mistakes

Sorting floors changes processing order. Counting equal heights as breaks violates the equal-or-greater rule.

### Interview explanation

“Given order matters: a taller next floor cannot sit on the current smaller top. My plan is: Return zero for no floors. Otherwise start at one tower and add one whenever a height exceeds its predecessor. The reason it works is that a rise forces a new tower, while an equal or smaller floor fits; counting exactly those rises is necessary and sufficient. Its cost is O(n) time for n floors; O(1) auxiliary space.”

Use this as a model of reasoning, not a script. Say what each variable means and explain the decisive update before coding.

### Check your understanding

How many towers for [5,5,3]? What if reordering floors were allowed?

<details>
<summary>Reasoning and answers</summary>

One. Reordering is a different problem: sorting descending would allow one tower for a nonempty list.

</details>

## 3. Dream Corridor Design — `max_corridor_area(segments)`

**Learning goal:** Use this idea in a solution and explain why it works: **Discard the shorter boundary safely**.

**Key concept and recognition clue:** The shorter width/height limits area, while the distance is an index difference.

### U — Understand

Return the maximum area between two segment boundaries: `min(segments[left], segments[right]) × (right - left)`. Distance is the difference between their indexes.

```python
max_corridor_area([1, 8, 6, 2, 5, 4, 8, 3, 7])  # 49
```

**Before planning:** Identify the input, the exact return value or mutation, and the allowed operations from the statement above. Check whether order, object identity, or input mutation matters; do not substitute printing for returning.

### P — Plan

**Hints, in order:** First identify the rule that controls the next decision. Then decide what state must be remembered. Finally, try the concrete steps below on the trace before writing code.

Use two end indexes, evaluate their area, save the best, and advance the shorter boundary until indexes meet.

**Trace:** [1,8,6,2,5,4,8,3,7]: discard height 1 after area 8; the next pair produces 49.

**Why this works and stops:** Fixing the shorter boundary while moving the other inward cannot improve its widest pair; the discarded boundary cannot hide a better answer.

### I — Implement

<details>
<summary>Open the implementation after trying the plan</summary>

```python
def max_corridor_area(segments):
    left, right = 0, len(segments) - 1
    best = 0
    while left < right:
        best = max(best, (right - left) * min(segments[left], segments[right]))
        if segments[left] < segments[right]:
            left += 1
        else:
            right -= 1
    return best
```

</details>

**Connect code to plan:** Use two end indexes, evaluate their area, save the best, and advance the shorter boundary until indexes meet.

**Check the solution:** Walk through the supplied examples and compare the result with the required output. Then use this small case to verify the decisive step: [1,8,6,2,5,4,8,3,7]: discard height 1 after area 8; the next pair produces 49. Try the questions below before opening their answers.

**Cost:** O(n) time for n segments; O(1) auxiliary space.

### Common mistakes

Using right-left+1 counts entries rather than distance. Moving only the taller boundary offers no improvement with the shorter fixed.

### Interview explanation

“The shorter width/height limits area, while the distance is an index difference. My plan is: Use two end indexes, evaluate their area, save the best, and advance the shorter boundary until indexes meet. The reason it works is that fixing the shorter boundary while moving the other inward cannot improve its widest pair; the discarded boundary cannot hide a better answer. Its cost is O(n) time for n segments; O(1) auxiliary space.”

Use this as a model of reasoning, not a script. Say what each variable means and explain the decisive update before coding.

### Check your understanding

What does [1,1] produce? How is this related to Most Honey?

<details>
<summary>Reasoning and answers</summary>

1. The story differs, but the formula and safe-boundary-discard reasoning are identical.

</details>

## 4. Dream Building Layout — `min_swaps(s)`

**Learning goal:** Use this idea in a solution and explain why it works: **Track the worst prefix deficit**.

**Key concept and recognition clue:** Balanced brackets require every prefix to have at least as many openings as closings. Equal total counts alone are insufficient.

### U — Understand

The even-length string has equal counts of `[` and `]`. Return the minimum arbitrary swaps needed to make it balanced.

```python
min_swaps("][][")   # 1
min_swaps("]]][[[") # 2
min_swaps("[]")     # 0
```

**Before planning:** Identify the input, the exact return value or mutation, and the allowed operations from the statement above. Check whether order, object identity, or input mutation matters; do not substitute printing for returning.

### P — Plan

**Hints, in order:** First identify the rule that controls the next decision. Then decide what state must be remembered. Finally, try the concrete steps below on the trace before writing code.

Add 1 for [, subtract 1 for ]. Keep the lowest running balance. Let deficit be its negation; return ceiling(deficit/2).

**Trace:**  ]]][[[ has balances -1,-2,-3,-2,-1,0; deficit 3 gives (3+1)//2=2 swaps.

**Why this works and stops:** A deficit D requires at least ceil(D/2) swaps because one swap repairs at most two units of prefix balance. Swapping an early unmatched closing with a late unmatched opening repeatedly achieves that bound.

### I — Implement

<details>
<summary>Open the implementation after trying the plan</summary>

```python
def min_swaps(s):
    balance = 0
    lowest_balance = 0
    for wall in s:
        balance += 1 if wall == "[" else -1
        lowest_balance = min(lowest_balance, balance)
    return (-lowest_balance + 1) // 2
```

</details>

**Connect code to plan:** Add 1 for [, subtract 1 for ]. Keep the lowest running balance. Let deficit be its negation; return ceiling(deficit/2).

**Check the solution:** Walk through the supplied examples and compare the result with the required output. Then use this small case to verify the decisive step:  ]]][[[ has balances -1,-2,-3,-2,-1,0; deficit 3 gives (3+1)//2=2 swaps. Try the questions below before opening their answers.

**Cost:** O(n) time for n brackets; O(1) auxiliary space.

### Common mistakes

Using the final balance yields zero for every valid-count input. Adjacent-swap formulas solve a different task; these swaps can use any positions.

### Interview explanation

“Balanced brackets require every prefix to have at least as many openings as closings. Equal total counts alone are insufficient. My plan is: Add 1 for [, subtract 1 for ]. Keep the lowest running balance. Let deficit be its negation; return ceiling(deficit/2). The reason it works is that a deficit D requires at least ceil(D/2) swaps because one swap repairs at most two units of prefix balance. Swapping an early unmatched closing with a late unmatched opening repeatedly achieves that bound. Its cost is O(n) time for n brackets; O(1) auxiliary space.”

Use this as a model of reasoning, not a script. Say what each variable means and explain the decisive update before coding.

### Check your understanding

Why is ][ not balanced? Why does deficit 3 need two swaps?

<details>
<summary>Reasoning and answers</summary>

Its first prefix is negative. A swap of an early closing with a later opening raises balances between them by 2, so one swap cannot fix a deficit of 3.

</details>

## 5. Designing a Balanced Room — `make_balanced_room(s)`

**Learning goal:** Use this idea in a solution and explain why it works: **Match openings and remove only unmatched parentheses**.

**Key concept and recognition clue:** Letters must remain; a closing wall needs an earlier unused opening wall.

### U — Understand

Remove the minimum number of parentheses from a string containing parentheses and lowercase decorations so the result is balanced. Keep all letters.

```python
make_balanced_room("art(t(d)e)sign)")  # "art(t(d)e)sign"
make_balanced_room("d)e(s)ign")        # "de(s)ign"
make_balanced_room("))((")             # ""
```

**Before planning:** Identify the input, the exact return value or mutation, and the allowed operations from the statement above. Check whether order, object identity, or input mutation matters; do not substitute printing for returning.

### P — Plan

**Hints, in order:** First identify the rule that controls the next decision. Then decide what state must be remembered. Finally, try the concrete steps below on the trace before writing code.

Store opening indexes in a stack. Match each closing by popping, or mark it for removal if none exists. Mark leftover openings, then rebuild without marked indexes.

**Trace:** a)b(c: mark ) at 1; store ( at 3; it remains unmatched, so output abc.

**Why this works and stops:** Each rejected closing has no earlier unused opening; leftover openings have no later closing. Removing exactly these unmatched walls is sufficient and necessary.

### I — Implement

<details>
<summary>Open the implementation after trying the plan</summary>

```python
def make_balanced_room(s):
    remove = set()
    open_walls = []
    for index, character in enumerate(s):
        if character == "(":
            open_walls.append(index)
        elif character == ")":
            if open_walls:
                open_walls.pop()
            else:
                remove.add(index)
    remove.update(open_walls)
    return "".join(character for index, character in enumerate(s) if index not in remove)
```

</details>

**Connect code to plan:** Store opening indexes in a stack. Match each closing by popping, or mark it for removal if none exists. Mark leftover openings, then rebuild without marked indexes.

**Check the solution:** Walk through the supplied examples and compare the result with the required output. Then use this small case to verify the decisive step: a)b(c: mark ) at 1; store ( at 3; it remains unmatched, so output abc. Try the questions below before opening their answers.

**Cost:** O(n) expected time and O(n) space for n characters, including indexes and output.

### Common mistakes

Using only total counts misses order: )( has equal counts but is invalid. Removing letters is outside the allowed operation.

### Interview explanation

“Letters must remain; a closing wall needs an earlier unused opening wall. My plan is: Store opening indexes in a stack. Match each closing by popping, or mark it for removal if none exists. Mark leftover openings, then rebuild without marked indexes. The reason it works is that each rejected closing has no earlier unused opening; leftover openings have no later closing. Removing exactly these unmatched walls is sufficient and necessary. Its cost is O(n) expected time and O(n) space for n characters, including indexes and output.”

Use this as a model of reasoning, not a script. Say what each variable means and explain the decisive update before coding.

### Check your understanding

What does ))(( become? Why is a stack useful?

<details>
<summary>Reasoning and answers</summary>

Empty string: all four walls are unmatched. Last-in-first-out matches the most recent unused opening, supporting nested parentheses.

</details>

## Note on Problems 6–7

The pasted Session 2 content supplied full statements through Problem 5 only; it listed the titles “Time to Complete Each Dream Design” and “Next Greater Element” without their requirements or examples. Send those full prompts and they can be added accurately.
