"""UPI solutions for Week 3, Session 1, Problem Set Version 1."""


# 1. U: Each nested list is one layer. P: Recursively find the deepest nested
# list. Pseudocode: RETURN 1 + the greatest depth among nested child lists.
def count_layers(sandwich):
    deepest_child = 0
    for item in sandwich:
        if isinstance(item, list):
            deepest_child = max(deepest_child, count_layers(item))
    return 1 + deepest_child


# 2. U: Orders are separated by spaces. P: Use a recursive helper that appends
# words from last to first. Pseudocode: visit index; append word; visit index - 1.
def reverse_orders(orders):
    words = orders.split()
    reversed_words = []

    def add_in_reverse(index):
        if index < 0:
            return
        reversed_words.append(words[index])
        add_in_reverse(index - 1)

    add_in_reverse(len(words) - 1)
    return " ".join(reversed_words)


# 3. U: Each batch stays whole and n staff must get equal volume. P: Recursively
# try adding each batch to every staff member's bucket.
def can_split_coffee(coffee, n):
    total = sum(coffee)
    if total % n != 0:
        return False
    target = total // n
    buckets = [0] * n
    coffee = sorted(coffee, reverse=True)

    def assign_batch(index):
        if index == len(coffee):
            return all(amount == target for amount in buckets)
        for person in range(n):
            if buckets[person] + coffee[index] <= target:
                buckets[person] += coffee[index]
                if assign_batch(index + 1):
                    return True
                buckets[person] -= coffee[index]
            if buckets[person] == 0:
                break
        return False

    return assign_batch(0)


class Node:
    def __init__(self, value, next=None):
        self.value = value
        self.next = next


# 4. U: Nodes must alternate A then B; remaining nodes are kept. P: Link A to
# a recursive merge beginning with B. Pseudocode: A.next = merge(B, A.next).
def merge_orders(sandwich_a, sandwich_b):
    if not sandwich_a:
        return sandwich_b
    if not sandwich_b:
        return sandwich_a
    next_a = sandwich_a.next
    sandwich_a.next = merge_orders(sandwich_b, next_a)
    return sandwich_a


def linked_values(head):
    values = []
    while head:
        values.append(head.value)
        head = head.next
    return values


if __name__ == "__main__":
    assert count_layers(["bread", ["lettuce", ["tomato", ["bread"]]]]) == 4
    assert count_layers(["bread", ["cheese", ["ham", ["mustard", ["bread"]]]]]) == 5
    assert reverse_orders("Bagel Sandwich Coffee") == "Coffee Sandwich Bagel"
    assert can_split_coffee([4, 4, 8], 2) is True
    assert can_split_coffee([5, 10, 15], 4) is False
    a = Node("Bacon", Node("Lettuce", Node("Tomato")))
    b = Node("Turkey", Node("Cheese", Node("Mayo")))
    assert linked_values(merge_orders(a, b)) == ["Bacon", "Turkey", "Lettuce", "Cheese", "Tomato", "Mayo"]
