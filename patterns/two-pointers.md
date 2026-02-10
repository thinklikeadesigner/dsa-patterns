# Two Pointers [Google + Meta]

## When to Use
When you need to find pairs/triplets in a **sorted array**, or when you need to process elements from both ends of an array/string toward the middle. Also for "partition" style problems (move zeros, Dutch national flag).

## Core Idea
Use two indices that move toward each other (or in the same direction) to reduce O(n^2) brute force to O(n). The sorted property lets you decide which pointer to move based on whether the current sum/value is too large or too small.

## Template Code

```python
# Opposite direction (e.g., two-sum on sorted array)
def two_pointer_opposite(arr, target):
    left, right = 0, len(arr) - 1
    while left < right:
        curr = arr[left] + arr[right]
        if curr == target:
            return [left, right]
        elif curr < target:
            left += 1
        else:
            right -= 1
    return []

# Same direction (e.g., remove duplicates in-place)
def two_pointer_same(arr):
    slow = 0
    for fast in range(len(arr)):
        if arr[fast] != arr[slow]:
            slow += 1
            arr[slow] = arr[fast]
    return slow + 1  # length of unique portion
```

## Key Variations
- **Opposite ends**: Two Sum II, Container With Most Water, Trapping Rain Water
- **Same direction (slow/fast)**: Remove Duplicates, Move Zeros, Linked List Cycle
- **Three pointers**: 3Sum (fix one, two-pointer on rest)

## Problems Solved
| Problem | Date | Result | Notes |
|---------|------|--------|-------|

## My Mistakes
- (none yet)
