# Week 2 — Session 2 — Problem Set Version 1

Work through **Understand → Plan → Implement**. Before opening the implementation, trace the plan yourself. The concept map shows what each exercise adds.

## Concept progression

| Problem | Main concept | Prerequisite | Explain after solving |
| --- | --- | --- | --- |
| 1. Balanced Art Collection | Combine frequencies of adjacent values | Frequency maps and subsequences | Maximum minus minimum must equal exactly 1; a valid choice contains x and x+1, both present. |
| 2. Verifying Authenticity | Compare exact contents after ignoring order | Sorting and multiplicity | A permutation may reorder values but must preserve every required occurrence. |
| 3. Gallery Wall | Prove a lower bound, then meet it | Frequency maps and independent lists | Each copy of the most frequent item needs a different row. |
| 4. Gallery Subdomain Traffic | Aggregate every domain suffix | String splitting and dictionaries | A visit counts toward the full domain and each parent after a dot. |
| 5. Beautiful Collection | Reuse counts while extending a substring | Nested loops and frequency maps | Every contiguous substring has a unique start/end pair. |

Build on the earlier exercises, but select an approach from the requirements rather than the story. A new collection or recursive call is useful only when its behavior serves those requirements.


## 1. Balanced Art Collection — `find_balanced_subsequence(art_pieces)`

**Learning goal:** Use this idea in a solution and explain why it works: **Combine frequencies of adjacent values**.

**Key concept and recognition clue:** Maximum minus minimum must equal exactly 1; a valid choice contains x and x+1, both present.

### U — Understand

Return the length of the longest subsequence whose maximum and minimum values differ by exactly 1.

```python
find_balanced_subsequence([1, 3, 2, 2, 5, 2, 3, 7])  # 5
find_balanced_subsequence([1, 2, 3, 4])               # 2
find_balanced_subsequence([1, 1, 1, 1])               # 0
```

**Before planning:** Identify the input, the exact return value or mutation, and the allowed operations from the statement above. Check whether order, object identity, or input mutation matters; do not substitute printing for returning.

### P — Plan

**Hints, in order:** First identify the rule that controls the next decision. Then decide what state must be remembered. Finally, try the concrete steps below on the trace before writing code.

Count values. For each x with x+1 present, add their counts and update the largest length.

**Trace:** [1,2,2,3]: pair 1/2 gives 3, pair 2/3 gives 3; all four values would have difference 2.

**Why this works and stops:** Every valid selection has only x and x+1; taking all their occurrences maximizes its length without changing their order.

### I — Implement

<details>
<summary>Open the implementation after trying the plan</summary>

```python
def find_balanced_subsequence(art_pieces):
    frequencies = {}
    for value in art_pieces:
        frequencies[value] = frequencies.get(value, 0) + 1

    best_length = 0
    for value in frequencies:
        if value + 1 in frequencies:
            best_length = max(best_length, frequencies[value] + frequencies[value + 1])
    return best_length
```

</details>

**Connect code to plan:** Count values. For each x with x+1 present, add their counts and update the largest length.

**Check the solution:** Walk through the supplied examples and compare the result with the required output. Then use this small case to verify the decisive step: [1,2,2,3]: pair 1/2 gives 3, pair 2/3 gives 3; all four values would have difference 2. Try the questions below before opening their answers.

**Cost:** O(n) expected time and O(k) auxiliary space for n entries and k distinct values.

### Common mistakes

Allowing a single repeated value uses difference 0. Subsequence does not mean contiguous substring.

### Interview explanation

“Maximum minus minimum must equal exactly 1; a valid choice contains x and x+1, both present. My plan is: Count values. For each x with x+1 present, add their counts and update the largest length. The reason it works is that every valid selection has only x and x+1; taking all their occurrences maximizes its length without changing their order. Its cost is O(n) expected time and O(k) auxiliary space for n entries and k distinct values.”

Use this as a model of reasoning, not a script. Say what each variable means and explain the decisive update before coding.

### Check your understanding

Why does [1,1,1] return 0? How can separated occurrences be kept?

<details>
<summary>Reasoning and answers</summary>

