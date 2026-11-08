"""Unit 9, Session 2, Version 1: Peer mock interviews, binary trees.

Includes local level-order helpers because their source was not pasted.
flatten_orders rewires the original nodes and returns the original root.
All other problem functions leave their inputs unchanged.
"""

from collections import Counter, deque


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def build_tree(values):
    """Build from level order: each real parent's next two entries are children."""
    if not values or values[0] is None:
        return None
    root = TreeNode(values[0])
    queue = deque([root])
    index = 1
    while queue and index < len(values):
        parent = queue.popleft()
        for side in ("left", "right"):
            if index == len(values):
                break
            value = values[index]
            index += 1
            if value is not None:
                child = TreeNode(value)
                setattr(parent, side, child)
                queue.append(child)
    return root


def tree_to_list(root):
    """Serialize level order, retaining internal None gaps, trimming trailing gaps."""
    values = []
    queue = deque([root])
    while queue:
        node = queue.popleft()
        if node is None:
            values.append(None)
        else:
            values.append(node.val)
            queue.extend((node.left, node.right))
    while values and values[-1] is None:
        values.pop()
    return values


def print_tree(root):
    print(tree_to_list(root))


# Problem 1: Creating Cookie Orders from Descriptions
# U: Construct one valid tree of unique flavors; descriptions may be unordered.
# P / Pseudocode: Reuse nodes by value, attach children, find the non-child root.
def build_cookie_tree(descriptions):
    nodes = {}
    children = set()
    for parent, child, is_left in descriptions:
        if parent not in nodes:
            nodes[parent] = TreeNode(parent)
        if child not in nodes:
            nodes[child] = TreeNode(child)
        if is_left:
            nodes[parent].left = nodes[child]
        else:
            nodes[parent].right = nodes[child]
        children.add(child)
    for value, node in nodes.items():
        if value not in children:
            return node
    return None


# Problem 2: Cookie Sum
# U: Count root-to-leaf paths with the target sum, not arbitrary subpaths.
# P / Pseudocode: Subtract this node; at a leaf test the remaining target.
def count_cookie_paths(root, target_sum):
    if root is None:
        return 0
    remaining = target_sum - root.val
    if root.left is None and root.right is None:
        return int(remaining == 0)
    return (count_cookie_paths(root.left, remaining)
            + count_cookie_paths(root.right, remaining))


# Problem 3: Most Popular Cookie Combo
# U: Return every subtree sum with maximum frequency, in any order.
# P / Pseudocode: Postorder computes each sum once; count sums, collect modes.
def most_popular_cookie_combo(root):
    if root is None:
        return []
    frequencies = Counter()

    def subtree_sum(node):
        if node is None:
            return 0
        total = node.val + subtree_sum(node.left) + subtree_sum(node.right)
        frequencies[total] += 1
        return total

    subtree_sum(root)
    highest = max(frequencies.values())
    return [total for total, count in frequencies.items() if count == highest]


# Problem 4: Convert Binary Tree of Bakery Orders to Linked List
# U: Reuse the same nodes in preorder; every left pointer becomes None.
# P / Pseudocode: Reverse preorder (right, left, node); link each node to previous.
def flatten_orders(orders):
    previous = None

    def flatten(node):
        nonlocal previous
        if node is None:
            return
        flatten(node.right)
        flatten(node.left)
        node.right = previous
        node.left = None
        previous = node

    flatten(orders)
    return orders


# Problem 5: Check Bakery Order Completeness
# U: Level order must never contain a real node after an empty child position.
# P / Pseudocode: BFS including missing children; reject a node after a gap.
def is_complete(root):
    queue = deque([root])
    seen_gap = False
    while queue:
        node = queue.popleft()
        if node is None:
            seen_gap = True
        else:
            if seen_gap:
                return False
            queue.extend((node.left, node.right))
    return True


if __name__ == "__main__":
    descriptions1 = [
        ["Chocolate Chip", "Peanut Butter", 1],
        ["Chocolate Chip", "Oatmeal Raisin", 0],
        ["Peanut Butter", "Sugar", 1],
    ]
    descriptions2 = [
        ["Ginger Snap", "Snickerdoodle", 0],
        ["Ginger Snap", "Shortbread", 1],
    ]
    assert tree_to_list(build_cookie_tree(descriptions1)) == [
        "Chocolate Chip", "Peanut Butter", "Oatmeal Raisin", "Sugar"]
    assert tree_to_list(build_cookie_tree(descriptions2)) == [
        "Ginger Snap", "Shortbread", "Snickerdoodle"]
    assert tree_to_list(build_cookie_tree(list(reversed(descriptions1)))) == [
        "Chocolate Chip", "Peanut Butter", "Oatmeal Raisin", "Sugar"]
    assert build_cookie_tree([]) is None
    print("Problem 1: Creating Cookie Orders from Descriptions -- checks passed")

    assert count_cookie_paths(build_tree([10, 5, 8, 3, 7, 12, 4]), 22) == 2
    assert count_cookie_paths(build_tree([8, 4, 12, 2, 6, None, 10]), 14) == 1
    assert count_cookie_paths(None, 0) == 0
    assert count_cookie_paths(build_tree([1, 0, 0]), 1) == 2
    assert count_cookie_paths(build_tree([1, 2]), 1) == 0
    assert count_cookie_paths(build_tree([2, -1]), 1) == 1
    print("Problem 2: Cookie Sum -- checks passed")

    assert sorted(most_popular_cookie_combo(build_tree([5, 2, -3]))) == [-3, 2, 4]
    assert most_popular_cookie_combo(build_tree([5, 2, -5])) == [2]
    assert most_popular_cookie_combo(None) == []
    assert most_popular_cookie_combo(build_tree([0, 0, 0])) == [0]
    print("Problem 3: Most Popular Cookie Combo -- checks passed")

    items = ["Croissant", "Cupcake", "Bagel", "Cake", "Pie", None, "Blondies"]
    orders = build_tree(items)
    original_preorder = [orders, orders.left, orders.left.left,
                         orders.left.right, orders.right, orders.right.right]
    assert flatten_orders(orders) is orders
    node = orders
    for original in original_preorder:
        assert node is original and node.left is None
        node = node.right
    assert node is None
    assert tree_to_list(orders) == [
        "Croissant", None, "Cupcake", None, "Cake", None,
        "Pie", None, "Bagel", None, "Blondies"]
    assert flatten_orders(None) is None
    single = TreeNode(0)
    assert flatten_orders(single) is single and single.right is None
    left_chain = build_tree([1, 2, None, 3])
    assert tree_to_list(flatten_orders(left_chain)) == [1, None, 2, None, 3]
    print("Problem 4: Convert Binary Tree of Bakery Orders to Linked List -- checks passed")

    assert is_complete(build_tree([
        "Croissant", "Cupcake", "Bagel", "Cake", "Pie", "Blondies"])) is True
    assert is_complete(build_tree(items)) is False
    assert is_complete(None) is True
    assert is_complete(TreeNode(1)) is True
    assert is_complete(build_tree([1, 2])) is True
    assert is_complete(build_tree([1, None, 2])) is False
    assert is_complete(build_tree([1, 2, None, 3])) is False
    print("Problem 5: Check Bakery Order Completeness -- checks passed")
