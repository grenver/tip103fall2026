# Week 4 — Session 1 — Problem Set Version 1

Work through **Understand → Plan → Implement**. Before opening the implementation, trace the plan yourself. The concept map shows what each exercise adds.

## Concept progression

| Problem | Main concept | Prerequisite | Explain after solving |
| --- | --- | --- | --- |
| 1. Villager Class | Each instance owns its state | Objects, attributes, and self | Every villager needs its own empty furniture inventory. |
| 2. Add Furniture | Validate before mutating an object | Instance state and set membership | Only five exact item names may change the inventory. |
| 3. Group by Personality | Filter objects, then collect the requested attribute | Object attributes and filtering | The requested output is matching names, not matching villager instances. |
| 4. Telephone | Advance a reference without changing the links | References, identity, and visited sets | Reachability follows neighbor references, not name equality or a search through all villagers. |
| 5. Linked Up | A next attribute stores a reference to another node | Node attributes and reference assignment | Connecting existing nodes requires links, not new values or copied nodes. |

Build on the earlier exercises, but select an approach from the requirements rather than the story. A new collection or recursive call is useful only when its behavior serves those requirements.


## Constructor prerequisites and file organization

Problems 3–4 use a revised constructor: `Villager(name, species, personality, catchphrase, neighbor=None)`. It retains the original attributes and adds `self.personality = personality` and `self.neighbor = neighbor`. `None` means no neighbor. The Python file preserves the initial class as `BasicVillager` and uses inheritance to keep both constructor versions available; that is a file organization choice, not a prerequisite concept for these exercises. The supplied `Node` class stores `value` and `next`, initially `None`. An attribute such as `.next` or `.neighbor` holds a reference; assigning another object to it does not copy that object.

## 1. Villager Class

**Learning goal:** Use this idea in a solution and explain why it works: **Each instance owns its state**.

**Key concept and recognition clue:** Every villager needs its own empty furniture inventory.

### U — Understand

Define `Villager(name, species, catchphrase)` with the corresponding string attributes and a new, empty `furniture` list for each instance.

**Before planning:** Identify the input, the exact return value or mutation, and the allowed operations from the statement above. Check whether order, object identity, or input mutation matters; do not substitute printing for returning.

### P — Plan

**Hints, in order:** First identify the rule that controls the next decision. Then decide what state must be remembered. Finally, try the concrete steps below on the trace before writing code.

In __init__, assign the arguments to self attributes and create self.furniture as a fresh list.

**Trace:** Create Alice and Bob; Alice.furniture.append(kotatsu) changes Alice only; Bob remains empty.

**Why this works and stops:** Each construction stores the supplied values and creates a fresh list, so inventories are independent.

### I — Implement

<details>
<summary>Open the implementation after trying the plan</summary>

```python
class Villager:
    def __init__(self, name, species, catchphrase):
        self.name = name
        self.species = species
        self.catchphrase = catchphrase
        self.furniture = []
```

</details>

**Connect code to plan:** In __init__, assign the arguments to self attributes and create self.furniture as a fresh list.

**Check the solution:** Walk through the supplied examples and compare the result with the required output. Then use this small case to verify the decisive step: Create Alice and Bob; Alice.furniture.append(kotatsu) changes Alice only; Bob remains empty. Try the questions below before opening their answers.

**Cost:** O(1) time and space per construction for the fixed set of attributes.

### Common mistakes

A furniture list stored on the class can be shared. A local name variable disappears instead of becoming an instance attribute.

### Interview explanation

“Every villager needs its own empty furniture inventory. My plan is: In __init__, assign the arguments to self attributes and create self.furniture as a fresh list. The reason it works is that each construction stores the supplied values and creates a fresh list, so inventories are independent. Its cost is O(1) time and space per construction for the fixed set of attributes.”

Use this as a model of reasoning, not a script. Say what each variable means and explain the decisive update before coding.

### Check your understanding

Should two villagers share furniture? What does self refer to?

<details>
<summary>Reasoning and answers</summary>

No. self is the particular instance whose constructor or method is running.

</details>

## 2. Add Furniture — `add_item(item_name)`

**Learning goal:** Use this idea in a solution and explain why it works: **Validate before mutating an object**.

**Key concept and recognition clue:** Only five exact item names may change the inventory.

### U — Understand

Accept only `"acoustic guitar"`, `"ironwood kitchenette"`, `"rattan armchair"`, `"kotatsu"`, or `"cacao tree"`. Append valid items to the instance's furniture list; ignore invalid items. No return value is required.

**Before planning:** Identify the input, the exact return value or mutation, and the allowed operations from the statement above. Check whether order, object identity, or input mutation matters; do not substitute printing for returning.

### P — Plan

**Hints, in order:** First identify the rule that controls the next decision. Then decide what state must be remembered. Finally, try the concrete steps below on the trace before writing code.

Create the allowed-name set. Check membership; append only on success. Invalid input leaves the inventory alone.

