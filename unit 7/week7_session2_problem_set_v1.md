# Unit 7 · Session 2 · Problem Set Version 1

Binary search: discard half the candidates using sorted order. Runnable solutions and labeled checks: [Python file](week7_session2_problem_set_v1.py).

| Problem | Callable | Main concept | Prerequisite / explanation goal |
| --- | --- | --- | --- |
| [1. Find Millenium Falcon Part I](#problem-1-find-millenium-falcon-part-i) | `check_stock` | Iterative membership | Explain which half can be discarded |
| [2. Find Millenium Falcon Part II](#problem-2-find-millenium-falcon-part-ii) | `check_stock_recursive` | Recursive membership | Explain base case and shrinking bounds |
| [3. Find First and Last Frequency Positions](#problem-3-find-first-and-last-frequency-positions) | `find_frequency_positions` | Two boundary searches | Continue searching after equality |
| [4. Smallest Letter Greater Than Target](#problem-4-smallest-letter-greater-than-target) | `next_greatest_letter` | Strict upper boundary | Explain duplicates and wraparound |
| [5. Find K Closest Planets](#problem-5-find-k-closest-planets) | `find_closest_planets` | Search window starts | Explain ties and output-copy cost |

## Shared prerequisite: bounds and sorted order

Binary search needs a decision that lets us reject a whole side. In `[1,2,5,12,20]`, if the middle value 5 is smaller than target 20, everything at or left of 5 is too small. Checking each item would be O(n); halving the candidate range needs O(log n) comparisons for n items.

Problems 1–2 use an inclusive range `[left, right]`: both endpoints are candidates, and `left > right` means empty. Problems 3–4 use `[left, right)`, where right is excluded; `right = n` is safe because a midpoint is always below right while `left < right`. They find insertion positions, which can equal n. Problem 5 instead searches possible starts of a fixed-length window.

Both supplied stock prompts use `check_stock`. Here Problem 1 retains that name and Problem 2 uses `check_stock_recursive` to preserve both implementations. For a standalone Problem 2 submission, rename its outer function to `check_stock`.

## Problem 1: Find Millenium Falcon Part I

**Learning goal / recognition clue:** Use sorted order to answer membership in logarithmic time, with a loop.

### U — Understand

`check_stock(inventory, part_id)` returns `True` or `False`, without changing the sorted list of integer IDs. `[1,2,5,12,20]` contains 20 but does not contain 100. Duplicates do not change the membership question.

### P — Plan

1. Set inclusive bounds to 0 and n−1.
2. Inspect the midpoint. Return `True` on equality; otherwise discard the midpoint and the impossible half.
3. Return `False` when the bounds cross.

**Trace:** Searching for 20: `(left,right,middle)=(0,4,2)` gives value 5, so left becomes 3. `(3,4,3)` gives 12, so left becomes 4. `(4,4,4)` finds 20.

**Why it works:** If the target exists and has not been found, an occurrence stays inside the current bounds. Sorted order justifies each discard. Excluding the tested midpoint strictly shrinks the range, so the loop stops.

**Try first:** What does a middle value smaller than the target tell you? Next hint: no value to its left can match. Final hint: update left to `middle + 1`.

### I — Implement

<details>
<summary>Show solution</summary>

```python
def check_stock(inventory, part_id):
    left, right = 0, len(inventory) - 1
    while left <= right:
        middle = (left + right) // 2
        if inventory[middle] == part_id:
            return True
        if inventory[middle] < part_id:
            left = middle + 1
        else:
            right = middle - 1
    return False
```

</details>

**Code connection / checks:** `//` gives an integer midpoint. `left <= right` still checks a one-element range. Checks cover both examples, empty input, a single matching item, and duplicates.

**Cost:** For n inventory items, O(log(n+1)) time (usually written O(log n)) and O(1) auxiliary space: only a few indices are stored.

**Common mistakes:** Using `left < right` with these inclusive bounds skips the final candidate → include equality. Updating left to middle can stall → discard the tested midpoint.

**Interview explanation:** I compare the target with the middle item and discard the half that sorted order rules out. Every step halves the remaining range; crossing the bounds proves absence. The loop uses logarithmic time and constant space.

**Check your understanding:** What is returned for an empty list? Could the same decisions safely search an unsorted list?

<details>
<summary>Reasoning and answers</summary>

False: right starts at −1, so the loop never runs. No: a matching item could be in the discarded half of an unsorted list.

</details>

## Problem 2: Find Millenium Falcon Part II

**Learning goal / recognition clue:** Translate shrinking loop state into recursive parameters without copying sublists.

### U — Understand

The required standalone callable is again `check_stock(inventory, part_id)`; this combined file names it `check_stock_recursive`. It has the same inputs and Boolean outputs as Problem 1. Because Part I is iterative, Part II must be recursive.

### P — Plan

1. Define a nested helper receiving left and right bounds; it can read the outer inventory and target.
2. Return `False` for an empty range, or `True` for a midpoint match.
3. Otherwise return the result of searching just the possible half.

**Trace:** Searching for 100 in `[1,2,5,12,20]` calls `search(0,4)`, `search(3,4)`, `search(4,4)`, then `search(5,4)`. The last call returns False; each waiting call returns that same result.

**Why it works:** The retained range obeys the same membership rule as Part I. Each call makes the range smaller. Eventually a match or the empty-range base case stops the recursion.

**Try first:** Which loop variables change? Next hint: make those variables helper parameters. Final hint: return each recursive result so it reaches the caller.

### I — Implement

<details>
<summary>Show solution</summary>

```python
def check_stock_recursive(inventory, part_id):
    def search(left, right):
        if left > right:
            return False
        middle = (left + right) // 2
        if inventory[middle] == part_id:
            return True
        if inventory[middle] < part_id:
            return search(middle + 1, right)
        return search(left, middle - 1)

    return search(0, len(inventory) - 1)
```

</details>

**Code connection / checks:** The nested function reads inventory without receiving a copied slice. The outer `return search(...)` returns the helper's Boolean to the caller. Checks cover both supplied examples, empty input, a one-item miss, and duplicates.

**Cost:** For n items, O(log(n+1)) time and O(log(n+1)) auxiliary stack space for n>=1, with O(1) for an empty list. Python keeps a call frame for every waiting recursive call.

**Common mistakes:** Omitting `return` before a recursive call loses the result → propagate it. Recursing on slices copies data → use indices to keep logarithmic time.

**Interview explanation:** The recursive helper carries the same bounds as the iterative search. Each call either answers the question or returns the answer from one half-sized range. Bounds avoid slicing, while the stack adds logarithmic space.

**Check your understanding:** Why check for an empty range before indexing? Is recursive binary search O(1) space in Python?

<details>
<summary>Reasoning and answers</summary>

An empty range has no valid midpoint to inspect. Python retains the waiting calls, so stack space grows logarithmically; it does not eliminate these tail calls.

</details>

## Problem 3: Find First and Last Frequency Positions

**Learning goal / recognition clue:** Search for boundaries rather than any occurrence when repeated values require exact first and last positions.

### U — Understand

`find_frequency_positions(transmissions, target_code)` returns an index tuple. For `[5,7,7,8,8,10]`, target 8 returns `(3,4)` and target 6 returns `(-1,-1)`. Empty input returns `(-1,-1)`. The total search must stay O(log n).

### P — Plan

1. Binary-search the first position with value >= target (lower boundary).
2. If that position is n or does not match, return `(-1,-1)`.
3. Binary-search the first position with value > target (upper boundary). Return lower and upper−1.

**Trace:** For target 8, the lower search visits midpoint indices 3 (8: move right bound to 3), 1 (7: move left to 2), and 2 (7: move left to 3). It ends at 3. The upper search treats equality as “move left bound forward” and ends at index 5, whose value is 10. Return `(3,5−1)`.

**Why it works:** For the lower search, all indices before left are too small and all indices at or after right satisfy >= target. For the upper search replace these tests with <= and >. Each midpoint decision preserves these facts and shrinks the range until the boundary is fixed. Equal values occupy one contiguous block in a sorted array.

**Try first:** Why is finding one 8 insufficient? Next hint: equality must guide a further search. Final hint: find the first >= 8 and the first > 8 separately.

### I — Implement

<details>
<summary>Show solution</summary>

```python
def find_frequency_positions(transmissions, target_code):
    def boundary(strict):
        left, right = 0, len(transmissions)
        while left < right:
            middle = (left + right) // 2
            if transmissions[middle] < target_code or (
                strict and transmissions[middle] == target_code
            ):
                left = middle + 1
            else:
                right = middle
        return left

    first = boundary(False)
    if first == len(transmissions) or transmissions[first] != target_code:
        return (-1, -1)
    return (first, boundary(True) - 1)
```

</details>

**Code connection:** `strict=False` finds >= target; `strict=True` skips equal values and finds > target. The `or` in the absence test short-circuits: when first equals n, Python never evaluates the invalid indexing expression.

**Checks / cost:** Checks cover all supplied examples, an all-equal list, and one match. For n transmissions, two logarithmic searches give O(log(n+1)) time and O(1) auxiliary space. Two searches do not multiply into O(log² n); their costs add.

**Common mistakes:** Scanning outward from a match takes O(n) for all-equal input → binary-search both boundaries. Returning the upper insertion index includes the next value → subtract one.

**Interview explanation:** I locate the two edges of the target's contiguous block through lower and upper boundary searches. I check that the lower boundary actually matches, then subtract one from the upper boundary. Both searches together remain logarithmic.

**Check your understanding:** What is the upper boundary if every value equals the target? How would you return the number of matches?

<details>
<summary>Reasoning and answers</summary>

It is n, one position beyond the list. The number of matches is upper−lower; if using the returned inclusive indices, use last−first+1 after checking that first is not −1.

</details>

## Problem 4: Smallest Letter Greater Than Target

**Learning goal / recognition clue:** Find a strictly greater value by moving past all equal values, then handle wraparound.

### U — Understand

`next_greatest_letter(letters, target)` returns a character from the sorted nonempty list. The prompt guarantees at least two different characters. For `['a','a','b','c','c','c','e','h','w']`, targets a, d, and y return b, e, and a respectively. Equality is not enough.

### P — Plan

1. Search for the first letter greater than target, using half-open bounds.
2. If the middle letter is <= target, discard it and everything before it.
3. Otherwise keep it as a possible answer and continue left. If the boundary is n, wrap to index 0.

**Trace:** For target d, `(left,right,middle)=(0,9,4)` gives c, so left=5. `(5,9,7)` gives h, so right=7. `(5,7,6)` gives e, so right=6. `(5,6,5)` gives c, so left=6. Return e. For target y all letters are too small, so the final index is 9 and wraps to 0.

**Why it works:** All rejected left-side letters are <= target. The first valid letter remains within the boundary search, and each step shrinks the range. The boundary is n exactly when no greater letter exists.

**Try first:** Should a middle letter equal to the target be kept? Next hint: strict inequality rejects it. Final hint: use `<=` to move left forward.

### I — Implement

<details>
<summary>Show solution</summary>

```python
def next_greatest_letter(letters, target):
    left, right = 0, len(letters)
    while left < right:
        middle = (left + right) // 2
        if letters[middle] <= target:
            left = middle + 1
        else:
            right = middle
    return letters[left % len(letters)]
```

</details>

**Code connection / checks:** `% len(letters)` keeps indices 0..n−1 unchanged and maps n to 0. Nonempty input makes this safe. Checks cover the examples, target equal to the largest letter, and target smaller than every letter.

**Cost:** Let n=len(letters). Each iteration halves the candidate range, giving O(log n) time. Only three indices are stored, so auxiliary space is O(1); the returned character uses constant space.

**Common mistakes:** Searching for >= can return the target itself → discard equality. Indexing directly at n raises an error → wrap around.

**Interview explanation:** I find the upper insertion boundary, skipping all values <= target. It identifies the smallest strictly greater letter. If it reaches n, I return the first letter as required. The search takes logarithmic time and constant space.

**Check your understanding:** What is returned when target equals w in the example? What comparison would change if equality were allowed?

<details>
<summary>Reasoning and answers</summary>

a: w is not strictly greater than itself. To find the first value >= target instead, move left forward only when the middle value is < target.

</details>

## Problem 5: Find K Closest Planets

**Learning goal / recognition clue:** Search a contiguous length-k window in sorted input, with equality favoring smaller values.

### U — Understand

`find_closest_planets(planets, target_distance, k)` returns k values in ascending order, without changing the input. Smaller absolute distance wins; equal distances favor the smaller planet value. Assume integer k with 0 <= k <= n; k=0 returns `[]`. For `[100,200,300,400,500]`, target 350 and k=3 return `[200,300,400]`. For `[10,20,30,40,50]`, target 25 and k=2 return `[20,30]`.

### P — Plan

1. Search possible window starts from 0 to n−k.
2. At a candidate start m, compare the outgoing value `planets[m]` with the incoming value `planets[m+k]` of the window shifted one step right.
3. If `target - planets[m] > planets[m+k] - target`, shift the search right. Otherwise keep m and search left, preserving smaller values on ties.
4. Copy the k values starting at the final index.

**Trace:** For `[100,200,300,400,500]`, target 350, k=3, possible starts are 0..2. At m=1, compare 350−200=150 with 500−350=150: equality keeps the left window, so right=1. At m=0, compare 250 with 50: shift left bound to 1. Return indices 1..3: `[200,300,400]`.

**Why a window works:** In sorted order, an intermediate value between two chosen endpoints is at least as close as one of those endpoints. Thus the k best values can be represented by a contiguous window, with duplicates interchangeable.

**Why the search works:** As m increases, `target - planets[m]` never increases while `planets[m+k] - target` never decreases. The “shift right” condition is therefore true for an initial range of starts and false afterward. When it is true, a rightward replacement is preferable (or exchanges equal values). When false, the left window is at least as good; ties must favor the smaller values. Searching the transition finds an optimal start. Each update shrinks the start range.

The signed differences are intentional. If the target lies left of both compared values, the left window is preferred; if it lies right of both, the right window is preferred. Equal duplicate values can be exchanged without changing the result. Do not replace the expression mechanically with absolute values: the monotone signed comparison handles duplicates outside the target correctly.

**Try first:** Could the best k values skip a better value between them? Next hint: compare adjacent windows that differ at only two endpoints. Final hint: binary-search the start using those outgoing and incoming values.

### I — Implement

<details>
<summary>Show solution</summary>

```python
def find_closest_planets(planets, target_distance, k):
    if k == 0:
        return []
    left, right = 0, len(planets) - k
    while left < right:
        middle = (left + right) // 2
        if target_distance - planets[middle] > planets[middle + k] - target_distance:
            left = middle + 1
        else:
            right = middle  # Equality keeps the smaller-valued window.
    return planets[left:left + k]
```

</details>

**Code connection / checks:** While left < right, middle < n−k, so middle+k is a valid index. Equality goes to `right = middle`, preserving the smaller window. The final slice copies k values already in order. Checks cover both examples, an exact distance tie, targets outside the input range, duplicates, k=n, and k=0.

**Cost:** Let n=len(planets) and k be the number returned. There are n−k+1 possible starts; searching costs O(log(n−k+1)) comparisons, and copying the output costs O(k). Total time is O(log(n−k+1)+k), with constant overhead for trivial cases. Auxiliary working space is O(1), excluding the O(k) returned list. Claiming only O(log n) ignores the cost of returning k values.

**Common mistakes:** Choosing the right window on ties can prefer larger values → move right only for strict `>`. Sorting all planets by distance adds unnecessary work and loses ascending value order → search a window in the existing order. Ignoring the slice underestimates time and output space → include O(k).

**Interview explanation:** Sorted order guarantees an optimal contiguous length-k window. I binary-search its start by comparing the value removed on the left with the one added on the right, favoring the left on ties. I then copy that window, so the cost includes both the logarithmic search and k output values.

**Check your understanding:** For `[1,2,3,4]`, target 2.5 and k=1, which value wins? Why is k=n an O(n) operation despite needing no search?

<details>
<summary>Reasoning and answers</summary>

2 wins the distance tie against 3 because it is smaller. When k=n, there is only one possible window, but copying all n elements still costs O(n).

</details>

## Run the checks

From the repository root, run `python "unit 7/week7_session2_problem_set_v1.py"` using the selected Python interpreter. A successful run prints five labeled passing messages. All functions return results; the checks print confirmations.
