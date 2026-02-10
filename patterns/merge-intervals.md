# Merge Intervals [Meta Heavy]

## When to Use
When dealing with **intervals** (start, end) and you need to merge overlapping ones, find gaps, insert a new interval, or check for conflicts. Key signal: any problem involving ranges, schedules, or time slots. Classic Meta interview question.

## Core Idea
Sort intervals by start time. Then scan left to right — if the current interval overlaps with the previous, merge them (extend the end). Otherwise, start a new group. Sorting is the key step: O(n log n).

## Template Code

```python
# Merge overlapping intervals
def merge(intervals):
    intervals.sort(key=lambda x: x[0])
    merged = [intervals[0]]

    for start, end in intervals[1:]:
        if start <= merged[-1][1]:  # overlapping
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])

    return merged

# Insert interval into sorted non-overlapping list
def insert(intervals, new):
    result = []
    i = 0

    # Add all intervals that end before new starts
    while i < len(intervals) and intervals[i][1] < new[0]:
        result.append(intervals[i])
        i += 1

    # Merge all overlapping intervals with new
    while i < len(intervals) and intervals[i][0] <= new[1]:
        new[0] = min(new[0], intervals[i][0])
        new[1] = max(new[1], intervals[i][1])
        i += 1
    result.append(new)

    # Add remaining
    result.extend(intervals[i:])
    return result

# Meeting rooms — can attend all? (no overlap)
def can_attend(intervals):
    intervals.sort()
    for i in range(1, len(intervals)):
        if intervals[i][0] < intervals[i - 1][1]:
            return False
    return True

# Meeting rooms II — minimum rooms needed
def min_meeting_rooms(intervals):
    import heapq
    intervals.sort()
    heap = []  # end times of current meetings
    for start, end in intervals:
        if heap and heap[0] <= start:
            heapq.heappop(heap)  # reuse room
        heapq.heappush(heap, end)
    return len(heap)
```

## Key Variations
- **Merge**: Combine overlapping intervals
- **Insert**: Insert into sorted list and merge
- **Meeting rooms**: Check overlap (I) or count max overlap (II)
- **Interval intersection**: Two pointer through two sorted lists
- **Employee free time**: Merge all busy intervals, find gaps

## Problems Solved
| Problem | Date | Result | Notes |
|---------|------|--------|-------|

## My Mistakes
- (none yet)
