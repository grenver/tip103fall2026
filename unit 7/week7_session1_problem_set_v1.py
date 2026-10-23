"""Unit 7, Session 1, Version 1: connected components and Union Find.

The shared helper is required when copying a solution for submission.
Inputs follow the problem contracts; functions do not change the inputs.
"""


# Shared helper -- Union Find (also called disjoint sets).
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n
        self.components = n

    def find(self, node):
        while node != self.parent[node]:
            # Point toward the grandparent to shorten future searches.
            self.parent[node] = self.parent[self.parent[node]]
            node = self.parent[node]
        return node

    def union(self, a, b):
        root_a, root_b = self.find(a), self.find(b)
        if root_a == root_b:
            return False  # Already in the same component.
        if self.size[root_a] < self.size[root_b]:
            root_a, root_b = root_b, root_a
        self.parent[root_b] = root_a
        self.size[root_a] += self.size[root_b]
        self.components -= 1
        return True


# ======================================================================
# Problem 1: Number of Provinces -- find_circle_num
# U -- Understand: A symmetric matrix represents undirected city connections.
# P -- Plan: Begin with n groups; merge cities connected above the diagonal.
# I -- Implement
def find_circle_num(is_connected):
    n = len(is_connected)
    groups = UnionFind(n)
    for city in range(n):
        for neighbor in range(city + 1, n):
            if is_connected[city][neighbor] == 1:
                groups.union(city, neighbor)
    return groups.components


# ======================================================================
# Problem 2: Redundant Connection -- find_redundant_connection
# U -- Understand: A tree on labels 1..n has exactly one extra edge.
# P -- Plan: Process input order; the first failed union closes the cycle.
# I -- Implement
def find_redundant_connection(edges):
    groups = UnionFind(len(edges) + 1)  # Index 0 is unused.
    for a, b in edges:
        if not groups.union(a, b):
            return [a, b]
    return []  # Unused for the guaranteed tree-plus-one-edge input.


# ======================================================================
# Problem 3: Graph Valid Tree -- valid_tree
# U -- Understand: A tree must be connected and acyclic; assume n >= 1.
# P -- Plan: Require n-1 edges, then reject any union within one component.
# I -- Implement
def valid_tree(n, edges):
    if len(edges) != n - 1:
        return False
    groups = UnionFind(n)
    for a, b in edges:
        if not groups.union(a, b):
            return False
    return groups.components == 1


# ======================================================================
# Problem 4: Number of Connected Components -- count_components
# U -- Understand: All n nodes count, including isolated nodes.
# P -- Plan: Each successful union reduces the component count by one.
# I -- Implement
def count_components(n, edges):
    groups = UnionFind(n)
    for a, b in edges:
        groups.union(a, b)
    return groups.components


# ======================================================================
# Problem 5: Accounts Merge -- accounts_merge
# U -- Understand: Shared emails merge accounts transitively; names do not.
# P -- Plan: Map each email to an account index, union matches, group emails.
# I -- Implement
def accounts_merge(accounts):
    groups = UnionFind(len(accounts))
    email_owner = {}
    for index, account in enumerate(accounts):
        for email_index in range(1, len(account)):
            email = account[email_index]
            if email in email_owner:
                groups.union(index, email_owner[email])
            else:
                email_owner[email] = index

    emails_by_root = {}
    for email, owner in email_owner.items():
        root = groups.find(owner)
        if root not in emails_by_root:
            emails_by_root[root] = []
        emails_by_root[root].append(email)

    merged = []
    for root, emails in emails_by_root.items():
        merged.append([accounts[root][0]] + sorted(emails))
    # Outer order is unspecified; sort for a reproducible displayed result.
    return sorted(merged)


# Example and boundary checks -- one labeled block per problem.
if __name__ == '__main__':
    # Problem 1: Number of Provinces
    assert find_circle_num([[1, 1, 0], [1, 1, 0], [0, 0, 1]]) == 2
    assert find_circle_num([[1, 0, 0], [0, 1, 0], [0, 0, 1]]) == 3
    assert find_circle_num([[1]]) == 1
    assert find_circle_num([[1, 1, 0], [1, 1, 1], [0, 1, 1]]) == 1
    print('Problem 1: Number of Provinces - passed')

    # Problem 2: Redundant Connection
    assert find_redundant_connection([[1, 2], [1, 3], [2, 3]]) == [2, 3]
    assert find_redundant_connection([[1, 2], [2, 3], [3, 4], [1, 4], [1, 5]]) == [1, 4]
    assert find_redundant_connection([[3, 1], [1, 2], [2, 3]]) == [2, 3]
    print('Problem 2: Redundant Connection - passed')

    # Problem 3: Graph Valid Tree
    assert valid_tree(5, [[0, 1], [0, 2], [0, 3], [1, 4]]) is True
    assert valid_tree(5, [[0, 1], [1, 2], [2, 3], [1, 3], [1, 4]]) is False
    assert valid_tree(1, []) is True
    assert valid_tree(4, [[0, 1], [1, 2], [2, 0]]) is False
    assert valid_tree(2, []) is False
    print('Problem 3: Graph Valid Tree - passed')

    # Problem 4: Number of Connected Components
    assert count_components(5, [[0, 1], [1, 2], [3, 4]]) == 2
    assert count_components(5, [[0, 1], [1, 2], [2, 3], [3, 4]]) == 1
    assert count_components(3, []) == 3
    assert count_components(4, [[0, 1], [1, 2], [2, 0]]) == 2
    print('Problem 4: Number of Connected Components - passed')

    # Problem 5: Accounts Merge
    accounts = [
        ['John', 'johnsmith@mail.com', 'john_newyork@mail.com'],
        ['John', 'johnsmith@mail.com', 'john00@mail.com'],
        ['Mary', 'mary@mail.com'],
        ['John', 'johnnybravo@mail.com'],
    ]
    assert accounts_merge(accounts) == [
        ['John', 'john00@mail.com', 'john_newyork@mail.com', 'johnsmith@mail.com'],
        ['John', 'johnnybravo@mail.com'],
        ['Mary', 'mary@mail.com'],
    ]
    assert accounts_merge([['A', 'x', 'y'], ['A', 'z'], ['A', 'y', 'z']]) == [['A', 'x', 'y', 'z']]
    assert accounts_merge([['A', 'x'], ['A', 'y']]) == [['A', 'x'], ['A', 'y']]
    assert accounts_merge([['A', 'x', 'x']]) == [['A', 'x']]
    print('Problem 5: Accounts Merge - passed')
