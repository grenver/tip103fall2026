# Unit 9 · Session 1 · Problem Set Version 1

Greedy algorithms. [Python solutions and runnable checks](week9_session1_problem_set_v1.py).

| Problem | Callable | Greedy choice |
| --- | --- | --- |
| 1. Non-overlapping Intervals | `erase_overlap_intervals` | Keep the compatible booking that ends first |
| 2. Gas Station | `can_complete_circuit` | Discard an entire failed range of starting stations |
| 3. Assign Cookies | `find_content_children` | Give the least demanding child the smallest fitting cookie |
| 4. Jump Game II | `jump` | Expand the farthest reachable boundary for each jump |
| 5. Partition Labels | `partition_labels` | Close each piece at the earliest valid boundary |

## Before starting: when is greedy safe?

A greedy algorithm commits to a choice using the current situation. A locally appealing choice needs a reason that it preserves a globally optimal answer. Useful arguments include exchanging the first choice in an optimal solution, proving discarded candidates cannot work, and maintaining a boundary that represents every possibility at the current cost.

Greedy can fail: with coin denominations `[1, 3, 4]` and amount 6, taking the largest available coin gives `4 + 1 + 1` (three coins), while `3 + 3` uses two. Dynamic programming can compare alternatives by defining `dp[a]` as the fewest coins for amount `a`, with `dp[0] = 0` and `dp[a] = min(dp[a-c] + 1)` over available coins `c <= a` with reachable remainders.

Minimum spanning trees are part of the session overview, but no MST problem was supplied. The key idea is the **cut property**: a minimum-weight edge across a cut that respects the edges already chosen is safe to add to some MST. Kruskal's algorithm considers edges by increasing weight and skips cycles; Prim's algorithm grows one connected component using its cheapest outgoing edge. These solve minimum total connection cost in a connected, undirected weighted graph. They do not generally find shortest paths from a source.

Use UMPIRE in discussion: **Understand** the result and constraints, **Match** a pattern, **Plan** the invariant, **Implement**, **Review** with examples, and **Evaluate** time and space. Each section below follows those steps. Implementations are in the linked Python file; they do not mutate input lists. Complexity assumes constant-time arithmetic and comparisons.

## Problem 1: Non-overlapping Intervals

### Understand

Given `[start, end]` conference-room bookings, return the minimum number to cancel so the remaining bookings do not overlap. Assume valid intervals with `start < end`. Touching endpoints are allowed: `[1, 2]` and `[2, 3]` can both remain.

Examples: `[[1,2],[2,3],[3,4],[1,3]] -> 1`; three copies of `[1,2] -> 2`; `[[1,2],[2,3]] -> 0`. Empty input returns 0.

### Match and approach

This is interval scheduling: minimizing cancellations equals maximizing the number kept. Sort by ending time. Track the end of the last kept booking. Keep an interval if its start is at least that end; otherwise count a cancellation. Initially the end is negative infinity so the first interval fits.

**Trace:** For `[[1,10],[2,3],[3,4]]`, the sorted order is `[2,3], [3,4], [1,10]`. Keep the first two and cancel the last: answer 1. Taking the earliest start would keep `[1,10]` and require two cancellations.

**Why it works:** Replace the first booking of any optimal compatible schedule with a globally earliest-finishing booking. The replacement ends no later, so every later booking still fits. Apply the same exchange argument to the compatible remaining bookings. Thus the greedy schedule keeps the maximum number.

### Implement, review, and evaluate

Use `erase_overlap_intervals` in the Python companion. `sorted(..., key=lambda interval: interval[1])` creates a new order without changing the caller's list. An overlap leaves `previous_end` unchanged because the earlier-finishing booking is retained.

For `n` intervals: **O(n log n) time**, dominated by sorting; **O(n) auxiliary space** for the sorted copy and Python's sorting workspace.

**Common mistake:** Using `start > previous_end` cancels bookings whose endpoints merely touch. Use `>=`.

**Interview explanation:** “I maximize bookings kept by always choosing the earliest compatible finish, leaving as much room as possible for later bookings.”

## Problem 2: Gas Station

### Understand

Stations form a circle. `gas[i]` is collected at station `i`; `cost[i]` pays for the next leg. Return a starting index that completes one clockwise circuit, or -1. Start with an empty tank, and assume unlimited tank capacity, equal-length arrays, and nonnegative fuel/cost values. The prompt guarantees uniqueness when a solution exists. For empty arrays, this implementation returns -1.

Examples: `gas=[1,2,3,4,5], cost=[3,4,5,1,2] -> 3`; `gas=[2,3,4], cost=[3,4,3] -> -1`.

### Match and approach

Track `total`, the net fuel over all stations, and `tank`, the net fuel since the candidate start. Add `gas[i] - cost[i]` to both. When `tank < 0`, discard every candidate from the current start through `i`, reset the tank, and try `i + 1`. At the end, reject if `total < 0`; otherwise return the candidate.

**Trace:** The first sample has net fuel `[-2,-2,-2,3,3]`. Starts 0, 1, and 2 each fail immediately. Starting at 3 gives tank values `3,6,4,2,0` around the circle, so the answer is 3.

**Why it works:** Before the first failure from candidate `s`, every partial sum from `s` is nonnegative. For any `k` between `s` and failing index `i`, the net fuel from `k` through `i` equals the negative failed sum minus a nonnegative prefix, so `k` also fails. The final candidate follows a minimum prefix sum of the net-fuel sequence. Later prefixes cannot fall below that minimum, and the wrapped section remains nonnegative when the total sum is nonnegative. A negative total is impossible from any start.

### Implement, review, and evaluate

Use `can_complete_circuit`. Notice that `total` is never reset; it answers whether the whole trip is possible. Only the candidate's `tank` resets.

