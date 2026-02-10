# Prefix Sums [Google + Meta]

## When to Use
When you need to answer **range sum queries** efficiently, or find subarrays with a given sum. Key signal: "subarray sum", "range sum query", "sum between indices i and j", "number of subarrays with sum k". Build prefix sum once, answer queries in O(1).

## Core Idea
Precompute `prefix[i] = sum(arr[0..i-1])`. Then `sum(arr[i..j]) = prefix[j+1] - prefix[i]`. This turns O(n) range sum queries into O(1). Combined with a hash map, it solves "count subarrays with sum k" in O(n).

## Template Code

```python
# Build prefix sum array
def build_prefix(arr):
    prefix = [0] * (len(arr) + 1)
    for i in range(len(arr)):
        prefix[i + 1] = prefix[i] + arr[i]
    return prefix

# Range sum query
def range_sum(prefix, i, j):
    return prefix[j + 1] - prefix[i]  # sum of arr[i..j]

# Subarray Sum Equals K (prefix sum + hash map)
def subarray_sum(nums, k):
    count = 0
    prefix = 0
    seen = {0: 1}  # prefix_sum -> count of occurrences

    for num in nums:
        prefix += num
        if prefix - k in seen:
            count += seen[prefix - k]
        seen[prefix] = seen.get(prefix, 0) + 1

    return count

# Continuous Subarray Sum (sum is multiple of k)
def check_subarray_sum(nums, k):
    prefix = 0
    seen = {0: -1}  # remainder -> earliest index

    for i, num in enumerate(nums):
        prefix += num
        remainder = prefix % k if k else prefix
        if remainder in seen:
            if i - seen[remainder] >= 2:
                return True
        else:
            seen[remainder] = i

    return False

# 2D Prefix Sum
def build_prefix_2d(matrix):
    rows, cols = len(matrix), len(matrix[0])
    prefix = [[0] * (cols + 1) for _ in range(rows + 1)]
    for r in range(rows):
        for c in range(cols):
            prefix[r + 1][c + 1] = (matrix[r][c]
                                      + prefix[r][c + 1]
                                      + prefix[r + 1][c]
                                      - prefix[r][c])
    return prefix

def region_sum(prefix, r1, c1, r2, c2):
    return (prefix[r2 + 1][c2 + 1]
            - prefix[r1][c2 + 1]
            - prefix[r2 + 1][c1]
            + prefix[r1][c1])

# Product Except Self (prefix product from left and right)
def product_except_self(nums):
    n = len(nums)
    result = [1] * n
    left = 1
    for i in range(n):
        result[i] = left
        left *= nums[i]
    right = 1
    for i in range(n - 1, -1, -1):
        result[i] *= right
        right *= nums[i]
    return result
```

## Key Variations
- **1D range sum**: Basic prefix sum, O(1) queries
- **Subarray sum = k**: Prefix sum + hash map (complement lookup)
- **2D prefix sum**: Range queries on a matrix
- **Prefix product**: Product except self (left and right passes)
- **Prefix XOR**: For range XOR queries

## Problems Solved
| Problem | Date | Result | Notes |
|---------|------|--------|-------|

## My Mistakes
- (none yet)
