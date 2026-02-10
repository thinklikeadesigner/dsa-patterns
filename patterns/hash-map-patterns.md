# Hash Map Patterns [Google + Meta]

## When to Use
When you need **O(1) lookups** to check existence, count frequencies, or group items. Key signals: "find a pair that sums to", "group anagrams", "first non-repeating", "count occurrences", "subarray sum equals k". If brute force is O(n^2) because of a nested search, a hash map often makes it O(n).

## Core Idea
Trade space for time. Store previously seen elements/counts in a dictionary so you can answer "have I seen X before?" or "how many times has X appeared?" in O(1).

## Template Code

```python
from collections import defaultdict, Counter

# Two Sum (classic — complement lookup)
def two_sum(nums, target):
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []

# Frequency map / group by key
def group_anagrams(strs):
    groups = defaultdict(list)
    for s in strs:
        key = tuple(sorted(s))  # or frequency tuple
        groups[key].append(s)
    return list(groups.values())

# Subarray sum equals k (prefix sum + hash map)
def subarray_sum(nums, k):
    count = 0
    prefix = 0
    prefix_counts = {0: 1}
    for num in nums:
        prefix += num
        if prefix - k in prefix_counts:
            count += prefix_counts[prefix - k]
        prefix_counts[prefix] = prefix_counts.get(prefix, 0) + 1
    return count

# First non-repeating character
def first_unique(s):
    freq = Counter(s)
    for i, ch in enumerate(s):
        if freq[ch] == 1:
            return i
    return -1

# Longest consecutive sequence
def longest_consecutive(nums):
    num_set = set(nums)
    best = 0
    for n in num_set:
        if n - 1 not in num_set:  # start of a sequence
            length = 1
            while n + length in num_set:
                length += 1
            best = max(best, length)
    return best
```

## Key Variations
- **Complement lookup**: Two Sum, pair problems
- **Frequency counting**: Anagrams, majority element, top k frequent
- **Prefix sum + map**: Subarray sum equals k, continuous subarray sum
- **Set for O(1) membership**: Longest consecutive sequence
- **Index tracking**: Store last-seen index for substring problems

## Problems Solved
| Problem | Date | Result | Notes |
|---------|------|--------|-------|

## My Mistakes
- (none yet)