**Trace:** Empty inventory + cacao tree -> [cacao tree]; then nintendo switch -> still [cacao tree].

**Why this works and stops:** Only membership success reaches append; invalid values cannot change furniture.

### I — Implement

<details>
<summary>Open the implementation after trying the plan</summary>

Add this method inside the Problem 1 class.
```python
    def add_item(self, item_name):
        valid_items = {
            "acoustic guitar", "ironwood kitchenette", "rattan armchair",
            "kotatsu", "cacao tree",
        }
        if item_name in valid_items:
            self.furniture.append(item_name)
```

</details>

**Connect code to plan:** Create the allowed-name set. Check membership; append only on success. Invalid input leaves the inventory alone.

**Check the solution:** Walk through the supplied examples and compare the result with the required output. Then use this small case to verify the decisive step: Empty inventory + cacao tree -> [cacao tree]; then nintendo switch -> still [cacao tree]. Try the questions below before opening their answers.

**Cost:** O(1) amortized time and O(1) working space per call: the allowed set has fixed size; a valid call adds one output-state entry.

### Common mistakes

Appending before checking keeps invalid items. Returning a new list does not update the instance inventory.

### Interview explanation

“Only five exact item names may change the inventory. My plan is: Create the allowed-name set. Check membership; append only on success. Invalid input leaves the inventory alone. The reason it works is that only membership success reaches append; invalid values cannot change furniture. Its cost is O(1) amortized time and O(1) working space per call: the allowed set has fixed size; a valid call adds one output-state entry.”

Use this as a model of reasoning, not a script. Say what each variable means and explain the decisive update before coding.

### Check your understanding

Is adding kotatsu twice allowed by these rules? How would you disallow duplicates?

<details>
<summary>Reasoning and answers</summary>

Yes: the rules restrict names, not repeat additions. Add an inventory membership check if uniqueness becomes a requirement.

</details>

## 3. Group by Personality — `of_personality_type(townies, personality_type)`

**Learning goal:** Use this idea in a solution and explain why it works: **Filter objects, then collect the requested attribute**.

**Key concept and recognition clue:** The requested output is matching names, not matching villager instances.

### U — Understand

The constructor now takes `name, species, personality, catchphrase`. Outside the class, return the **names** of villagers whose personality matches the requested string, in any order.

```python
of_personality_type([isabelle, bob, stitches], "Lazy")  # ['Bob', 'Stitches']
of_personality_type([isabelle, bob, stitches], "Cranky")  # []
```

**Before planning:** Identify the input, the exact return value or mutation, and the allowed operations from the statement above. Check whether order, object identity, or input mutation matters; do not substitute printing for returning.

### P — Plan

**Hints, in order:** First identify the rule that controls the next decision. Then decide what state must be remembered. Finally, try the concrete steps below on the trace before writing code.

Start an empty result. Check each personality; append its name only on a match. Return after scanning all villagers.

**Trace:** Normal Isabelle is skipped for Lazy; Lazy Bob is kept as Bob, not as the Bob object.

**Why this works and stops:** Every visited match contributes its name once, and every nonmatch contributes nothing; the finite loop checks everyone.

### I — Implement

<details>
<summary>Open the implementation after trying the plan</summary>

```python
def of_personality_type(townies, personality_type):
    names = []
    for villager in townies:
        if villager.personality == personality_type:
            names.append(villager.name)
    return names
```

</details>

**Connect code to plan:** Start an empty result. Check each personality; append its name only on a match. Return after scanning all villagers.

**Check the solution:** Walk through the supplied examples and compare the result with the required output. Then use this small case to verify the decisive step: Normal Isabelle is skipped for Lazy; Lazy Bob is kept as Bob, not as the Bob object. Try the questions below before opening their answers.

**Cost:** O(n) time for n villagers; O(1) working state beyond O(k) output for k matches.

### Common mistakes

Appending the object gives the wrong output type. Returning inside the loop can miss later matches.

### Interview explanation

“The requested output is matching names, not matching villager instances. My plan is: Start an empty result. Check each personality; append its name only on a match. Return after scanning all villagers. The reason it works is that every visited match contributes its name once, and every nonmatch contributes nothing; the finite loop checks everyone. Its cost is O(n) time for n villagers; O(1) working state beyond O(k) output for k matches.”

Use this as a model of reasoning, not a script. Say what each variable means and explain the decisive update before coding.

### Check your understanding

What happens when none match? How would you return objects instead?

<details>
<summary>Reasoning and answers</summary>

Return []. Append villager rather than villager.name if the output contract changes.

</details>

## 4. Telephone — `message_received(start_villager, target_villager)`

**Learning goal:** Use this idea in a solution and explain why it works: **Advance a reference without changing the links**.

**Key concept and recognition clue:** Reachability follows neighbor references, not name equality or a search through all villagers.

### U — Understand

The updated constructor also accepts `neighbor=None`. Return whether the target instance can be reached by repeatedly following the starting villager's neighbor.





