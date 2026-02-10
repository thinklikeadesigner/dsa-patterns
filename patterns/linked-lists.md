# Linked Lists [Meta Heavy]

## When to Use
When the problem explicitly involves a linked list. Key signals: "reverse a linked list", "detect cycle", "merge two sorted lists", "remove nth from end", "reorder list". Meta loves linked list problems — they test pointer manipulation and edge case handling.

## Core Idea
Use pointer manipulation. Common techniques: **dummy node** (simplifies head edge cases), **slow/fast pointers** (find middle, detect cycle), **reverse in-place** (three pointer technique). Always handle: empty list, single node, even/odd length.

## Template Code

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

# Reverse linked list (iterative)
def reverse(head):
    prev = None
    curr = head
    while curr:
        nxt = curr.next
        curr.next = prev
        prev = curr
        curr = nxt
    return prev

# Detect cycle (Floyd's)
def has_cycle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            return True
    return False

# Find cycle start
def detect_cycle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            slow = head
            while slow != fast:
                slow = slow.next
                fast = fast.next
            return slow
    return None

# Find middle (slow/fast)
def find_middle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    return slow

# Merge two sorted lists
def merge(l1, l2):
    dummy = curr = ListNode(0)
    while l1 and l2:
        if l1.val <= l2.val:
            curr.next = l1
            l1 = l1.next
        else:
            curr.next = l2
            l2 = l2.next
        curr = curr.next
    curr.next = l1 or l2
    return dummy.next

# Remove Nth from end (two pointers with gap of n)
def remove_nth(head, n):
    dummy = ListNode(0, head)
    fast = slow = dummy
    for _ in range(n + 1):
        fast = fast.next
    while fast:
        fast = fast.next
        slow = slow.next
    slow.next = slow.next.next
    return dummy.next

# Reorder List: L0→Ln→L1→Ln-1→...
def reorder(head):
    # Find middle
    slow = fast = head
    while fast.next and fast.next.next:
        slow = slow.next
        fast = fast.next.next

    # Reverse second half
    second = reverse(slow.next)
    slow.next = None

    # Interleave
    first = head
    while second:
        tmp1, tmp2 = first.next, second.next
        first.next = second
        second.next = tmp1
        first, second = tmp1, tmp2
```

## Key Patterns
- **Dummy node**: Use when the head might change (merge, remove, insert)
- **Slow/fast**: Find middle (fast moves 2x), detect cycle (Floyd's)
- **Reverse**: Three pointers (prev, curr, nxt) — also used for reversing sublists
- **Two pass or two pointer**: Remove nth from end, find intersection point

## Problems Solved
| Problem | Date | Result | Notes |
|---------|------|--------|-------|

## My Mistakes
- (none yet)
