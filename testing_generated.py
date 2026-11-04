def min_distance(word1: str, word2: str) -> int:
    m, n = len(word1), len(word2)

    # Build a (m+1) x (n+1) table.
    # dp[i][j] = min operations to convert word1[:i] into word2[:j]
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # Base cases: converting to/from an empty string costs i or j operations
    for i in range(m + 1):
        dp[i][0] = i   # delete all chars from word1
    for j in range(n + 1):
        dp[0][j] = j   # insert all chars of word2

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                # Characters match — no operation needed
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(
                    dp[i - 1][j],      # delete  word1[i-1]
                    dp[i][j - 1],      # insert  word2[j-1]
                    dp[i - 1][j - 1],  # replace word1[i-1] with word2[j-1]
                )

    return dp[m][n]


def print_dp_table(word1: str, word2: str) -> None:
    """Prints the filled DP table so you can trace the solution."""
    m, n = len(word1), len(word2)
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
                dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])

    header = "      " + "  ".join(f'"{c}"' for c in [""] + list(word2))
    print(header)
    for i, row in enumerate(dp):
        label = f'"{word1[i - 1]}"' if i > 0 else '" "'
        print(f"  {label}  " + "   ".join(str(v) for v in row))
    print()


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    cases = [
        ("horse",     "ros",       3),
        ("intention", "execution", 5),
        ("",          "abc",       3),
        ("abc",       "abc",       0),
        ("a",         "",          1),
    ]

    for word1, word2, expected in cases:
        result = min_distance(word1, word2)
        status = "PASS" if result == expected else "FAIL"
        print(f"[{status}]  min_distance({word1!r}, {word2!r}) = {result}  (expected {expected})")

    print()
    print("DP table for 'horse' → 'ros':")
    print_dp_table("horse", "ros")