**Constructor versions in the Python file:** `BasicVillager` preserves the three-argument class for Problems 1–2. The final `Villager` class adds personality and neighbor for Problems 3–4 and inherits `add_item`.

**Before planning:** Identify the input, the exact return value or mutation, and the allowed operations from the statement above. Check whether order, object identity, or input mutation matters; do not substitute printing for returning.

### P — Plan

**Hints, in order:** First identify the rule that controls the next decision. Then decide what state must be remembered. Finally, try the concrete steps below on the trace before writing code.

Start current at the given instance. Test identity with the target. Record visited objects and advance to neighbor; stop at None or a repeated object.

**Trace:** A->B->C, target C: test A, advance B, test B, advance C, return True. Links remain unchanged.

**Why this works and stops:** current follows the only available neighbor route; identity detects the exact target, and None or repetition terminates unsuccessful traversal.

### I — Implement

<details>
<summary>Open the implementation after trying the plan</summary>

```python
def message_received(start_villager, target_villager):
    visited = set()
    current = start_villager
    while current is not None and current not in visited:
        if current is target_villager:
            return True
        visited.add(current)
        current = current.neighbor
    return False
```

</details>

**Connect code to plan:** Start current at the given instance. Test identity with the target. Record visited objects and advance to neighbor; stop at None or a repeated object.

**Check the solution:** Walk through the supplied examples and compare the result with the required output. Then use this small case to verify the decisive step: A->B->C, target C: test A, advance B, test B, advance C, return True. Links remain unchanged. Try the questions below before opening their answers.

**Cost:** O(r) expected time and O(r) auxiliary space for r distinct visited instances; an acyclic-only traversal can omit the set and use O(1) space.

### Common mistakes

Comparing names can confuse different objects. Forgetting advancement loops forever. Cycles need a termination policy.

### Interview explanation

“Reachability follows neighbor references, not name equality or a search through all villagers. My plan is: Start current at the given instance. Test identity with the target. Record visited objects and advance to neighbor; stop at None or a repeated object. The reason it works is that current follows the only available neighbor route; identity detects the exact target, and None or repetition terminates unsuccessful traversal. Its cost is O(r) expected time and O(r) auxiliary space for r distinct visited instances; an acyclic-only traversal can omit the set and use O(1) space.”

Use this as a model of reasoning, not a script. Say what each variable means and explain the decisive update before coding.

### Check your understanding

What if start is target? What if B points back to A?

<details>
<summary>Reasoning and answers</summary>

True immediately. The visited set stops the cycle and returns False if the target was not reached. Cycle protection is an extension when cycles are not specified.

</details>

## 5. Linked Up

**Learning goal:** Use this idea in a solution and explain why it works: **A next attribute stores a reference to another node**.

**Key concept and recognition clue:** Connecting existing nodes requires links, not new values or copied nodes.

### U — Understand

Connect the provided `Node` instances to form `kk_slider -> harriet -> saharah -> isabelle`.

```python
kk_slider.next = harriet
harriet.next = saharah
saharah.next = isabelle
```

**Before planning:** Identify the input, the exact return value or mutation, and the allowed operations from the statement above. Check whether order, object identity, or input mutation matters; do not substitute printing for returning.

### P — Plan

**Hints, in order:** First identify the rule that controls the next decision. Then decide what state must be remembered. Finally, try the concrete steps below on the trace before writing code.

Assign each predecessor.next to its required successor. Keep the final next as None.

**Trace:** After kk_slider.next = harriet, reading kk_slider.next reaches that same Harriet object. Then link Harriet to Saharah and Saharah to Isabelle.

**Why this works and stops:** Each assigned reference names the required successor; the fixed three links create exactly the specified chain.

### I — Implement

<details>
<summary>Open the implementation after trying the plan</summary>

```python
kk_slider.next = harriet
harriet.next = saharah
saharah.next = isabelle
```

</details>

**Connect code to plan:** Assign each predecessor.next to its required successor. Keep the final next as None.

**Check the solution:** Walk through the supplied examples and compare the result with the required output. Then use this small case to verify the decisive step: After kk_slider.next = harriet, reading kk_slider.next reaches that same Harriet object. Then link Harriet to Saharah and Saharah to Isabelle. Try the questions below before opening their answers.

**Cost:** O(1) time and auxiliary space for these three fixed assignments.

### Common mistakes

Assigning a name string to next prevents node traversal. Linking the final node back to the head creates a cycle.

### Interview explanation

“Connecting existing nodes requires links, not new values or copied nodes. My plan is: Assign each predecessor.next to its required successor. Keep the final next as None. The reason it works is that each assigned reference names the required successor; the fixed three links create exactly the specified chain. Its cost is O(1) time and auxiliary space for these three fixed assignments.”

Use this as a model of reasoning, not a script. Say what each variable means and explain the decisive update before coding.

### Check your understanding

What is kk_slider.next.next after linking? How would you insert a node between Harriet and Saharah?

<details>
<summary>Reasoning and answers</summary>

The Saharah instance. Set new.next to Saharah before setting Harriet.next to new.

</details>
