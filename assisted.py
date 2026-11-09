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


# ---------------------------------------------------------------------------
# 0/1 KNAPSACK
# ---------------------------------------------------------------------------
# Problem: Given a knapsack of capacity W and n items each with a weight and
# a value, pick items to maximise total value without exceeding W.
# Each item can only be taken once (0/1 — take it or leave it).
#
# Example:
#   capacity = 6
#   weights  = [1, 2, 3, 5]
#   values   = [1, 6, 10, 16]
#   → best choice: items with weights 2 and 3  (value 6 + 10 = 17, total weight 5 ≤ 6)
#     OR item with weight 5 alone              (value 16, weight 5 ≤ 6)
#     Optimal: weight 1 + 2 + 3 = 6, value 1 + 6 + 10 = 17  ✓
#
# Approach – 2D DP table:
#   dp[i][w] = max value using the first i items with capacity w
#
# Recurrence:
#   Skip item i:  dp[i][w] = dp[i-1][w]
#   Take item i:  dp[i][w] = dp[i-1][w - weights[i-1]] + values[i-1]
#                             (only valid if weights[i-1] <= w)
#   dp[i][w] = max of both options
#
# Base case: dp[0][w] = 0 for all w  (no items → zero value)
# ---------------------------------------------------------------------------

def knapsack(weights: list[int], values: list[int], capacity: int) -> int:
    n = len(weights)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        w_i = weights[i - 1]
        v_i = values[i - 1]

        for w in range(capacity + 1):
            # Option 1: skip item i
            dp[i][w] = dp[i - 1][w]

            # Option 2: take item i (only if it fits)
            if w_i <= w:
                take = dp[i - 1][w - w_i] + v_i
                dp[i][w] = max(dp[i][w], take)

    return dp[n][capacity]


def knapsack_items(weights: list[int], values: list[int], capacity: int) -> tuple[int, list[int]]:
    """Returns (max_value, list of chosen item indices) by backtracking the DP table."""
    n = len(weights)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        w_i, v_i = weights[i - 1], values[i - 1]
        for w in range(capacity + 1):
            dp[i][w] = dp[i - 1][w]
            if w_i <= w:
                dp[i][w] = max(dp[i][w], dp[i - 1][w - w_i] + v_i)

    # Backtrack to find which items were taken
    chosen = []
    w = capacity
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:   # item i was taken
            chosen.append(i - 1)        # 0-indexed
            w -= weights[i - 1]

    return dp[n][capacity], chosen[::-1]


# Example usage:
weights  = [1, 2, 3, 5]
values   = [1, 6, 10, 16]
capacity = 6

print(knapsack(weights, values, capacity))          # 17

max_val, items = knapsack_items(weights, values, capacity)
print(f"Max value: {max_val}")                      # 17
print(f"Items taken (0-indexed): {items}")          # [0, 1, 2]
print(f"Weights used: {[weights[i] for i in items]}")  # [1, 2, 3]
print(f"Values used:  {[values[i]  for i in items]}")  # [1, 6, 10]


# ---------------------------------------------------------------------------
# LONGEST COMMON SUBSEQUENCE  (LCS)
# ---------------------------------------------------------------------------
# Problem: Given two strings, find the length of their longest common
# subsequence — a sequence of characters that appears in both strings in the
# same relative order, but not necessarily contiguously.
#
# Example:  s1 = "abcde",  s2 = "ace"
#   LCS = "ace",  length = 3
#
# Note: "ace" is NOT a substring (it skips chars), but it IS a subsequence.
#
# Approach – 2D DP table:
#   dp[i][j] = length of LCS of s1[:i] and s2[:j]
#
# Recurrence:
#   If s1[i-1] == s2[j-1]:  dp[i][j] = dp[i-1][j-1] + 1   (extend the match)
#   Else:                    dp[i][j] = max(dp[i-1][j],     (skip char from s1)
#                                           dp[i][j-1])     (skip char from s2)
#
# Base case: dp[i][0] = dp[0][j] = 0  (empty string has no common subsequence)
# ---------------------------------------------------------------------------

def lcs_length(s1: str, s2: str) -> int:
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    return dp[m][n]


def lcs_string(s1: str, s2: str) -> str:
    """Reconstructs the actual LCS string by backtracking the DP table."""
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    # Backtrack from dp[m][n] to reconstruct the sequence
    result = []
    i, j = m, n
    while i > 0 and j > 0:
        if s1[i - 1] == s2[j - 1]:
            result.append(s1[i - 1])   # this character is part of the LCS
            i -= 1
            j -= 1
        elif dp[i - 1][j] > dp[i][j - 1]:
            i -= 1                      # came from skipping s1[i-1]
        else:
            j -= 1                      # came from skipping s2[j-1]

    return "".join(reversed(result))


# Example usage:
print(lcs_length("abcde", "ace"))              # 3
print(lcs_length("abc", "abc"))                # 3
print(lcs_length("abc", "def"))                # 0

print(lcs_string("abcde", "ace"))              # ace
print(lcs_string("AGGTAB", "GXTXAYB"))         # GTAB
