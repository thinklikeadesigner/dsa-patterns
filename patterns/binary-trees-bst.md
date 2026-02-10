# Binary Trees & BSTs [Google + Meta]

## When to Use
Any problem involving a tree data structure. Key signals: "given a binary tree", "BST", "serialize/deserialize", "lowest common ancestor", "path sum", "validate BST". Most tree problems are solved with recursive DFS (pre/in/post-order).

## Core Idea
Think recursively: solve the problem for left subtree, solve for right subtree, combine results at the current node. Decide which traversal order you need:
- **Pre-order** (root → left → right): serialize, copy tree
- **In-order** (left → root → right): BST gives sorted order
- **Post-order** (left → right → root): delete tree, calculate height, path problems where you need children's answers first

## Template Code

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

# Max depth (post-order)
def max_depth(root):
    if not root:
        return 0
    return 1 + max(max_depth(root.left), max_depth(root.right))

# Validate BST (in-order with bounds)
def is_valid_bst(root, lo=float('-inf'), hi=float('inf')):
    if not root:
        return True
    if root.val <= lo or root.val >= hi:
        return False
    return (is_valid_bst(root.left, lo, root.val) and
            is_valid_bst(root.right, root.val, hi))

# Lowest Common Ancestor
def lca(root, p, q):
    if not root or root == p or root == q:
        return root
    left = lca(root.left, p, q)
    right = lca(root.right, p, q)
    if left and right:
        return root
    return left or right

# Diameter of binary tree (track global max)
def diameter(root):
    result = [0]
    def height(node):
        if not node:
            return 0
        l = height(node.left)
        r = height(node.right)
        result[0] = max(result[0], l + r)
        return 1 + max(l, r)
    height(root)
    return result[0]

# Serialize / Deserialize (pre-order)
def serialize(root):
    if not root:
        return "null"
    return f"{root.val},{serialize(root.left)},{serialize(root.right)}"

def deserialize(data):
    vals = iter(data.split(","))
    def build():
        val = next(vals)
        if val == "null":
            return None
        node = TreeNode(int(val))
        node.left = build()
        node.right = build()
        return node
    return build()
```

## Key Patterns
- **Return info up**: Height, diameter, is balanced — post-order, return values from children
- **Pass info down**: Validate BST, path sum — pass constraints/accumulator as parameters
- **Global variable trick**: Diameter, max path sum — update a nonlocal/list variable during traversal
- **BST property**: In-order = sorted; use bounds for validation; search in O(h)

## Problems Solved
| Problem | Date | Result | Notes |
|---------|------|--------|-------|

## My Mistakes
- (none yet)