No adjacent distinct value is present. Select both values in their original order; gaps are allowed in a subsequence.

</details>

## 2. Verifying Authenticity — `is_authentic_collection(art_pieces)`

**Learning goal:** Use this idea in a solution and explain why it works: **Compare exact contents after ignoring order**.

**Key concept and recognition clue:** A permutation may reorder values but must preserve every required occurrence.

### U — Understand

An authentic collection is a permutation of `base[n] = [1, 2, ..., n, n]`: values 1 through `n - 1` once and `n` twice. Return whether the input is authentic.

```python
is_authentic_collection([2, 1, 3])     # False
is_authentic_collection([1, 3, 3, 2])  # True
is_authentic_collection([1, 1])        # True
```

**Before planning:** Identify the input, the exact return value or mutation, and the allowed operations from the statement above. Check whether order, object identity, or input mutation matters; do not substitute printing for returning.

### P — Plan

**Hints, in order:** First identify the rule that controls the next decision. Then decide what state must be remembered. Finally, try the concrete steps below on the trace before writing code.

For nonempty input let n be its maximum. Build 1..n plus another n. Compare with sorted input.

**Trace:** [1,3,3,2] sorts to [1,2,3,3], matching base[3]; [1,2,3] lacks the second 3.

**Why this works and stops:** Sorted equality checks multiplicity as well as membership; both finite lists represent the proposed contents.

### I — Implement

<details>
<summary>Open the implementation after trying the plan</summary>

```python
def is_authentic_collection(art_pieces):
    if not art_pieces:
        return False
    n = max(art_pieces)
    expected = list(range(1, n + 1)) + [n]
    return sorted(art_pieces) == expected
```

</details>

**Connect code to plan:** For nonempty input let n be its maximum. Build 1..n plus another n. Compare with sorted input.

**Check the solution:** Walk through the supplied examples and compare the result with the required output. Then use this small case to verify the decisive step: [1,3,3,2] sorts to [1,2,3,3], matching base[3]; [1,2,3] lacks the second 3. Try the questions below before opening their answers.

**Cost:** For m input entries and maximum v: O(m log m + v) time and O(m+v) space. On valid inputs v=m-1.

### Common mistakes

Using a set loses the repeated n. Confusing the maximum value with input length builds the wrong expected list.

### Interview explanation

“A permutation may reorder values but must preserve every required occurrence. My plan is: For nonempty input let n be its maximum. Build 1..n plus another n. Compare with sorted input. The reason it works is that sorted equality checks multiplicity as well as membership; both finite lists represent the proposed contents. Its cost is For m input entries and maximum v: O(m log m + v) time and O(m+v) space. On valid inputs v=m-1.”

Use this as a model of reasoning, not a script. Say what each variable means and explain the decisive update before coding.

### Check your understanding

Why is [1,1] valid? What if one huge maximum is supplied?

<details>
<summary>Reasoning and answers</summary>

It is base[1]. This implementation builds through that maximum, so time and memory must include its magnitude; validate size first for a more robust alternative.

</details>

## 3. Gallery Wall — `organize_exhibition(collection)`

**Learning goal:** Use this idea in a solution and explain why it works: **Prove a lower bound, then meet it**.

**Key concept and recognition clue:** Each copy of the most frequent item needs a different row.

### U — Understand

Return a 2D array that uses every string, has no duplicate string within any row, and has the minimum possible number of rows.

```python
organize_exhibition(["O'Keefe", "Kahlo", "Picasso", "O'Keefe", "Warhol", "Kahlo", "O'Keefe"])
# [["O'Keefe", "Kahlo", "Picasso", "Warhol"], ["O'Keefe", "Kahlo"], ["O'Keefe"]]
```

**Before planning:** Identify the input, the exact return value or mutation, and the allowed operations from the statement above. Check whether order, object identity, or input mutation matters; do not substitute printing for returning.

### P — Plan

**Hints, in order:** First identify the rule that controls the next decision. Then decide what state must be remembered. Finally, try the concrete steps below on the trace before writing code.

Count item frequencies; create as many rows as the largest count. Track occurrences used per item and place its next copy in the next row.

