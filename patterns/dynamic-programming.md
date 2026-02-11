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

### Tabulation (Bottom-Up) Examples

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
```

### Memoization (Top-Down) Pattern

**Standard memoization template:**
```python
def problem(params):
  return helper(params, {})

def helper(params, memo):
  # 1. Check memo
  if key in memo:
    return memo[key]

  # 2. Base case(s)
  if base_condition:
    return base_value

  # 3. Recursive logic
  result = compute_from_subproblems()

  # 4. Store and return
  memo[key] = result
  return result
```

**Category 1: Simple Numeric Sequences**
```python
# Fibonacci
def fib(n):
  return _fib(n, {})

def _fib(n, memo):
  if n in memo:
    return memo[n]
  if n == 0:
    return 0
  if n == 1:
    return 1

  memo[n] = _fib(n - 1, memo) + _fib(n - 2, memo)
  return memo[n]

# Tribonacci
def tribonacci(n):
  return _tribonacci(n, {})

def _tribonacci(n, memo):
  if n in memo:
    return memo[n]
  if n == 0:
    return 0
  if n in (1, 2):
    return 1

  memo[n] = (_tribonacci(n - 1, memo) +
             _tribonacci(n - 2, memo) +
             _tribonacci(n - 3, memo))
  return memo[n]
```

**Category 2: Decision Problems (Yes/No)**
```python
# Sum Possible (can you make target sum with numbers?)
def sum_possible(amount, numbers):
  return _sum_possible(amount, numbers, {})

def _sum_possible(amount, numbers, memo):
  if amount in memo:
    return memo[amount]
  if amount < 0:
    return False
  if amount == 0:
    return True

  for num in numbers:
    if _sum_possible(amount - num, numbers, memo):
      memo[amount] = True
      return True

  memo[amount] = False
  return False

# Array Stepper (can you reach the end?)
def array_stepper(numbers):
  return _array_stepper(numbers, 0, {})

def _array_stepper(numbers, i, memo):
  if i in memo:
    return memo[i]
  if i >= len(numbers) - 1:
    return True

  max_step = numbers[i]
  for step in range(1, max_step + 1):
    if _array_stepper(numbers, i + step, memo):
      memo[i] = True
      return True

  memo[i] = False
  return False
```

**Category 3: Minimization Problems**
```python
# Min Change (fewest coins to make amount)
def min_change(amount, coins):
  result = _min_change(amount, coins, {})
  return -1 if result == float('inf') else result

def _min_change(amount, coins, memo):
  if amount in memo:
    return memo[amount]
  if amount < 0:
    return float('inf')
  if amount == 0:
    return 0

  min_coins = float('inf')
  for coin in coins:
    num_coins = 1 + _min_change(amount - coin, coins, memo)
    min_coins = min(min_coins, num_coins)

  memo[amount] = min_coins
  return min_coins

# Summing Squares (min perfect squares summing to n)
import math

def summing_squares(n):
  return _summing_squares(n, {})

def _summing_squares(n, memo):
  if n in memo:
    return memo[n]
  if n == 0:
    return 0

  min_squares = float('inf')
  for i in range(1, int(math.sqrt(n)) + 1):
    square = i * i
    num_squares = 1 + _summing_squares(n - square, memo)
    min_squares = min(min_squares, num_squares)

  memo[n] = min_squares
  return memo[n]

# Quickest Concat (min words to form string)
def quickest_concat(s, words):
  result = _quickest_concat(s, words, 0, {})
  return -1 if result == float('inf') else result

def _quickest_concat(s, words, i, memo):
  if i in memo:
    return memo[i]
  if i == len(s):
    return 0

  min_words = float('inf')
  for word in words:
    if s.startswith(word, i):
      attempt = 1 + _quickest_concat(s, words, i + len(word), memo)
      min_words = min(attempt, min_words)

  memo[i] = min_words
  return min_words
```

**Category 4: Counting Problems**
```python
# Counting Change (number of ways to make amount)
def counting_change(amount, coins):
  return _counting_change(amount, coins, 0, {})

