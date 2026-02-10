# Heap / Priority Queue [Google + Meta]

## When to Use
When you need to repeatedly find the **min or max element** efficiently, or maintain a **top-k** set. Key signals: "kth largest", "merge k sorted", "find median", "top k frequent", "schedule by deadline". If you keep extracting min/max, use a heap.

## Core Idea
A heap gives O(log n) insert and O(log n) extract-min/max, with O(1) peek. Python's `heapq` is a min-heap. For max-heap, negate values. For problems needing both min and max, use two heaps.

## Template Code

```python
import heapq

# Top K Frequent Elements
def top_k_frequent(nums, k):
    from collections import Counter
    freq = Counter(nums)
    return heapq.nlargest(k, freq.keys(), key=freq.get)

# Kth Largest Element (min-heap of size k)
def kth_largest(nums, k):
    heap = nums[:k]
    heapq.heapify(heap)
    for num in nums[k:]:
        if num > heap[0]:
            heapq.heapreplace(heap, num)
    return heap[0]

# Merge K Sorted Lists
def merge_k_lists(lists):
    heap = []
    for i, lst in enumerate(lists):
        if lst:
            heapq.heappush(heap, (lst.val, i, lst))

    dummy = curr = ListNode(0)
    while heap:
        val, i, node = heapq.heappop(heap)
        curr.next = node
        curr = curr.next
        if node.next:
            heapq.heappush(heap, (node.next.val, i, node.next))

    return dummy.next

# Find Median from Data Stream (two heaps)
class MedianFinder:
    def __init__(self):
        self.lo = []  # max-heap (negate values)
        self.hi = []  # min-heap

    def add_num(self, num):
        heapq.heappush(self.lo, -num)
        heapq.heappush(self.hi, -heapq.heappop(self.lo))
        if len(self.hi) > len(self.lo):
            heapq.heappush(self.lo, -heapq.heappop(self.hi))

    def find_median(self):
        if len(self.lo) > len(self.hi):
            return -self.lo[0]
        return (-self.lo[0] + self.hi[0]) / 2

# Task Scheduler (greedy with max-heap)
def least_interval(tasks, n):
    from collections import Counter
    freq = list(Counter(tasks).values())
    max_freq = max(freq)
    max_count = freq.count(max_freq)
    return max(len(tasks), (max_freq - 1) * (n + 1) + max_count)
```

## Key Variations
- **Top-k**: Min-heap of size k (keeps the k largest)
- **Merge k sorted**: Heap of k elements, one from each list
- **Two heaps**: Find median — max-heap for lower half, min-heap for upper half
- **Lazy deletion**: Mark items as deleted, skip them on pop (useful when modifying priorities)
- **Greedy scheduling**: Process highest priority first

## Problems Solved
| Problem | Date | Result | Notes |
|---------|------|--------|-------|

## My Mistakes
- (none yet)
