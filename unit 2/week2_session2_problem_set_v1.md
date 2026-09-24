# Week 2 — Session 2 — Problem Set Version 1

## 1. Balanced Art Collection — `find_balanced_subsequence(art_pieces)`

Return the length of the longest subsequence whose maximum and minimum values differ by exactly 1.

```python
find_balanced_subsequence([1, 3, 2, 2, 5, 2, 3, 7])  # 5
find_balanced_subsequence([1, 2, 3, 4])               # 2
find_balanced_subsequence([1, 1, 1, 1])               # 0
```

**Approach:** Count each value. For every value `x`, combine the frequency of `x` with `x + 1`, keeping the largest total.

**Why it works:** A balanced result can contain only two adjacent values. All occurrences of those two values can be kept without changing their order, yielding the longest such subsequence. Time: O(n); extra space: O(n).

## 2. Verifying Authenticity — `is_authentic_collection(art_pieces)`

An authentic collection is a permutation of `base[n] = [1, 2, ..., n, n]`: values 1 through `n - 1` once and `n` twice. Return whether the input is authentic.

```python
is_authentic_collection([2, 1, 3])     # False
is_authentic_collection([1, 3, 3, 2])  # True
is_authentic_collection([1, 1])        # True
```

**Approach:** Let `n` be the maximum value. Create the expected sorted list `[1, ..., n, n]` and compare it with the sorted input.

**Why it works:** The maximum must be `n`; sorting ignores permutation order and makes an exact content comparison possible. Time: O(n log n); extra space: O(n).

## 3. Gallery Wall — `organize_exhibition(collection)`

Return a 2D array that uses every string, has no duplicate string within any row, and has the minimum possible number of rows.

```python
organize_exhibition(["O'Keefe", "Kahlo", "Picasso", "O'Keefe", "Warhol", "Kahlo", "O'Keefe"])
# [["O'Keefe", "Kahlo", "Picasso", "Warhol"], ["O'Keefe", "Kahlo"], ["O'Keefe"]]
```

**Approach:** Find the largest frequency, create that many rows, then place each occurrence of an item in the next row assigned to that item.

**Why it works:** If an item occurs `k` times, it requires at least `k` rows. Using exactly that many rows and placing each copy in a different row meets the constraint with the minimum count. Time: O(n); extra space: O(n).

## 4. Gallery Subdomain Traffic — `subdomain_visits(cpdomains)`

Each entry is formatted as `"count domain"`. A visit to `modern.artmuseum.com` also visits `artmuseum.com` and `com`. Return count-paired strings for every subdomain in any order.

```python
subdomain_visits(["9001 modern.artmuseum.com"])
# ["9001 modern.artmuseum.com", "9001 artmuseum.com", "9001 com"]  # any order
```

**Approach:** Split each entry into a count and domain. Split the domain at dots, build every suffix, and add the count in a dictionary.

**Why it works:** The suffixes of a domain are exactly its parent subdomains. Aggregating each suffix across all entries produces its total visits. Time: O(total domain pieces); extra space: O(number of unique subdomains).

## 5. Beautiful Collection — `beauty_sum(collection)`

The beauty of a string is its highest character frequency minus its lowest positive character frequency. Return the sum of the beauty of every substring.

```python
beauty_sum("aabcb")    # 5
beauty_sum("aabcbaa")  # 17
```

**Approach:** For each start position, extend the substring one character at a time while maintaining a frequency map. Add the current maximum frequency minus minimum frequency after every extension.

**Why it works:** Every substring has one unique start/end pair, so this nested-loop process visits every substring once. The frequency map always describes the current substring, making its beauty available immediately. Time: O(n² × k), where `k` is the number of distinct letters (at most 26); extra space: O(k).