**Trace:** [A,B,A,A]: create 3 rows; A goes in rows 0,1,2 and B in row 0 -> [[A,B],[A],[A]].

**Why this works and stops:** The largest frequency is a lower bound on row count; assigning each copy a separate row achieves that bound.

### I — Implement

<details>
<summary>Open the implementation after trying the plan</summary>

```python
def organize_exhibition(collection):
    frequencies = {}
    for item in collection:
        frequencies[item] = frequencies.get(item, 0) + 1
    row_count = max(frequencies.values(), default=0)
    rows = [[] for _ in range(row_count)]
    used = {}
    for item in collection:
        row = used.get(item, 0)
        rows[row].append(item)
        used[item] = row + 1
    return rows
```

</details>

**Connect code to plan:** Count item frequencies; create as many rows as the largest count. Track occurrences used per item and place its next copy in the next row.

**Check the solution:** Walk through the supplied examples and compare the result with the required output. Then use this small case to verify the decisive step: [A,B,A,A]: create 3 rows; A goes in rows 0,1,2 and B in row 0 -> [[A,B],[A],[A]]. Try the questions below before opening their answers.

**Cost:** O(n) expected time, O(k) counting/placement state, and O(n) output for n entries and k distinct items.

### Common mistakes

Creating shared rows with [[]]*k makes one list appear in every row. Using a set discards copies that must be retained.

### Interview explanation

“Each copy of the most frequent item needs a different row. My plan is: Count item frequencies; create as many rows as the largest count. Track occurrences used per item and place its next copy in the next row. The reason it works is that the largest frequency is a lower bound on row count; assigning each copy a separate row achieves that bound. Its cost is O(n) expected time, O(k) counting/placement state, and O(n) output for n entries and k distinct items.”

Use this as a model of reasoning, not a script. Say what each variable means and explain the decisive update before coding.

### Check your understanding

Why are two rows insufficient for [A,A,A]? What if all items are unique?

<details>
<summary>Reasoning and answers</summary>

Each row can hold A only once, requiring three rows. All unique items fit in one row.

</details>

## 4. Gallery Subdomain Traffic — `subdomain_visits(cpdomains)`

**Learning goal:** Use this idea in a solution and explain why it works: **Aggregate every domain suffix**.

**Key concept and recognition clue:** A visit counts toward the full domain and each parent after a dot.

### U — Understand

Each entry is formatted as `"count domain"`. A visit to `modern.artmuseum.com` also visits `artmuseum.com` and `com`. Return count-paired strings for every subdomain in any order.

```python
subdomain_visits(["9001 modern.artmuseum.com"])
# ["9001 modern.artmuseum.com", "9001 artmuseum.com", "9001 com"]  # any order
```

**Before planning:** Identify the input, the exact return value or mutation, and the allowed operations from the statement above. Check whether order, object identity, or input mutation matters; do not substitute printing for returning.

### P — Plan

**Hints, in order:** First identify the rule that controls the next decision. Then decide what state must be remembered. Finally, try the concrete steps below on the trace before writing code.

Parse the count as an integer. Split the domain, build each suffix, add its count, and format count/domain strings.

**Trace:** 2 a.b.com contributes 2 to a.b.com, b.com, com; 3 b.com raises the last two totals to 5.

**Why this works and stops:** Every full domain and parent suffix receives exactly this entry’s contribution once; aggregation includes all entries.

### I — Implement

<details>
<summary>Open the implementation after trying the plan</summary>

```python
def subdomain_visits(cpdomains):
    visits = {}
    for entry in cpdomains:
        count_text, domain = entry.split(" ", 1)
        count = int(count_text)
        pieces = domain.split(".")
        for start in range(len(pieces)):
            subdomain = ".".join(pieces[start:])
            visits[subdomain] = visits.get(subdomain, 0) + count
    return [f"{count} {domain}" for domain, count in visits.items()]
```

</details>

**Connect code to plan:** Parse the count as an integer. Split the domain, build each suffix, add its count, and format count/domain strings.

**Check the solution:** Walk through the supplied examples and compare the result with the required output. Then use this small case to verify the decisive step: 2 a.b.com contributes 2 to a.b.com, b.com, com; 3 b.com raises the last two totals to 5. Try the questions below before opening their answers.

