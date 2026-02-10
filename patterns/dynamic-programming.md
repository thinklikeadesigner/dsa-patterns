# Dynamic Programming [Google Only]

> **Note: Meta has banned DP from interviews. Only study this for Google.**

## When to Use
When a problem has **overlapping subproblems** and **optimal substructure**. Key signals: "minimum cost", "number of ways", "can you reach", "longest/shortest subsequence". If brute force is exponential and you see repeated work, it's likely DP.

## Core Idea
Break the problem into subproblems, solve each once, and store results. Two approaches:
- **Top-down** (memoization): Recursive + cache
- **Bottom-up** (tabulation): Iterative, fill a table

The hardest part is defining the **state** and **transition**.

## Template Code

```python
from functools import lru_cache

# 1D DP — Climbing Stairs / Fibonacci
def climb_stairs(n):
    if n <= 2:
        return n
    dp = [0] * (n + 1)
    dp[1], dp[2] = 1, 2
    for i in range(3, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]
    return dp[n]

# 1D DP — Coin Change (min coins)
def coin_change(coins, amount):
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    for i in range(1, amount + 1):
        for coin in coins:
            if coin <= i:
                dp[i] = min(dp[i], dp[i - coin] + 1)
    return dp[amount] if dp[amount] != float('inf') else -1

# 2D DP — Longest Common Subsequence
def lcs(text1, text2):
    m, n = len(text1), len(text2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i - 1] == text2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    return dp[m][n]

# 2D DP — 0/1 Knapsack
def knapsack(weights, values, capacity):
    n = len(weights)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for w in range(capacity + 1):
            dp[i][w] = dp[i - 1][w]
            if weights[i - 1] <= w:
                dp[i][w] = max(dp[i][w], dp[i - 1][w - weights[i - 1]] + values[i - 1])
    return dp[n][capacity]

# Top-down with memoization
@lru_cache(maxsize=None)
def min_path_sum(grid, r=0, c=0):
    if r == len(grid) - 1 and c == len(grid[0]) - 1:
        return grid[r][c]
    if r >= len(grid) or c >= len(grid[0]):
        return float('inf')
    return grid[r][c] + min(min_path_sum(grid, r + 1, c),
                             min_path_sum(grid, r, c + 1))
```

## Key Categories
- **1D**: Climbing stairs, house robber, coin change, word break
- **2D**: LCS, edit distance, unique paths, knapsack
- **Interval DP**: Burst balloons, matrix chain multiplication
- **Bitmask DP**: Traveling salesman (state = set of visited cities)
- **Space optimization**: Often can reduce 2D to 1D by only keeping previous row

## Framework for Solving
1. **Define state**: What does `dp[i]` (or `dp[i][j]`) represent?
2. **Transition**: How do you compute `dp[i]` from smaller subproblems?
3. **Base case**: What are the trivially known values?
4. **Answer**: Where in the table is the final answer?

## Problems Solved
| Problem | Date | Result | Notes |
|---------|------|--------|-------|
| Grid Path Count (count paths avoiding "X") | 2026-02-08 | Struggled | Had to look at solution for the bug |
| Max Path Sum (grid, right/down moves) | 2026-02-08 | Struggled | Same or/and bug — didn't catch it despite just seeing it |
| Summing Squares (min perfect squares summing to n) | 2026-02-09 | Failed | 5 bugs: missing return on memo hit, loop over all numbers instead of perfect squares, recursive call didn't reduce n, subtracted 1 from count undoing the +1, unnecessary if/else branch |
| Counting Change (number of ways to make amount with coins) | 2026-02-09 | Watched | New problem — watched walkthrough, confidence 0. Code was correct but need to internalize the pattern. |
| Array Stepper (can you reach last index?) | 2026-02-09 | Struggled | 1 bug: used `i` as loop variable, shadowing the function parameter. Needed 1 hint to spot it. |

## My Mistakes
- **2026-02-08**: Grid path count — used `or` instead of `and` for the destination base case (`r == last_row or c == last_col` instead of `and`). This incorrectly assumes any cell on the last row/column has exactly 1 path to the end, ignoring possible "X" blockers along the remaining edge. The recursion handles edges naturally — only the actual destination `(rows-1, cols-1)` should return 1.
- **2026-02-08**: Max path sum — **SAME BUG AGAIN**. `or` instead of `and` on the destination check. Returned only the current cell's value when on the last row/col, skipping remaining cells along the edge. **Drill this: the only true base case is the bottom-right corner. Let recursion + out-of-bounds handle the rest.**
- **2026-02-09**: Summing Squares — Multiple fundamental issues:
  1. **Forgot `return` on memo lookup** — `memo[n]` instead of `return memo[n]`. Memo was useless.
  2. **Looped over all numbers, not just perfect squares** — should iterate `i` from 1 to `sqrt(n)` and use `i*i` as the square.
  3. **Recursive call didn't reduce the problem** — called `ss(n, memo)` instead of `ss(n - i*i, memo)`. Infinite recursion.
  4. **Subtracted 1 from count in `min()`** — undid the `1 +` that correctly counts using one square.
  5. **Unnecessary if/else checking `is_perfect_square`** — the loop itself should only generate perfect squares.
  **Drill this: in "min coins/squares" DP, loop over the *choices* (squares), subtract the choice from n, recurse on the remainder. Pattern is exactly like coin change.**
- **2026-02-09**: Array Stepper — **Variable shadowing**: used `i` as the `for` loop variable, overwriting the function parameter `i`. This meant `i + 1` stepped from the loop counter instead of the current position, and `memo[i]` cached the wrong index. **Drill this: never reuse parameter names as loop variables. Use descriptive names (`step`, `qty`, `offset`).**
