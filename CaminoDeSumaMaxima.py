class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def maxPathSum(root):
    max_sum = float('-inf')

    def dfs(node):
        nonlocal max_sum
        if not node:
            return 0

        left_max = max(dfs(node.left), 0)
        right_max = max(dfs(node.right), 0)

        max_sum = max(max_sum, left_max + right_max + node.val)

        return node.val + max(left_max, right_max)

    dfs(root)
    return max_sum

# EJEMPLO
root = TreeNode(10,
                TreeNode(2, TreeNode(20), TreeNode(1)),
                TreeNode(10, None, TreeNode(-25, TreeNode(3), TreeNode(4))))

print(maxPathSum(root))  # 42 (20 -> 2 -> 10 -> 10)
