"""UPI solutions for Week 2, Session 1, Problem Set Version 1."""


# 1. Counting Treasure
# U: Do values represent treasure counts? Yes. What is returned for {}? 0.
# P: Add every value in the dictionary.
# Pseudocode: total = 0; FOR each value: total += value; RETURN total.
def total_treasures(treasure_map):
    total = 0
    for amount in treasure_map.values():
        total += amount
    return total


# 2. Pirate Message Check
# U: Are spaces letters? No. Must every alphabet letter occur? Yes.
# P: Put message characters in a set, then check whether every alphabet letter
# is present.
# Pseudocode: letters = set(message); RETURN alphabet is a subset of letters.
def can_trust_message(message):
    alphabet = set("abcdefghijklmnopqrstuvwxyz")
    return alphabet.issubset(set(message))


# 3. Find All Duplicate Treasure Chests
# U: Which numbers are reported? Exactly those occurring twice.
# P: Count occurrences with a frequency map and return values whose count is 2.
# Pseudocode: count each chest; RETURN values with count == 2.
def find_duplicate_chests(chests):
    frequencies = {}
    for chest in chests:
        frequencies[chest] = frequencies.get(chest, 0) + 1
    return sorted(chest for chest in frequencies if frequencies[chest] == 2)


# 4. Booby Trap
# U: Must exactly one character be removed? Yes. Do zero counts matter? No.
# P: Try removing one occurrence of each distinct character and check whether
# every remaining positive frequency is identical.
# Pseudocode: count letters; FOR each letter: decrement it; IF remaining counts
# are equal: RETURN True; restore it; RETURN False.
def can_make_balanced(code):
    frequencies = {}
    for letter in code:
        frequencies[letter] = frequencies.get(letter, 0) + 1

    for letter in frequencies:
        frequencies[letter] -= 1
        remaining_counts = [count for count in frequencies.values() if count > 0]
        if len(set(remaining_counts)) <= 1:
            return True
        frequencies[letter] += 1
    return False


# 5. Overflowing With Gold
# U: Can one location be reused? No. Is exactly one pair guaranteed? Yes.
# P: Save previously seen values and their indices. For each amount, look for
# its complement (target - amount).
# Pseudocode: FOR each index and amount: IF complement was seen, RETURN both
# indices; otherwise save amount and index.
def find_treasure_indices(gold_amounts, target):
    seen = {}
    for index, amount in enumerate(gold_amounts):
        complement = target - amount
        if complement in seen:
            return [seen[complement], index]
        seen[amount] = index
    return []


if __name__ == "__main__":
    assert total_treasures({"Cove": 3, "Beach": 7, "Forest": 5}) == 15
    assert total_treasures({"Shipwreck": 10, "Cave": 20, "Lagoon": 15, "Island Peak": 5}) == 50
    assert can_trust_message("sphinx of black quartz judge my vow") is True
    assert can_trust_message("trust me") is False
    assert find_duplicate_chests([4, 3, 2, 7, 8, 2, 3, 1]) == [2, 3]
    assert find_duplicate_chests([1, 1, 2]) == [1]
    assert find_duplicate_chests([1]) == []
    assert can_make_balanced("arghh") is True
    assert can_make_balanced("haha") is False
    assert find_treasure_indices([2, 7, 11, 15], 9) == [0, 1]
    assert find_treasure_indices([3, 2, 4], 6) == [1, 2]
    assert find_treasure_indices([3, 3], 6) == [0, 1]
