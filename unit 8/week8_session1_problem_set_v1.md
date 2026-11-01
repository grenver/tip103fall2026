# Unit 8 · Session 1 · Problem Set Version 1

Avatar dynamic programming. [Runnable solutions and labeled checks](week8_session1_problem_set_v1.py).

| Problem | Callable | Main concept | Prerequisite / explanation goal |
| --- | --- | --- | --- |
| [1. Spirit World Wisdom Pyramid](#problem-1-spirit-world-wisdom-pyramid) | `wisdom_pyramid` | Previous-row state | Explain why a separate next row avoids overwriting needed values |
| [2. Aang and Zuko's Elemental Duel](#problem-2-aang-and-zukos-elemental-duel) | `aang_wins` | Winning and losing states | Explain why leaving a losing position wins |
| [3. Iroh's Tea Brewing](#problem-3-irohs-tea-brewing) | `strongest_tea` | Maximum and minimum ending products | Explain why a negative product must be retained |
| [4. Toph and Katara's Training Synchronization](#problem-4-toph-and-kataras-training-synchronization) | `training_synchronization` | Two-dimensional prefix table | Distinguish subsequence from substring |
| [5. Aang's Airbending Journey](#problem-5-aangs-airbending-journey) | `aang_journey` | Reachability states | Distinguish a possible jump from an accessible starting point |

## Before starting: what is dynamic programming?

Dynamic programming stores answers to smaller questions so later questions can reuse them. A **state** says exactly what one stored answer means. A **transition** explains how to calculate it from earlier states. A **base case** supplies an answer that needs no earlier calculation.

For the pyramid, the smaller question is an earlier row. For the duel, it is whether a smaller strength wins. State meanings differ even when both solutions use lists. Build the state definition before writing a loop.

The Python files return answers; their final check blocks print check labels. Complexity below counts arithmetic as constant time, as usual in these exercises; very large Python integers take additional work.

## Problem 1: Spirit World Wisdom Pyramid

**Learning goal / clue:** Each number depends on the previous row's two neighbors, so retain that row while constructing the next one.

### U — Understand

`wisdom_pyramid(wisdomLevel)` returns the 0-indexed row of the Wisdom Pyramid. Assume `wisdomLevel` is a nonnegative integer. Row 0 is `[1]`; outside entries of every row are 1. Row 3 is `[1, 3, 3, 1]` and row 5 is `[1, 5, 10, 10, 5, 1]`.

### P — Plan

1. Start with `row = [1]`.
2. For each level through the requested level, create a new list of ones with one more position.
3. Fill each interior position with the sum of its two parents. Replace the old row only after finishing the new row.

**Trace:** `[1] → [1,1] → [1,2,1] → [1,3,3,1]`. At level 3, interior index 1 receives `1 + 2 = 3`; index 2 receives `2 + 1 = 3`. Both sums use the unchanged level-2 row.

**Why it works:** Initially the stored row is correct for level 0. If a stored row is correct, the stated parent-sum rule produces every interior value of the next row, while its edges remain 1. Each iteration advances one level, so the final row is the requested one.

**Try first:** Which two positions supply interior index `i`? Hint: look at indices `i-1` and `i` in the old row. Final hint: construct `next_row` separately before assigning it to `row`.

### I — Implement

<details>
<summary>Show solution</summary>

```python
def wisdom_pyramid(wisdomLevel):
    row = [1]
    for level in range(1, wisdomLevel + 1):
        next_row = [1] * (level + 1)
        for index in range(1, level):
            next_row[index] = row[index - 1] + row[index]
        row = next_row
    return row
```

</details>

**Code connection / checks:** `range(1, level)` visits only interior indices; the ending boundary is excluded. `row = next_row` moves the variable to the completed list. Checks cover supplied levels 0, 3, 5 and level 1, whose row has no interior entries.

**Cost:** For requested level `L`, O((L+1)²) time from constructing rows of lengths 1 through L+1, and O(L+1) peak space. The returned row has L+1 entries; the previous row and next row coexist during construction.

**Common mistakes:** Updating the old row from left to right → later sums read already changed values → build a separate row. Treating row 1 as the first row → off-by-one output → initialize row 0 before the loop.

**Interview explanation:** I store the previous correct row and use its adjacent values to build the next row. This follows the pyramid rule directly. Building all earlier rows takes quadratic time, while retaining only two rows takes linear space.

**Check your understanding:** What is row 2? How would you return all rows through level L?

<details>
<summary>Reasoning and answers</summary>

Row 2 is `[1,2,1]`. To return all rows, retain each completed row in an outer result list. That changes stored output space to O((L+1)²), because all row lengths add up.

</details>

## Problem 2: Aang and Zuko's Elemental Duel

**Learning goal / clue:** Optimal play asks whether any legal choice forces the opponent into a losing state. The same question recurs at smaller strengths.

### U — Understand

`aang_wins(n)` returns a Boolean for positive integer `n`. A legal move subtracts a positive proper divisor `x`: `x < n` and `n % x == 0`. A player unable to move loses. The supplied examples are `2 → True` and `3 → False`.

### P — Plan

1. Define `wins[s]` as whether the player whose turn begins at strength `s` can force a win. It refers to the current player, whichever character that is.
2. Strength 1 loses. Process larger strengths in increasing order.
3. Enumerate divisors up to the square root. Each divisor `d` supplies the paired divisor `s // d`; consider both if proper.
4. Mark `s` winning as soon as a move reaches any losing smaller state. If every move reaches a winning state, leave `s` losing.

**Trace:** `wins[1]=False`. At 2, subtract 1 to leave 1, so 2 wins. At 3, its only move leaves winning state 2, so 3 loses. At 4, subtract 1 to leave losing state 3, so 4 wins.

**Why it works:** Every move leaves a smaller positive strength, whose result has already been computed. If a losing successor exists, the current player chooses it. If none exists, the opponent can win after every choice. Divisors occur in pairs around the square root, so checking both members finds all legal moves. Finite loops complete the table through n.

**Try first:** If the opponent starts in a losing position, what does that mean for you? Hint: one such move suffices. Final hint: test `not wins[s-x]` for each legal `x`.

### I — Implement

<details>
<summary>Show solution</summary>

```python
def aang_wins(n):
    wins = [False] * (n + 1)
    for strength in range(2, n + 1):
        divisor = 1
        while divisor * divisor <= strength:
            if strength % divisor == 0:
                partner = strength // divisor
                if not wins[strength - divisor]:
                    wins[strength] = True
                    break
                if partner < strength and not wins[strength - partner]:
                    wins[strength] = True
                    break
            divisor += 1
    return wins[n]
```

</details>

**Code connection / checks:** `%` tests divisibility; `//` finds the paired integer divisor. `partner < strength` excludes subtracting the whole strength. Index 0 is unused for legal moves. Rechecking a square-root divisor is harmless. Checks cover 1, both supplied examples, and strengths 4 and 9.

**Cost:** O(n√n) time as an upper bound: each of n states tests at most √n candidates, with early stopping possible. O(n) auxiliary space stores the table. This is the cost of this DP implementation.

**Common mistakes:** Allowing `x=n` → an illegal move to 0 changes the game → exclude the full strength. Requiring all successors to lose → rejects valid winning choices → a single losing successor is sufficient.

**Interview explanation:** I define a state from the current player's perspective. A state wins exactly when it has a move to a losing state. Since every move reduces strength, a bottom-up table evaluates the dependencies in order, using O(n√n) time and O(n) space.

**Check your understanding:** Why does strength 5 lose? How would you return a winning move as well as a Boolean?

<details>
<summary>Reasoning and answers</summary>

At 5 only divisor 1 is legal, and it leaves winning state 4. To return a winning move, store the divisor whenever a losing successor is found; losing states have no such move.

</details>

## Problem 3: Iroh's Tea Brewing

**Learning goal / clue:** A negative factor reverses product order. Keep both the largest and smallest products ending at the current position.

### U — Understand

`strongest_tea(ingredients)` returns the largest product of a **nonempty contiguous** subarray. Assume the input list is nonempty; the prompt gives no empty-list result. Supplied examples: `[1,2,-3,4] → 4`, `[-2,-1] → 2`. Choosing nonconsecutive ingredients is not allowed.

### P — Plan

1. Initialize largest-ending, smallest-ending, and overall-best products to the first value.
2. For each next value, either start a new subarray with it or extend an old subarray ending immediately before it.
3. Compute both old extremes times the new value before changing either state. Their maximum and minimum, together with the new value itself, give the new extremes.
4. Update the best product seen anywhere.

**Trace:** For `[-2,3,-4]`:

| Value | Candidates ending here | Largest | Smallest | Best |
| --- | --- | --- | --- | --- |
| -2 | Initial value | -2 | -2 | -2 |
| 3 | 3, -6, -6 | 3 | -6 | 3 |
| -4 | -4, -12, 24 | 24 | -12 | 24 |

**Why it works:** Every subarray ending here either starts here or extends one ending immediately before. Multiplying by a positive value preserves order; multiplying by a negative value reverses it. Therefore the previous extremes contain all information needed to find the new extremes. Taking the largest over all ending positions covers every nonempty subarray. The loop advances through the finite list.

**Try first:** What happens to a very negative product when multiplied by a negative value? Hint: it can become the next maximum. Final hint: retain the previous minimum before updating the maximum.

### I — Implement

<details>
<summary>Show solution</summary>

```python
def strongest_tea(ingredients):
    largest = smallest = best = ingredients[0]
    for index in range(1, len(ingredients)):
        value = ingredients[index]
        extend_largest = largest * value
        extend_smallest = smallest * value
        largest = max(value, extend_largest, extend_smallest)
        smallest = min(value, extend_largest, extend_smallest)
        best = max(best, largest)
    return best
```

</details>

**Code connection / checks:** The two `extend_` variables preserve the previous state for both updates. A zero naturally permits a restart; no special zero branch is needed. Checks cover the supplied cases, two negatives separated by a positive, a zero, and a single negative.

**Cost:** For n ingredients, O(n) time and O(1) auxiliary space. Indexing avoids an O(n) copy from `ingredients[1:]`.

**Common mistakes:** Tracking only the largest product → loses the future benefit of a negative minimum → track both extremes. Initializing best to 0 → incorrectly returns 0 for `[-3]` → initialize from the first ingredient.

**Interview explanation:** I summarize subarrays ending at each index with their largest and smallest products. A new factor can start a subarray or extend either extreme. Retaining both handles sign reversals, yielding linear time and constant extra space.

**Check your understanding:** What is returned for `[-2,0,-1]`? How could you also return the chosen subarray's boundaries?

<details>
<summary>Reasoning and answers</summary>

The answer is 0: every positive-length subarray either has a negative product or includes zero. To return boundaries, track start indices with both ending extremes and record the current end index whenever the global best changes. Keep the starts paired with the old products during updates.

</details>

## Problem 4: Toph and Katara's Training Synchronization

**Learning goal / clue:** A subsequence preserves order but may skip characters. Since progress in each string matters independently, use two prefix lengths as the state.

### U — Understand

`training_synchronization(katara_moves, toph_moves)` returns the longest common subsequence (LCS) **length**, not the sequence. Empty strings are allowed and give length 0. Supplied examples: `("waterbend","earthbend") → 6`, `("bend","bend") → 4`, `("fire","air") → 2`. In the first example, `"erbend"` is a valid common subsequence; in the last, `"ir"` is valid.

### P — Plan

1. Let `dp[i][j]` mean the LCS length of the first i characters of Katara's string and the first j of Toph's.
2. Initialize row 0 and column 0 to zero: an empty prefix has no matching characters.
3. If the final characters match, extend the diagonal answer by 1.
4. Otherwise, skip the last character of one prefix and take the larger answer from above or left.

**Trace:** For `"ab"` and `"acb"`, the table is:

| Katara prefix \ Toph prefix | empty | a | ac | acb |
| --- | --- | --- | --- | --- |
| empty | 0 | 0 | 0 | 0 |
| a | 0 | 1 | 1 | 1 |
| ab | 0 | 1 | 1 | 2 |

At `(1,2)`, `a != c`, so keep max(0,1)=1. At `(2,3)`, both characters are `b`, so diagonal 1 becomes 2.

**Why it works:** Matching final characters can extend an LCS of the shorter prefixes. If the final characters differ, a common subsequence must omit at least one of those final characters, and the two skip cases cover those possibilities. Earlier table cells already solve those smaller questions. Increasing row and column indices visits every dependency before use and eventually reaches the full prefixes.

**Try first:** What should an empty-prefix cell contain? Hint: mismatching characters cannot both be the final match. Final hint: compare `dp[i-1][j]` and `dp[i][j-1]`.

### I — Implement

<details>
<summary>Show solution</summary>

```python
def training_synchronization(katara_moves, toph_moves):
    rows, columns = len(katara_moves), len(toph_moves)
    dp = [[0] * (columns + 1) for _ in range(rows + 1)]
    for row in range(1, rows + 1):
        for column in range(1, columns + 1):
            if katara_moves[row - 1] == toph_moves[column - 1]:
                dp[row][column] = dp[row - 1][column - 1] + 1
            else:
                dp[row][column] = max(dp[row - 1][column], dp[row][column - 1])
    return dp[rows][columns]
```

</details>

**Code connection / checks:** Table indices count prefix lengths, so character indices are one smaller. The comprehension creates independent rows. Checks cover all supplied examples, empty input, disjoint alphabets, and repeated characters.

**Cost:** With m and n the two string lengths, O((m+1)(n+1)) time and space, including initialization. For nonempty strings this is commonly written O(mn).

**Common mistakes:** Resetting to zero on mismatch → solves a different contiguous-substring problem → carry the larger neighboring answer. Using `[[0] * width] * height` → rows share one list → construct each row separately.

**Interview explanation:** Each cell answers the LCS question for two prefixes. Matching characters extend the diagonal; otherwise I keep the better result from skipping one character. The table gives the full answer in O(mn) time and space for nonempty strings.

**Check your understanding:** Why does `("abc","ac")` return 2? How would you recover an actual subsequence?

<details>
<summary>Reasoning and answers</summary>

`"ac"` appears in order in both strings, even though `b` is skipped in the first. To recover a sequence, walk backward from the last table cell: take a matching character and move diagonally, or move to a neighboring cell that preserves the LCS length. Reverse the collected characters at the end.

</details>

## Problem 5: Aang's Airbending Journey

**Learning goal / clue:** Reaching a platform depends on whether an earlier reachable platform can jump far enough. Store a Boolean answer for each destination.

### U — Understand

`aang_journey(platforms)` returns whether index n-1 is reachable from index 0. Assume a nonempty list of nonnegative integers. A value is a **maximum** forward distance; a shorter jump is allowed. The prompt does not define empty input. Supplied cases are `[2,3,1,1,4] → True` and `[3,2,1,0,4] → False`.

### P — Plan

1. Mark index 0 reachable because Aang starts there.
2. For each later destination, inspect earlier starting indices.
3. If an earlier start is reachable and `start + platforms[start] >= destination`, mark the destination reachable and stop searching for another witness.
4. Return the reachability of the last platform.

**Trace:** In `[3,2,1,0,4]`, indices 1, 2, 3 become reachable from index 0. For destination 4, every reachable start has maximum endpoint at most 3. The value 4 at index 4 cannot help Aang arrive there, so the result is False.

**Why it works:** Any path to a later destination must end with a jump from a reachable earlier platform. The inner loop checks every such possible last jump. Conversely, finding one gives a real path. Processing destinations in order ensures earlier reachability answers are complete; both loops are finite.

**Try first:** Does a long jump at an unreachable platform help? Hint: a valid transition needs two conditions. Final hint: combine `reachable[start]` with the endpoint comparison.

### I — Implement

<details>
<summary>Show solution</summary>

```python
def aang_journey(platforms):
    reachable = [False] * len(platforms)
    reachable[0] = True
    for destination in range(1, len(platforms)):
        for start in range(destination):
            if reachable[start] and start + platforms[start] >= destination:
                reachable[destination] = True
                break
    return reachable[-1]
```

</details>

**Code connection / checks:** `break` stops only the inner loop after finding a valid last jump. `reachable[-1]` reads the last platform's state. Checks cover both supplied examples, an already-finished one-platform journey, an initial zero that blocks progress, and jumping directly over a zero.

**Cost:** For n platforms, O(n²) worst-case time from checking up to `1+2+...+(n-1)` possible jumps, and O(n) auxiliary space. This implementation uses a reachability table to teach DP.

**Common mistakes:** Always jumping the maximum → can miss a useful shorter landing → test reachability rather than committing to that route. Using an unreachable start → invents a path → require its Boolean state to be True. Treating every zero as fatal → ignores paths over it → check whether the destination can be reached.

**Interview explanation:** I mark each position reachable when an already reachable earlier position can jump to it. This accounts for every possible final jump into a destination. The final Boolean answers the problem, using O(n²) time and O(n) space.

**Check your understanding:** Why is `[0]` True? How could the table also produce one route?

<details>
<summary>Reasoning and answers</summary>

Aang starts on the final platform, so no jump is necessary. To produce a route, record the earlier start when each destination first becomes reachable. Follow these predecessor indices backward from the last index, then reverse the route.

</details>