**Cost:** String construction matters: O(T + Σ dL) time upper bound, where T is input characters and each domain has d labels and L characters. Memory includes distinct suffix strings and formatted output, not just the number of keys.

### Common mistakes

Overwriting counts loses earlier contributions. Prefixes such as a.b are not parent domains.

### Interview explanation

“A visit counts toward the full domain and each parent after a dot. My plan is: Parse the count as an integer. Split the domain, build each suffix, add its count, and format count/domain strings. The reason it works is that every full domain and parent suffix receives exactly this entry’s contribution once; aggregation includes all entries. Its cost is String construction matters: O(T + Σ dL) time upper bound, where T is input characters and each domain has d labels and L characters. Memory includes distinct suffix strings and formatted output, not just the number of keys.”

Use this as a model of reasoning, not a script. Say what each variable means and explain the decisive update before coding.

### Check your understanding

How many suffixes does a.b.com produce? What if two entries share com?

<details>
<summary>Reasoning and answers</summary>

Three. Add both visit counts to com in the same dictionary entry.

</details>

## 5. Beautiful Collection — `beauty_sum(collection)`

**Learning goal:** Use this idea in a solution and explain why it works: **Reuse counts while extending a substring**.

**Key concept and recognition clue:** Every contiguous substring has a unique start/end pair.

### U — Understand

The beauty of a string is its highest character frequency minus its lowest positive character frequency. Return the sum of the beauty of every substring.

```python
beauty_sum("aabcb")    # 5
beauty_sum("aabcbaa")  # 17
```

**Before planning:** Identify the input, the exact return value or mutation, and the allowed operations from the statement above. Check whether order, object identity, or input mutation matters; do not substitute printing for returning.

### P — Plan

**Hints, in order:** First identify the rule that controls the next decision. Then decide what state must be remembered. Finally, try the concrete steps below on the trace before writing code.

For each start reset counts. Extend end one character at a time, update its frequency, and add max minus minimum positive frequency.

**Trace:** For start 0 of aab: a has beauty 0; aa has 0; aab has counts 2,1 and beauty 1.

**Why this works and stops:** At each extension the map describes exactly start..end; every substring has one unique pair of indexes.

### I — Implement

<details>
<summary>Open the implementation after trying the plan</summary>

```python
def beauty_sum(collection):
    total_beauty = 0
    for start in range(len(collection)):
        frequencies = {}
        for end in range(start, len(collection)):
            letter = collection[end]
            frequencies[letter] = frequencies.get(letter, 0) + 1
            counts = frequencies.values()
            total_beauty += max(counts) - min(counts)
    return total_beauty
```

</details>

**Connect code to plan:** For each start reset counts. Extend end one character at a time, update its frequency, and add max minus minimum positive frequency.

**Check the solution:** Walk through the supplied examples and compare the result with the required output. Then use this small case to verify the decisive step: For start 0 of aab: a has beauty 0; aa has 0; aab has counts 2,1 and beauty 1. Try the questions below before opening their answers.

**Cost:** O(n²k) time for n characters and at most k distinct letters per substring; O(k) auxiliary space. Fixed lowercase alphabet gives O(n²).

### Common mistakes

Including zero-frequency letters makes the minimum incorrect. Failing to reset for a new start counts letters outside the substring.

### Interview explanation

“Every contiguous substring has a unique start/end pair. My plan is: For each start reset counts. Extend end one character at a time, update its frequency, and add max minus minimum positive frequency. The reason it works is that at each extension the map describes exactly start..end; every substring has one unique pair of indexes. Its cost is O(n²k) time for n characters and at most k distinct letters per substring; O(k) auxiliary space. Fixed lowercase alphabet gives O(n²).”

Use this as a model of reasoning, not a script. Say what each variable means and explain the decisive update before coding.

### Check your understanding

What is beauty of aaa? Could you use this directly for noncontiguous subsequences?

<details>
<summary>Reasoning and answers</summary>

0: only one positive frequency exists. No: start/end pairs enumerate contiguous substrings, not arbitrary subsequences.

</details>
