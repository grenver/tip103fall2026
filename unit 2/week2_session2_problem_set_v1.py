"""UPI solutions for Week 2, Session 2, Problem Set Version 1."""


# 1. Balanced Art Collection
# U: A balanced subsequence has max - min exactly 1. Order is preserved, but
# choosing all occurrences of two adjacent values preserves it automatically.
# P: Count values, then find the largest total for value and value + 1.
# Pseudocode: count values; FOR each value: update best with count[value] +
# count[value + 1]; RETURN best.
def find_balanced_subsequence(art_pieces):
    frequencies = {}
    for value in art_pieces:
        frequencies[value] = frequencies.get(value, 0) + 1

    best_length = 0
    for value in frequencies:
        if value + 1 in frequencies:
            best_length = max(best_length, frequencies[value] + frequencies[value + 1])
    return best_length


# 2. Verifying Authenticity
# U: base[n] contains 1 through n once, with n twice. Order does not matter.
# P: Sort the collection and compare it with its expected base array.
# Pseudocode: n = max(values); expected = [1..n] plus n; RETURN sorted == expected.
def is_authentic_collection(art_pieces):
    if not art_pieces:
        return False
    n = max(art_pieces)
    expected = list(range(1, n + 1)) + [n]
    return sorted(art_pieces) == expected


# 3. Gallery Wall
# U: Rows cannot repeat a string, and their count must be minimal.
# P: The maximum occurrence count determines the number of rows. Place each
# occurrence of an item in its next unused row.
# Pseudocode: count max frequency; create that many rows; FOR each item: append
# it to row number of previous occurrences; RETURN rows.
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


# 4. Gallery Subdomain Traffic
# U: A visit counts for the full domain and every suffix after a dot.
# P: Split each entry into visits and domain; add visits to every suffix.
# Pseudocode: FOR entry: parse count/domain; FOR each suffix: add count; format results.
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


# 5. Beautiful Collection
# U: Beauty is max frequency minus min positive frequency for every substring.
# P: Start each substring position, extend its end one character at a time, and
# maintain its frequency map to add its beauty.
# Pseudocode: FOR start: frequencies = {}; FOR end: count character; add
# max(counts) - min(counts); RETURN total.
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


if __name__ == "__main__":
    assert find_balanced_subsequence([1, 3, 2, 2, 5, 2, 3, 7]) == 5
    assert find_balanced_subsequence([1, 2, 3, 4]) == 2
    assert find_balanced_subsequence([1, 1, 1, 1]) == 0
    assert is_authentic_collection([2, 1, 3]) is False
    assert is_authentic_collection([1, 3, 3, 2]) is True
    assert is_authentic_collection([1, 1]) is True
    assert organize_exhibition(["O'Keefe", "Kahlo", "Picasso", "O'Keefe", "Warhol", "Kahlo", "O'Keefe"]) == [["O'Keefe", "Kahlo", "Picasso", "Warhol"], ["O'Keefe", "Kahlo"], ["O'Keefe"]]
    assert organize_exhibition(["Kusama", "Monet", "Ofili", "Banksy"]) == [["Kusama", "Monet", "Ofili", "Banksy"]]
    assert set(subdomain_visits(["9001 modern.artmuseum.com"])) == {"9001 modern.artmuseum.com", "9001 artmuseum.com", "9001 com"}
    assert beauty_sum("aabcb") == 5
    assert beauty_sum("aabcbaa") == 17
