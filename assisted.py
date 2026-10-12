from collections import deque


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def level_order(root: TreeNode) -> list[list[int]]:
    """
    Returns nodes grouped by level, e.g. [[3], [9, 20], [15, 7]]
    """
    if not root:
        return []

    result = []
    queue = deque([root])

    while queue:
        level_size = len(queue)
        current_level = []

        for _ in range(level_size):
            node = queue.popleft()
            current_level.append(node.val)

            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

        result.append(current_level)

    return result


# Example usage:
#
#        3
#       / \
#      9  20
#        /  \
#       15   7
#
root = TreeNode(3)
root.left = TreeNode(9)
root.right = TreeNode(20)
root.right.left = TreeNode(15)
root.right.right = TreeNode(7)

print(level_order(root))  # [[3], [9, 20], [15, 7]]


# ---------------------------------------------------------------------------
# EDIT DISTANCE  (Levenshtein Distance)
# ---------------------------------------------------------------------------
# Problem: Given two strings word1 and word2, return the minimum number of
# single-character operations (insert, delete, replace) needed to transform
# word1 into word2.
#
# Example:  "horse" → "ros"  =  3 operations
#   horse → rorse  (replace 'h' with 'r')
#   rorse → rose   (delete 'r')
#   rose  → ros    (delete 'e')
#
# Approach – 2D DP table:
#   dp[i][j] = min operations to convert word1[:i] → word2[:j]
#
# Base cases:
#   dp[i][0] = i  (delete all i chars from word1)
#   dp[0][j] = j  (insert all j chars to reach word2)
#
# Recurrence:
#   If word1[i-1] == word2[j-1]:  dp[i][j] = dp[i-1][j-1]  (no operation needed)
#   Else:                          dp[i][j] = 1 + min(
#                                       dp[i-1][j],    # delete from word1
#                                       dp[i][j-1],    # insert into word1
#                                       dp[i-1][j-1]   # replace
#                                   )
# ---------------------------------------------------------------------------

def min_distance(word1: str, word2: str) -> int:
    m, n = len(word1), len(word2)

    # dp[i][j] = edit distance between word1[:i] and word2[:j]
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(
                    dp[i - 1][j],      # delete
                    dp[i][j - 1],      # insert
                    dp[i - 1][j - 1],  # replace
                )

    return dp[m][n]


# Example usage:
print(min_distance("horse", "ros"))     # 3
print(min_distance("intention", "execution"))  # 5
print(min_distance("", "abc"))          # 3
print(min_distance("abc", "abc"))       # 0


# ---------------------------------------------------------------------------
# TWO SUM
# ---------------------------------------------------------------------------
# Problem: Given an array of integers and a target, return the indices of the
# two numbers that add up to the target. Each input has exactly one solution
# and you may not use the same element twice.
#
# Example:  nums = [2, 7, 11, 15], target = 9  →  [0, 1]  (2 + 7 = 9)
#
# Approach – hash map O(n):
#   For each number x, check if (target - x) has already been seen.
#   If yes, return both indices immediately. If no, record x and move on.
# ---------------------------------------------------------------------------

def two_sum(nums: list[int], target: int) -> list[int]:
    seen = {}  # value → index

    for i, num in enumerate(nums):
        complement = target - num

        if complement in seen:
            return [seen[complement], i]

        seen[num] = i

    return []


# Example usage:
print(two_sum([2, 7, 11, 15], target=9))   # [0, 1]
print(two_sum([3, 2, 4],      target=6))   # [1, 2]
print(two_sum([3, 3],         target=6))   # [0, 1]
