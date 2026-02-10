# Sliding Window [Google + Meta]

## When to Use
When you need to find a **subarray or substring** that satisfies some condition (max sum, contains all characters, longest without repeats). The key signal: "contiguous subarray/substring" + some optimization or constraint.

## Core Idea
Maintain a window [left, right] that expands by moving `right` and contracts by moving `left`. Track window state (sum, character counts, etc.) incrementally instead of recomputing. Reduces O(n*k) to O(n).

## Template Code

```python
# Variable-size sliding window
def sliding_window(s):
    left = 0
    window = {}  # or any state tracker
    result = 0

    for right in range(len(s)):
        # Expand: add s[right] to window state
        window[s[right]] = window.get(s[right], 0) + 1

        # Shrink: while window is invalid, remove s[left]
        while window_is_invalid(window):
            window[s[left]] -= 1
            if window[s[left]] == 0:
                del window[s[left]]
            left += 1

        # Update result
        result = max(result, right - left + 1)

    return result

# Fixed-size sliding window
def fixed_window(arr, k):
    window_sum = sum(arr[:k])
    result = window_sum
    for i in range(k, len(arr)):
        window_sum += arr[i] - arr[i - k]
        result = max(result, window_sum)
    return result
```

## Key Variations
- **Fixed size**: Max sum subarray of size k
- **Variable size (longest)**: Longest substring without repeating chars — expand freely, shrink when invalid
- **Variable size (shortest)**: Minimum window substring — shrink when valid to find smallest
- **With hash map**: Track character frequencies for anagram/substring problems

## Problems Solved
| Problem | Date | Result | Notes |
|---------|------|--------|-------|

## My Mistakes
- (none yet)