def _counting_change(amount, coins, i, memo):
  key = (amount, i)
  if key in memo:
    return memo[key]
  if amount == 0:
    return 1
  if i == len(coins):
    return 0

  coin = coins[i]
  total = 0
  for qty in range(0, (amount // coin) + 1):
    remainder = amount - (qty * coin)
    total += _counting_change(remainder, coins, i + 1, memo)

  memo[key] = total
  return total

# Count Compounds (count ways to form compound from elements)
def count_compounds(compound, elements):
  elements = [e.lower() for e in elements]
  return _count_compounds(compound, elements, 0, {})

def _count_compounds(compound, elements, i, memo):
  if i in memo:
    return memo[i]
  if i == len(compound):
    return 1

  count = 0
  for element in elements:
    if compound.startswith(element, i):
      count += _count_compounds(compound, elements, i + len(element), memo)

  memo[i] = count
  return memo[i]
```

**Category 5: Grid Problems (2D State)**
```python
# Count Paths (count paths avoiding obstacles)
def count_paths(grid):
  return _count_paths(grid, 0, 0, {})

def _count_paths(grid, r, c, memo):
  pos = (r, c)
  if pos in memo:
    return memo[pos]
  if r == len(grid) or c == len(grid[0]) or grid[r][c] == "X":
    return 0
  if r == len(grid) - 1 and c == len(grid[0]) - 1:
    return 1

  memo[pos] = (_count_paths(grid, r + 1, c, memo) +
               _count_paths(grid, r, c + 1, memo))
  return memo[pos]

# Max Path Sum (maximize sum along path)
def max_path_sum(grid):
  return _max_path_sum(grid, 0, 0, {})

def _max_path_sum(grid, r, c, memo):
  pos = (r, c)
  if pos in memo:
    return memo[pos]
  if r == len(grid) or c == len(grid[0]):
    return float('-inf')
  if r == len(grid) - 1 and c == len(grid[0]) - 1:
    return grid[r][c]

  down = _max_path_sum(grid, r + 1, c, memo)
  right = _max_path_sum(grid, r, c + 1, memo)

  memo[pos] = grid[r][c] + max(right, down)
  return memo[pos]
```

**Category 6: Interval/Range DP (Two-Pointer State)**
```python
# Max Palindromic Subsequence
def max_palin_subsequence(string):
  return _max_palin_subsequence(string, 0, len(string) - 1, {})

def _max_palin_subsequence(string, i, j, memo):
  key = (i, j)
  if key in memo:
    return memo[key]
  if i == j:
    return 1
  if i > j:
    return 0

  if string[i] == string[j]:
    memo[key] = 2 + _max_palin_subsequence(string, i + 1, j - 1, memo)
  else:
    memo[key] = max(
      _max_palin_subsequence(string, i + 1, j, memo),
      _max_palin_subsequence(string, i, j - 1, memo)
    )

  return memo[key]

# Overlap Subsequence (longest common subsequence)
def overlap_subsequence(s1, s2):
  return _overlap_subsequence(s1, s2, 0, 0, {})

def _overlap_subsequence(s1, s2, i, j, memo):
  key = (i, j)
  if key in memo:
    return memo[key]
  if i >= len(s1) or j >= len(s2):
    return 0

  if s1[i] == s2[j]:
    memo[key] = 1 + _overlap_subsequence(s1, s2, i + 1, j + 1, memo)
  else:
    memo[key] = max(
      _overlap_subsequence(s1, s2, i + 1, j, memo),
      _overlap_subsequence(s1, s2, i, j + 1, memo)
    )

  return memo[key]
```

**Category 7: Word Break Pattern (String + Index)**
```python
# Can Concat (can words form string?)
def can_concat(s, words):
  return _can_concat(s, words, 0, {})

def _can_concat(s, words, i, memo):
  if i in memo:
    return memo[i]
  if i == len(s):
    return True

  for word in words:
    if s.startswith(word, i):
      if _can_concat(s, words, i + len(word), memo):
        memo[i] = True
        return True

  memo[i] = False
  return False

# Valid Compound (chemistry word break)
def valid_compound(compound, elements):
  return _valid_compound(compound, elements, 0, {})

def _valid_compound(compound, elements, i, memo):
  if i == len(compound):
    return True
  if i in memo:
    return memo[i]

  for element in elements:
    if compound.startswith(element.lower(), i):
      if _valid_compound(compound, elements, i + len(element), memo):
        memo[i] = True
        return True

  memo[i] = False
  return False
```

**Category 8: Graph + DP (DAG Longest Path)**
```python
# Longest Path in DAG (counts edges)
def longest_path(graph):
  memo = {}
  max_path = 0

  for node in graph:
    current_path = dfs(graph, node, memo)
    max_path = max(max_path, current_path)

  return max_path

def dfs(graph, node, memo):
  if node in memo:
    return memo[node]

  max_length = 0
  for neighbor in graph[node]:
    length = dfs(graph, neighbor, memo) + 1
    max_length = max(length, max_length)

  memo[node] = max_length
  return memo[node]

# Semesters Required (counts nodes, not edges)
def semesters_required(num_courses, prereqs):
  graph = build_graph(num_courses, prereqs)
  memo = {}

  # Calculate longest path from each node
  max_length = 0
  for node in graph:
    current_length = dfs(graph, node, memo)
    max_length = max(max_length, current_length)

  return max_length

def dfs(graph, node, memo):
  # If already calculated, return memoized result
  if node in memo:
    return memo[node]

  # Find the longest path among all neighbors
  max_length = 0
  for neighbor in graph[node]:
    neighbor_length = dfs(graph, neighbor, memo)
    max_length = max(neighbor_length, max_length)

  # This node's path length = 1 (itself) + longest neighbor path
  # For leaf nodes: graph[node] is empty, so max_length = 0, result = 1
  memo[node] = 1 + max_length
  return memo[node]

def build_graph(num_courses, prereqs):
  graph = {i: [] for i in range(num_courses)}
  for a, b in prereqs:
    graph[a].append(b)
  return graph
```

**Category 9: House Robber Pattern (Skip Elements)**
```python
# Non-Adjacent Sum (max sum without adjacent elements)
def non_adjacent_sum(nums):
  return _non_adjacent_sum(nums, 0, {})

def _non_adjacent_sum(nums, i, memo):
  if i in memo:
    return memo[i]
  if i >= len(nums):
    return 0

  include = nums[i] + _non_adjacent_sum(nums, i + 2, memo)
  exclude = _non_adjacent_sum(nums, i + 1, memo)

  memo[i] = max(include, exclude)
  return memo[i]
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

## Optimization: String Slicing → Index Pointers
When your DP recurses on substrings, replace slicing with `(i, j)` pointers. Avoids O(n) copy per call and makes memo keys cheap.

| Slicing | Pointers |
|---------|----------|
| `string` (whole) | `string[i:j]` (never actually sliced) |
| `string[1:]` | `i + 1, j` |
| `string[:-1]` | `i, j - 1` |
| `string[1:-1]` | `i + 1, j - 1` |
| `len(string) == 0` | `i > j` |
| `len(string) == 1` | `i == j` |
| `string[0]` / `string[-1]` | `string[i]` / `string[j]` |
| `memo[string]` | `memo[(i, j)]` |

### Example: Can Concat (Word Break Pattern)

**Brute force (no memoization — exponential time):**
```python
def can_concat(s, words):
  if s == "":
    return True

  for word in words:
    if s.startswith(word):
      suffix = s[len(word):]
      if can_concat(suffix, words):
        return True

  return False
```

**Slicing version with memo (slower — O(n) per slice):**
```python
def can_concat(s, words):
  return _can_concat(s, words, {})

def _can_concat(s, words, memo):
  if s in memo:
    return memo[s]
  if s == "":
    return True

  for word in words:
    if s.startswith(word):
      suffix = s[len(word):]  # O(n) string copy
      if _can_concat(suffix, words, memo):
        memo[s] = True
        return True

  memo[s] = False
  return False
```

**Pointer version (faster — O(1) per step):**
```python
def can_concat(s, words):
  return _can_concat(s, words, 0, {})

def _can_concat(s, words, i, memo):
  if i in memo:
    return memo[i]
  if i == len(s):
    return True

  for word in words:
    if s.startswith(word, i):  # check at position i
      if _can_concat(s, words, i + len(word), memo):
        memo[i] = True
        return True

  memo[i] = False
  return False
```

**Key changes:**
- `s` → `i` (position instead of substring)
- `s == ""` → `i == len(s)` (reached the end)
- `s.startswith(word)` → `s.startswith(word, i)` (check at position i)
- `s[len(word):]` → `i + len(word)` (advance pointer, no slicing)
- `memo[s]` → `memo[i]` (integer keys instead of string keys)

## Problems Solved
| Problem | Date | Result | Notes |
|---------|------|--------|-------|
| Grid Path Count (count paths avoiding "X") | 2026-02-08 | Struggled | Had to look at solution for the bug |
| Max Path Sum (grid, right/down moves) | 2026-02-08 | Struggled | Same or/and bug — didn't catch it despite just seeing it |
| Summing Squares (min perfect squares summing to n) | 2026-02-09 | Failed | 5 bugs: missing return on memo hit, loop over all numbers instead of perfect squares, recursive call didn't reduce n, subtracted 1 from count undoing the +1, unnecessary if/else branch |
| Counting Change (number of ways to make amount with coins) | 2026-02-09 | Watched | New problem — watched walkthrough, confidence 0. Code was correct but need to internalize the pattern. |
| Array Stepper (can you reach last index?) | 2026-02-09 | Struggled | 1 bug: used `i` as loop variable, shadowing the function parameter. Needed 1 hint to spot it. |
| Max Palindromic Subsequence | 2026-02-09 | Struggled | Missed the core decision (check first==last), tried wrong comparisons, forgot to memo the match branch. Needed several hints but worked through each fix. |
| Can Concat (can words concatenate to form string?) | 2026-02-11 | Solved | 2 bugs: off-by-one in slicing (`slice_factor + 1` instead of `slice_factor`), and used `or` instead of `and` for the prefix match check. Fixed both with hints. |
| Quickest Concat (min words to form string) | 2026-02-11 | Solved | Extended Can Concat to count minimum words. Key insight: same structure as min coins problem — `min(1 + recurse(remaining))` across all valid word choices. Return -1 if impossible (check for `float('inf')`). |
| Valid Compound (check if elements form compound) | 2026-02-11 | Solved | Recognized as word break pattern, used pointer optimization. Pre-processed elements to lowercase once. Clean application of the pattern with minor case-handling twist. |
| Count Compounds (count ways to form compound) | 2026-02-11 | Solved | Word break counting variant. Fixed base case (return 1 when complete) and initial count (start at 0, accumulate all paths). Needed hints on base case value and removing early return. |

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
- **2026-02-09**: Max Palindromic Subsequence — Three issues:
  1. **Missed the core palindrome check** — didn't compare `string[0] == string[-1]`. This is the key decision that defines the problem.
  2. **Wrong slicing** — used `string[:1]` (first char) instead of `string[:-1]` (everything but last). Also tried `string[2:]`/`string[:-2]` instead of `string[1:-1]` for chopping both ends.
  3. **Forgot to memo the match branch** — returned `2 + recurse(...)` without storing in memo first.
  **Drill this: palindrome DP has two branches — match (2 + recurse middle) vs no match (max of drop-first, drop-last). Always memo before returning.**
- **2026-02-11**: Can Concat — Used `or` instead of `and` when checking the condition to continue recursing. **Pattern: when you have a condition that must be true before recursing down a branch, use `and` to combine the condition check with the recursive call.** Example: `if word == beginning_of_s and recurse(...)` means "only recurse if the condition holds." Using `or` would incorrectly return True whenever the condition is true, regardless of the recursion result.
