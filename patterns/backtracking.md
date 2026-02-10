# Backtracking [Google + Meta]

## When to Use
When you need to find **all combinations, permutations, or subsets**, or solve a **constraint satisfaction** problem (N-Queens, Sudoku, word search). Key signal: "generate all", "find all valid", or any problem where you build a solution incrementally and need to undo choices.

## Core Idea
Recursively build candidates, and "backtrack" (undo the last choice) when a candidate can't lead to a valid solution. The template is: choose → explore → unchoose. Prune early to avoid unnecessary work.

## Template Code

```python
# Subsets (power set)
def subsets(nums):
    result = []
    def backtrack(start, path):
        result.append(path[:])  # copy current path
        for i in range(start, len(nums)):
            path.append(nums[i])
            backtrack(i + 1, path)
            path.pop()           # backtrack
    backtrack(0, [])
    return result

# Permutations
def permutations(nums):
    result = []
    def backtrack(path, used):
        if len(path) == len(nums):
            result.append(path[:])
            return
        for i in range(len(nums)):
            if used[i]:
                continue
            used[i] = True
            path.append(nums[i])
            backtrack(path, used)
            path.pop()
            used[i] = False
    backtrack([], [False] * len(nums))
    return result

# Combinations (n choose k)
def combine(n, k):
    result = []
    def backtrack(start, path):
        if len(path) == k:
            result.append(path[:])
            return
        for i in range(start, n + 1):
            path.append(i)
            backtrack(i + 1, path)
            path.pop()
    backtrack(1, [])
    return result

# Combination Sum (reuse allowed)
def combination_sum(candidates, target):
    result = []
    def backtrack(start, path, remaining):
        if remaining == 0:
            result.append(path[:])
            return
        for i in range(start, len(candidates)):
            if candidates[i] > remaining:
                break  # pruning (requires sorted input)
            path.append(candidates[i])
            backtrack(i, path, remaining - candidates[i])  # i, not i+1 (reuse)
            path.pop()
    candidates.sort()
    backtrack(0, [], target)
    return result
```

## Key Patterns
- **Subsets**: Loop from `start`, recurse with `i+1`, collect at every level
- **Permutations**: Loop from `0`, use `used[]` array, collect when path is full
- **Combinations**: Like subsets but stop at length k
- **Constraint satisfaction**: Add validity checks before recursing (pruning)
- **Dedup with sorting**: Sort input, skip `nums[i] == nums[i-1]` when `i > start`

## Problems Solved
| Problem | Date | Result | Notes |
|---------|------|--------|-------|

## My Mistakes
- (none yet)
