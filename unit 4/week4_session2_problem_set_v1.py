"""UPI solutions for Week 4, Session 2, Problem Set Version 1."""


class TreeNode:
    def __init__(self, value, left=None, right=None):
        self.val = value
        self.left = left
        self.right = right


# 1. U: Follow only right children; never fall back to the left child.
# P: Append the current value, then move right until reaching None.
def right_vine(root):
    values = []
    current = root
    while current is not None:
        values.append(current.val)
        current = current.right
    return values


# 2. U: Problem 1 is iterative, so this version must be recursive.
# P: Append the current value and recursively visit its right child.
# Named separately so both solutions remain available in this file.
def right_vine_recursive(root):
    values = []

    def visit(node):
        if node is None:
            return
        values.append(node.val)
        visit(node.right)

    visit(root)
    return values


# 3. U: Postorder means left subtree, right subtree, then root.
# P: Recursively survey both children before appending the current value.
def survey_tree(root):
    values = []

    def visit(node):
        if node is None:
            return
        visit(node.left)
        visit(node.right)
        values.append(node.val)

    visit(root)
    return values


# 4. U: Every node contributes its stock once.
# P: Return current stock plus the sums of the left and right subtrees.
def sum_inventory(inventory):
    if inventory is None:
        return 0
    return inventory.val + sum_inventory(inventory.left) + sum_inventory(inventory.right)


# 5. U: Leaves are integers; internal nodes apply an operator to two children.
# P: Evaluate both children, then apply the current operator in left/right order.
def calculate_yield(root):
    if root.left is None and root.right is None:
        return root.val
    left = calculate_yield(root.left)
    right = calculate_yield(root.right)
    if root.val == "+":
        return left + right
    if root.val == "-":
        return left - right
    if root.val == "*":
        return left * right
    if root.val == "/":
        return left / right
    raise ValueError("Unsupported operator")


if __name__ == "__main__":
    ivy1 = TreeNode("Root", TreeNode("Node1", TreeNode("Leaf1")),
                    TreeNode("Node2", TreeNode("Leaf2"), TreeNode("Leaf3")))
    ivy2 = TreeNode("Root", TreeNode("Node1", TreeNode("Leaf1")))
    for solution in (right_vine, right_vine_recursive):
        assert solution(ivy1) == ["Root", "Node2", "Leaf3"]
        assert solution(ivy2) == ["Root"]
        assert solution(None) == []
    assert survey_tree(ivy1) == ["Leaf1", "Node1", "Leaf2", "Leaf3", "Node2", "Root"]
    assert survey_tree(None) == []
    inventory = TreeNode(40, TreeNode(5, TreeNode(20)),
                         TreeNode(10, TreeNode(1), TreeNode(30)))
    assert sum_inventory(inventory) == 106
    assert sum_inventory(None) == 0
    root = TreeNode("+", TreeNode("-", TreeNode(4), TreeNode(2)),
                    TreeNode("*", TreeNode(10), TreeNode(2)))
    assert calculate_yield(root) == 22
    assert calculate_yield(TreeNode("/", TreeNode(9), TreeNode(2))) == 4.5
    assert calculate_yield(TreeNode(7)) == 7
