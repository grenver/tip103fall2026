# Week 4 — Session 1 — Problem Set Version 1

## 1. Villager Class

Define `Villager(name, species, catchphrase)` with the corresponding string attributes and a new, empty `furniture` list for each instance.

**Approach:** Assign each argument to an instance attribute in `__init__` and initialize `self.furniture = []`.

**Why it works:** Each object retains its own supplied values and its own inventory. Construction takes O(1) time and space.

## 2. Add Furniture — `add_item(item_name)`

Accept only `"acoustic guitar"`, `"ironwood kitchenette"`, `"rattan armchair"`, `"kotatsu"`, or `"cacao tree"`. Append valid items to the instance's furniture list; ignore invalid items. No return value is required.

**Approach:** Check membership in a set of the five allowed names before appending.

**Why it works:** Only an allowed name reaches the append operation. Each call takes O(1) amortized time and O(1) auxiliary space, with one additional inventory entry when valid.

## 3. Group by Personality — `of_personality_type(townies, personality_type)`

The constructor now takes `name, species, personality, catchphrase`. Outside the class, return the **names** of villagers whose personality matches the requested string, in any order.

```python
of_personality_type([isabelle, bob, stitches], "Lazy")  # ['Bob', 'Stitches']
of_personality_type([isabelle, bob, stitches], "Cranky")  # []
```

**Approach:** Traverse the villagers and append each matching name.

**Why it works:** Each villager is checked once, and exactly the matching names are returned. For `n` villagers and `k` matches, time is O(n), auxiliary space is O(1), and output space is O(k).

## 4. Telephone — `message_received(start_villager, target_villager)`

The updated constructor also accepts `neighbor=None`. Return whether the target instance can be reached by repeatedly following the starting villager's neighbor.

**Approach:** Compare each current object to the target using `is`, then move to its neighbor. Stop at `None` or a previously visited object. A visited set prevents infinite loops if neighbor references form a cycle.

**Why it works:** The traversal follows the only available message route. For `r` distinct villagers visited, time and auxiliary space are O(r). Starting at the target returns `True`.

**Constructor versions in the Python file:** `BasicVillager` preserves the three-argument class for Problems 1–2. The final `Villager` class adds personality and neighbor for Problems 3–4 and inherits `add_item`.

## 5. Linked Up

Connect the provided `Node` instances to form `kk_slider -> harriet -> saharah -> isabelle`.

```python
kk_slider.next = harriet
harriet.next = saharah
saharah.next = isabelle
```

**Why it works:** Each next pointer references the required successor; Isabelle's next pointer remains `None`. The three assignments take O(1) time and auxiliary space. The provided printer produces `K.K. Slider -> Harriet -> Saharah -> Isabelle`.
