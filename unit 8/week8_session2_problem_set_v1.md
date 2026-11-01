# Unit 8 · Session 2 · Problem Set Version 1

Backtracking: build a partial answer, explore a choice, then undo it. [Runnable solutions and labeled checks](week8_session2_problem_set_v1.py).

| Problem | Callable | Main concept | Prerequisite / explanation goal |
| --- | --- | --- | --- |
| [1. Subsets](#problem-1-subsets) | `subsets` | Increasing choice indices | Explain why every partial path is an answer |
| [2. Permutations](#problem-2-permutations) | `permute` | Used-item state | Explain why earlier unused items remain available |
| [3. Combination Sum](#problem-3-combination-sum) | `combination_sum` | Reuse with a remaining target | Explain same-index recursion without duplicate orderings |
| [4. Generate Parentheses](#problem-4-generate-parentheses) | `generate_parentheses` | Valid-prefix constraints | Explain why a closing parenthesis needs an unmatched opening one |
| [5. Letter Combinations of a Phone Number](#problem-5-letter-combinations-of-a-phone-number) | `letter_combinations` | One choice per input position | Explain how recursion advances to the next digit |

## Before starting: recursion and undoing a choice

A recursive helper explores the choices available from one partial answer. A **base case** stops a branch. Each call has its own parameters, but the helpers here share the outer `path` list and `result` list.

The repeated steps are:

```python
path.append(choice)  # Temporarily include this choice.
search(next_state)   # Explore everything that begins with this path.
path.pop()           # Remove the last item before trying a sibling choice.
```

`append()` changes the list and returns `None`. `pop()` removes and returns its last item; here we only need its removal effect. When a nested call returns, execution resumes at the next line in its caller. That is when the caller undoes its choice.

`result.append(path.copy())` saves a separate list. Saving `path` directly would save repeated references to one changing list. Strings built with `"".join(path)` are independent immutable values, so they do not need a list copy.

Different problems change which choices are legal and when an answer is complete. These inputs are small enough for enumeration: producing exponentially many answers necessarily takes substantial work. Auxiliary-space costs below exclude the returned answers but include recursive calls.

## Problem 1: Subsets

**Learning goal / clue:** A loadout may contain any selection, including none. Each partial selection is already a valid answer. Distinct items let us avoid duplicates by choosing indices in increasing order.

### U — Understand

`subsets(nums)` returns a list of all subsets of distinct integers. Input order is preserved within each returned subset; this is a representation choice, not a requirement to sort the input. The example is:

```python
subsets([1, 2, 3])
# [[], [1], [1, 2], [1, 2, 3], [1, 3], [2], [2, 3], [3]]
```

The input is not changed. For empty input, the only subset is the empty one: `[[]]`.

### P — Plan

1. Keep a current `path` and a result list. Call `search(0)`.
2. Save a copy of the current path immediately, including the initial empty path.
3. Try each index from `start` onward. Append that item, recurse with the following index, then pop the item.

**Trace:** With `[1,2]`: save `[]`; choose 1 and save `[1]`; choose 2 and save `[1,2]`; pop 2, then pop 1. The initial call next chooses 2 and saves `[2]`. It finishes with `path=[]` and four independent answers.

**Why it works:** Every subset has exactly one increasing sequence of input indices. Each call explores every possible next index, so every subset is reached once. Recursing with `index+1` prevents both reuse and reversed duplicates. The index strictly increases along a branch, so recursion ends.

**Try first:** Is an unfinished loadout still a subset? Hint: save a path before extending it. Final hint: pass `index+1` so a chosen item cannot appear again.

### I — Implement

<details>
<summary>Show solution</summary>

```python
def subsets(nums):
    result = []
    path = []

    def search(start):
        result.append(path.copy())
        for index in range(start, len(nums)):
            path.append(nums[index])
            search(index + 1)
            path.pop()

    search(0)
    return result
```

</details>

**Code connection / checks:** `start` is the first permitted index, not a count of answers. An empty `range` ends a branch naturally; no separate base-case `return` is needed. Checks cover the supplied full output, empty input, and a singleton.

**Cost:** For n items, there are 2ⁿ subsets, containing n·2ⁿ⁻¹ total elements when n≥1. Time and returned space are O((n+1)2ⁿ), including copying and list overhead. Auxiliary space is O(n+1) for the path and recursive calls.

**Common mistakes:** Saving `path` without copying → stored answers change during undo → use `path.copy()`. Restarting the loop at 0 → revisits earlier items and duplicates selections → respect `start`.

**Interview explanation:** I save every partial selection and extend it only with later input items. Every subset has one increasing index representation, which makes enumeration complete and duplicate-free. Copying the answers takes O(n2ⁿ) time for nonempty input, with O(n) auxiliary space.

**Check your understanding:** What does `subsets([])` return? If the input were `[1,1]`, would increasing indices remove duplicate value-subsets?

<details>
<summary>Reasoning and answers</summary>

It returns `[[]]`, because the initial empty path is saved. Increasing indices distinguish positions, not equal values, so `[1,1]` would produce `[1]` twice. Repeated input values would require additional duplicate handling; this prompt guarantees distinct integers.

</details>

## Problem 2: Permutations

**Learning goal / clue:** Every ordering uses every item once. Unlike subsets, a later choice may use an earlier input index as long as it has not been used in this path.

### U — Understand

`permute(nums)` returns all full orderings of distinct integers. Order of the returned answers is unrestricted. The input is unchanged.

```python
permute([1, 2, 3])
# [[1,2,3], [1,3,2], [2,1,3], [2,3,1], [3,1,2], [3,2,1]]
```

For empty input, this implementation uses the mathematical convention of one empty ordering: `[[]]`.

### P — Plan

1. Keep a path and a Boolean `used` entry for every input index.
2. If the path has n items, save its copy and return.
3. Otherwise, loop over every input index, skipping those already used.
4. Mark an index used, append its item, recurse, then restore both the path and the used flag.

**Trace:** With `[1,2]`, choose 1 (`used=[True,False]`), then 2 and save `[1,2]`. Undo both choices. Choose 2 (`used=[False,True]`), then index 0 is available, giving `[2,1]`. Each sibling starts with the state its parent had before the previous choice.

**Why it works:** At a path of length k, precisely its k items are marked used. Choosing any unused item extends the ordering legally; undoing restores that rule. Every complete ordering corresponds to one sequence of distinct index choices, and every such sequence is explored. Path length increases to n, which stops each branch.

**Try first:** Should input index 0 remain available after choosing index 1 first? Hint: position order differs from input order. Final hint: scan all indices but skip `used[index]`.

### I — Implement

<details>
<summary>Show solution</summary>

```python
def permute(nums):
    result = []
    path = []
    used = [False] * len(nums)

    def search():
        if len(path) == len(nums):
            result.append(path.copy())
            return
        for index in range(len(nums)):
            if not used[index]:
                used[index] = True
                path.append(nums[index])
                search()
                path.pop()
                used[index] = False

    search()
    return result
```

</details>

**Code connection / checks:** The helper needs no `start` parameter: the used list determines available choices. Both undo lines are needed. Checks cover the supplied six permutations, a singleton, and the empty ordering convention.

**Cost:** For n items, n! answers each have length n. This implementation takes O((n+1)n!) time, including scanning candidate indices and copying completed paths. Returned space is O((n+1)n!); auxiliary space is O(n+1) for flags, path, and calls.

**Common mistakes:** Using increasing indices → produces combinations rather than all orderings → allow every unused index. Forgetting to clear a used flag → later branches lose legal choices → restore the flag after recursion.

**Interview explanation:** I fill the ordering one position at a time, choosing among unused input items. A used flag prevents repeats within a path, and restoring it lets sibling branches reuse the item. Enumerating and copying n! results takes O(n·n!) time for n≥1 and O(n) auxiliary space.

**Check your understanding:** How many answers exist for four distinct items? How would the stopping condition change for orderings of exactly k distinct items from n?

<details>
<summary>Reasoning and answers</summary>

There are 4·3·2·1 = 24 full permutations. For length k with 0≤k≤n, save and stop when `len(path)==k`; the same used flags prevent repeats. There are n!/(n-k)! such orderings.

</details>

## Problem 3: Combination Sum

**Learning goal / clue:** Unlimited reuse requires revisiting the same candidate; combinations require preventing different selection orders from creating duplicate answers.

### U — Understand

`combination_sum(candidates, target)` returns unique combinations of distinct positive candidates that sum to target. A candidate may appear repeatedly. `[2,2,3]` and `[3,2,2]` represent the same combination.

```python
combination_sum([2, 3, 6, 7], 7)
# [[2, 2, 3], [7]]
```

The prompt does not specify a target range. For nonnegative targets, this implementation treats target 0 as one empty combination, `[[]]`; for a negative target it returns `[]` because positive candidates cannot sum to it. Empty candidates yield `[]` for a positive target. Candidate order is retained and the input is not sorted or changed.

### P — Plan

1. Track a path, first allowed candidate index, and remaining target.
2. When remaining is zero, save a copy and return.
3. Try each candidate at or after the allowed index, provided it does not exceed remaining.
4. Recurse with the **same** index to permit reuse, subtract its value from remaining, and undo the choice afterward.

**Trace:** With `[2,3]`, target 7: choose 2 → remaining 5; choose 2 → remaining 3. Another 2 leaves 1 and produces no answer. Undo it, choose 3 → remaining 0, and save `[2,2,3]`. The branch beginning with 3 cannot later choose index 0, so it never creates the duplicate `[3,2,2]`.

**Why it works:** Every combination has exactly one representation with nondecreasing candidate indices, even when candidate values are unsorted. The search explores every such representation that can reach the target. A positive candidate exceeding remaining cannot help, because later additions are also positive. Remaining strictly decreases with each choice, so every branch terminates.

**Try first:** How does reuse change `index+1` from Subsets? Hint: keep the current index available. Final hint: call `search(index, remaining-value)` while still excluding earlier indices.

### I — Implement

<details>
<summary>Show solution</summary>

```python
def combination_sum(candidates, target):
    result = []
    path = []

    def search(start, remaining):
        if remaining == 0:
            result.append(path.copy())
            return
        for index in range(start, len(candidates)):
            value = candidates[index]
            if value <= remaining:
                path.append(value)
                search(index, remaining - value)
                path.pop()

    search(0, target)
    return result
```

</details>

**Code connection / checks:** A too-large candidate is skipped, not used to `break` the loop, because later candidates may be smaller in an unsorted input. Checks cover the supplied output, no solution, target 0, empty candidates, and unsorted candidates `[3,2]` producing `[3,2,2]` for target 7.

**Cost:** Let m be the number of candidates, T≥0 the target, c the smallest candidate, D=⌊T/c⌋ the maximum path length, V the number of calls actually visited, and S the total size of returned lists including their list objects. For m≥1, time is O(mV+S), because each nonterminal call scans at most m candidates and answers are copied. A loose bound is V≤1+m+...+mᴰ; for m≥2 this gives O(mᴰ⁺¹+S) time. Auxiliary space is O(D+1); returned space is O(S). For no candidates, the call does constant work. These are upper bounds, not claims that every candidate sequence is visited.

**Common mistakes:** Passing `index+1` → prevents reuse → retain `index`. Allowing index 0 after every choice → duplicates different orders → retain a lower index bound. Allowing candidate 0 → remaining need not shrink → positivity is essential to termination.

**Interview explanation:** I keep candidate indices nondecreasing to give each combination a single representation. Reusing the current index permits repeated values, and subtracting a positive value guarantees progress. The search is exponential in the maximum combination length in a loose worst-case bound; its stack and path use O(T/min(candidates)+1) space.

**Check your understanding:** Why does candidate 2 fail to make target 3 by itself? What must change if each candidate can be used only once?

<details>
<summary>Reasoning and answers</summary>

Choosing 2 leaves 1, so no candidate is small enough to continue. If reuse is forbidden, recurse at `index+1`. If that new problem also permits repeated input values, further duplicate handling would be needed.

</details>

## Problem 4: Generate Parentheses

**Learning goal / clue:** Balanced parentheses require every prefix to have at least as many opening as closing parentheses. Enforce that rule while building the string.

### U — Understand

`generate_parentheses(n)` returns all balanced strings containing n pairs. Assume n is a nonnegative integer. For n=0, this implementation returns `[""]`: the empty string is the one balanced arrangement of zero pairs.

```python
generate_parentheses(3)
# ['((()))', '(()())', '(())()', '()(())', '()()()']
```

### P — Plan

1. Keep a path plus counts `opened` and `closed`.
2. Add `(` if fewer than n openings have been used.
3. Add `)` only if `closed < opened`, so it closes an existing unmatched opening.
4. When length reaches 2n, join the path into a string and save it. Undo each appended character after exploring its branch.

**Trace:** For n=2, the empty path can only choose `(`. From `(`, choosing another opening eventually gives `(())`. Undoing to `(` allows a closing next, giving `()`, then `()()`. The initial path never explores `)` because there is no opening to match it.

**Why it works:** Every generated prefix has `0≤closed≤opened≤n`. At length 2n those inequalities force both counts to equal n, producing a balanced string. Every balanced string obeys the same prefix rule, so its sequence of choices is explored. Each call adds one character, ensuring termination at depth 2n.

**Try first:** Is equal total count enough to make `)(` valid? Hint: examine the first prefix. Final hint: permit `)` only when `closed < opened`.

### I — Implement

<details>
<summary>Show solution</summary>

```python
def generate_parentheses(n):
    result = []
    path = []

    def search(opened, closed):
        if len(path) == 2 * n:
            result.append("".join(path))
            return
        if opened < n:
            path.append("(")
            search(opened + 1, closed)
            path.pop()
        if closed < opened:
            path.append(")")
            search(opened, closed + 1)
            path.pop()

    search(0, 0)
    return result
```

</details>

**Code connection / checks:** These are two independent `if` statements: both choices can be legal. Joining makes a complete string whose value is unaffected by later pops. Checks cover all five supplied strings, n=1, and n=0.

**Cost:** Let Cₙ=(1/(n+1))·binomial(2n,n), the number of balanced strings (the nth Catalan number). Time and returned space are O((n+1)Cₙ), including string construction; auxiliary space is O(n+1). A looser time bound is O((n+1)4ⁿ), since there are at most 2²ⁿ unrestricted strings of length 2n.

**Common mistakes:** Checking counts only at the end → admits invalid prefixes such as `)(` → enforce the prefix rule. Using `elif` → skips one legal branch when both choices work → use independent conditions.

**Interview explanation:** I generate only prefixes that could still become balanced. Openings are limited by n, and closings are limited by openings already placed. Each valid length-2n string is reached once, with O(n) auxiliary space and time proportional to the total output size.

**Check your understanding:** From path `()`, can the next character be `)`? How could you limit maximum nesting depth to d?

<details>
<summary>Reasoning and answers</summary>

No: opened and closed are equal, so another closing has no match. For a depth limit, also require `opened-closed < d` before adding an opening; that difference counts currently unmatched openings.

</details>

## Problem 5: Letter Combinations of a Phone Number

**Learning goal / clue:** Each output chooses one letter for each input digit. The next recursive level handles the next digit, rather than choosing any remaining digit.

### U — Understand

`letter_combinations(digits)` returns all letter strings for the digit sequence, preserving digit order. Digits are from 2–9: `2:abc`, `3:def`, `4:ghi`, `5:jkl`, `6:mno`, `7:pqrs`, `8:tuv`, `9:wxyz`. Return order is unrestricted.

```python
letter_combinations("23")
# ['ad', 'ae', 'af', 'bd', 'be', 'bf', 'cd', 'ce', 'cf']
```

The prompt does not specify empty-input behavior. This implementation returns `[]` for `""`, matching the convention that an absent phone number gives no letter suggestions. It assumes nonempty inputs contain only digits 2–9.

### P — Plan

1. Return `[]` immediately for empty digits. Otherwise prepare the digit-to-letter dictionary.
2. Let `search(index)` build the letter at input position `index`.
3. Try each letter for that digit, append it, recurse at `index+1`, then pop it.
4. Once index reaches the digit count, join the path and save it.

**Trace:** For `"23"`, choose `a` for digit 2, then try `d`, `e`, `f` for digit 3, saving `ad`, `ae`, `af`. Undo `a` and choose `b`, which generates `bd`, `be`, `bf`. Then `c` generates the final three strings.

**Why it works:** At call index i, the path contains exactly one valid letter for each of the first i digits. Trying every mapped letter extends that property. Every possible output corresponds to one such sequence of choices, and different choices give different strings. Index increases to the finite input length, where the complete string is saved.

**Try first:** Which digit does a path of length two need next? Hint: the path length and digit index advance together. Final hint: loop through `keypad[digits[index]]`, then recurse at `index+1`.

### I — Implement

<details>
<summary>Show solution</summary>

```python
def letter_combinations(digits):
    if not digits:
        return []
    keypad = {"2": "abc", "3": "def", "4": "ghi", "5": "jkl",
              "6": "mno", "7": "pqrs", "8": "tuv", "9": "wxyz"}
    result = []
    path = []

    def search(index):
        if index == len(digits):
            result.append("".join(path))
            return
        for letter in keypad[digits[index]]:
            path.append(letter)
            search(index + 1)
            path.pop()

    search(0)
    return result
```

</details>

**Code connection / checks:** `keypad[digits[index]]` looks up a string value in the dictionary; the loop then visits that string's letters. It does not loop through dictionary keys or values as a whole. Checks cover the supplied nine answers, empty digits, the four-letter digit 7, and sixteen combinations for `"79"`.

**Cost:** For d≥1 digits, let a count the digits with three letters and b count those with four; a+b=d. There are K=3ᵃ4ᵇ outputs. Time and returned space are O(dK), including joins; auxiliary space is O(d). The looser worst-case time bound is O(d4ᵈ). Empty input takes O(1) time and space.

**Common mistakes:** Treating all keys as three-letter groups → loses letters for 7 and 9 → use the full mapping. Recursing at the same index → never advances to the next digit → use `index+1`. Omitting the empty-input check → returns `[""]` under the helper's base case → apply the chosen empty-number convention explicitly.

**Interview explanation:** Each recursive level selects one mapped letter for the next digit. Trying every letter forms the Cartesian product of the digit groups. With K answers of length d, constructing them takes O(dK) time and O(d) auxiliary space.

**Check your understanding:** How many strings does `"27"` produce? How would the same approach generate outfits from separate shirt, trouser, and shoe lists?

<details>
<summary>Reasoning and answers</summary>

Digit 2 supplies three choices and digit 7 four, so 3·4=12 strings. For outfits, let each recursion level choose one item from its category list, advance to the next category, and save a copy when all categories have a choice. The structure is the same product of independent groups.

</details>
