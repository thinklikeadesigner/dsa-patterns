# Binary Search [Google Heavy]

## When to Use
When searching in a **sorted array**, or when you can frame the problem as "find the minimum/maximum value that satisfies a condition" (**binary search on answer**). Key signal: monotonic property — if condition holds for x, it holds for all x' > x (or all x' < x).

## Core Idea
Cut the search space in half each iteration. Classic binary search finds an element; "binary search on answer" searches over possible answer values and checks feasibility. O(log n) time.

## Template Code

```python
# Classic: find target in sorted array
def binary_search(arr, target):
    lo, hi = 0, len(arr) - 1
    while lo <= hi:
        mid = lo + (hi - lo) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1

# Find leftmost (first) position where condition is true
def bisect_left(arr, target):
    lo, hi = 0, len(arr)
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid
    return lo

# Binary search on answer
def binary_search_on_answer(lo, hi):
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if feasible(mid):
            hi = mid       # mid could be the answer, search left
        else:
            lo = mid + 1   # mid is too small
    return lo

def feasible(value):
    # Problem-specific: can we achieve the goal with this value?
    pass
```

## Key Variations
- **Classic**: Search for exact value
- **Bisect left/right**: First/last occurrence, insertion point
- **Search on answer**: Koko eating bananas, split array largest sum, capacity to ship packages — "minimize the maximum" or "maximize the minimum"
- **Search on rotated array**: Find pivot, then binary search on correct half

## Problems Solved
| Problem | Date | Result | Notes |
|---------|------|--------|-------|

## My Mistakes
- (none yet)
