# Monotonic Stack [Google + Meta]

## When to Use
When you need the **next greater/smaller element** for each element in an array, or problems involving histograms and rectangles. Key signal: "next greater element", "daily temperatures", "largest rectangle in histogram", "stock span". The stack maintains a monotonic (increasing or decreasing) order.

## Core Idea
Maintain a stack where elements are always in sorted order. When a new element violates the order, pop elements and process them — the new element is the "answer" for the popped elements. This gives O(n) time because each element is pushed and popped at most once.

## Template Code

```python
# Next Greater Element (monotonic decreasing stack)
def next_greater(nums):
    n = len(nums)
    result = [-1] * n
    stack = []  # indices

    for i in range(n):
        while stack and nums[i] > nums[stack[-1]]:
            idx = stack.pop()
            result[idx] = nums[i]
        stack.append(i)

    return result

# Daily Temperatures (same idea — next warmer day)
def daily_temperatures(temps):
    n = len(temps)
    result = [0] * n
    stack = []

    for i in range(n):
        while stack and temps[i] > temps[stack[-1]]:
            idx = stack.pop()
            result[idx] = i - idx
        stack.append(i)

    return result

# Largest Rectangle in Histogram
def largest_rectangle(heights):
    stack = []  # indices of increasing heights
    max_area = 0
    heights.append(0)  # sentinel to flush remaining

    for i, h in enumerate(heights):
        while stack and heights[stack[-1]] > h:
            height = heights[stack.pop()]
            width = i if not stack else i - stack[-1] - 1
            max_area = max(max_area, height * width)
        stack.append(i)

    heights.pop()  # remove sentinel
    return max_area

# Stock Span (monotonic decreasing — count days price was <=)
def stock_span(prices):
    result = []
    stack = []  # (price, span)

    for price in prices:
        span = 1
        while stack and stack[-1][0] <= price:
            span += stack.pop()[1]
        stack.append((price, span))
        result.append(span)

    return result
```

## Key Variations
- **Next greater** (decreasing stack): Pop when new element is larger
- **Next smaller** (increasing stack): Pop when new element is smaller
- **Previous greater/smaller**: Iterate right to left, or the answer is what's on top of stack when you push
- **Histogram**: Width calculation using indices on the stack
- **Circular array**: Iterate `2*n` with modular indexing

## Problems Solved
| Problem | Date | Result | Notes |
|---------|------|--------|-------|

## My Mistakes
- (none yet)