For `n` stations: **O(n) time**, one scan; **O(1) auxiliary space**.

**Common mistakes:** Choosing the largest individual gas amount ignores travel costs. Resetting the total loses the impossibility check. A zero tank is allowed; reset only when negative.

**Interview explanation:** “A failed segment eliminates all starts within it. The total fuel balance then decides whether the remaining candidate can complete the circle.”

## Problem 3: Assign Cookies

### Understand

Each child needs a cookie of size at least their greed factor. Each cookie and child can participate in at most one assignment. Maximize the number satisfied; cookies cannot be combined or split. Empty children or cookies means answer 0.

Examples: `g=[1,2,3], s=[1,1] -> 1`; `g=[1,2], s=[1,2,3] -> 2`.

### Match and approach

Sort both lists in ascending order. Keep a pointer to the least demanding unsatisfied child. Scan cookies from smallest to largest. If a cookie fits, satisfy that child and advance the pointer. Otherwise discard the cookie: it cannot fit any remaining child.

**Trace:** `g=[3,1,2]`, `s=[3,1]` becomes children `[1,2,3]` and cookies `[1,3]`. Cookie 1 satisfies child 1; cookie 3 satisfies child 2. Answer 2.

**Why it works:** Let `c` be the smallest cookie fitting the least demanding child `g`. In an optimal assignment where that child receives a larger cookie, swapping in `c` cannot hurt: any child previously receiving `c` also accepts the larger cookie. If `g` is unsatisfied while `c` is used for someone else, reassigning `c` to `g` preserves the count. Thus some optimal assignment contains the greedy pair; repeat for the rest.

### Implement, review, and evaluate

Use `find_content_children`. The pointer value is both the next child index and the number already satisfied. Stop once all children are satisfied.

For `n` children and `m` cookies: **O(n log n + m log m) time** for sorting and a linear scan; **O(n + m) auxiliary space** for sorted copies/workspace.

**Common mistake:** Giving a very large cookie to a low-demand child before checking smaller cookies can waste a cookie needed by another child.

**Interview explanation:** “I satisfy the easiest remaining child with the smallest cookie that works, preserving larger cookies for harder children.”

## Problem 4: Jump Game II

### Understand

At index `i`, jump forward by up to `nums[i]` positions. Return the minimum jumps from index 0 to the final index. Assume a nonempty list of nonnegative integers and a reachable destination. This function does not detect unreachable inputs. A one-element array needs zero jumps.

Examples: `[2,3,1,1,4] -> 2`; `[2,3,0,1,4] -> 2`.

### Match and approach

Think of breadth-first search layers, where one layer means one additional jump. `current_end` is the farthest boundary reachable with the counted jumps. While scanning that range, `farthest` records the largest next boundary available from any scanned position. At `current_end`, count one more jump and expand the boundary to `farthest`.

```text
nums = [2, 3, 1, 1, 4]
0 jumps: index 0
1 jump:  indices 1..2    (0 reaches 2)
2 jumps: indices 3..4    (1 reaches 4)
```

**Why it works:** Every position in the current range is reachable using at most the current number of jumps. Scanning all of them finds the farthest boundary possible with one additional jump. No smaller jump count reaches beyond the current boundary. Expanding layers therefore finds the minimum count, as BFS does, without storing a queue.

### Implement, review, and evaluate

Use `jump`. Scan through `len(nums) - 2`; reaching the destination requires no jump out of it. `farthest` is an index, so compute `index + nums[index]`.

For `n` positions: **O(n) time**, **O(1) auxiliary space**.

**Common mistake:** Jumping to the position with the largest value ignores its index. Evaluate its total reach instead, and consider all positions in the current layer.

**Interview explanation:** “I count reachable layers. Each boundary expansion is exactly one jump, and I use all positions in a layer to maximize the next boundary.”

## Problem 5: Partition Labels

### Understand

Split a string into as many contiguous pieces as possible. A letter may repeat inside its piece but cannot occur in multiple pieces. Return piece lengths, preserving order. Empty input returns `[]`.

Examples: `"ababcbacadefegdehijhklij" -> [9,7,8]`; `"eccbbbbdec" -> [10]`.

### Match and approach

First map every character to its last occurrence. Scan a candidate piece, extending `end` to the greatest last occurrence of any character encountered. When the scan reaches `end`, every letter in the piece is finished, so close it immediately. Its length is `end - start + 1`.

**Trace:** For `"abac"`, `last={a:2,b:1,c:3}`. Seeing `a` forces the first piece through index 2. At index 2 close `"aba"`; index 3 closes `"c"`. Answer `[3,1]`.

**Why it works:** A boundary before `end` would split some encountered letter across pieces, so it is invalid. At `end`, no character in the piece occurs later, so the cut is safe. Cutting at this earliest safe position preserves every later opportunity for a cut and maximizes the number of pieces.

### Implement, review, and evaluate

Use `partition_labels`. `end = max(end, last[letter])` preserves earlier requirements; a later letter cannot shorten the piece.

For length `n`, with `k` distinct characters and `p` output pieces: **O(n) time**, **O(k) auxiliary space**, plus **O(p) output space**. For a fixed lowercase-English alphabet, the map uses O(1) space; the returned list can still use O(n).

**Common mistakes:** Cutting after the current character's final occurrence without honoring other letters already in the piece; forgetting the `+1` for inclusive endpoints.

**Interview explanation:** “Every character extends a required endpoint. I close the piece as soon as the scan meets all those requirements.”

## Run the checks

From the repository root:

```powershell
python "unit 9/week9_session1_problem_set_v1.py"
```

The assertions cover every supplied example, touching/contained intervals, impossible fuel totals, empty assignments, single-position jumps, and repeated or distinct letters.
