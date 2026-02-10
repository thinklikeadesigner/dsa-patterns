# BFS — Breadth-First Search [Google + Meta]

## When to Use
When you need **shortest path in an unweighted graph/grid**, **level-order traversal** of a tree, or when you need to explore all nodes at distance k before distance k+1. Key signal: "minimum number of steps/moves" or "nearest" in an unweighted context.

## Core Idea
Use a queue (FIFO). Process all nodes at the current level before moving to the next. This guarantees the first time you reach a node is via the shortest path (in unweighted graphs). O(V + E) time.

## Template Code

```python
from collections import deque

# BFS on a grid (shortest path)
def bfs_grid(grid, start, end):
    rows, cols = len(grid), len(grid[0])
    queue = deque([(start[0], start[1], 0)])  # row, col, distance
    visited = {(start[0], start[1])}

    while queue:
        r, c, dist = queue.popleft()
        if (r, c) == end:
            return dist

        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) not in visited and grid[nr][nc] != 1:
                visited.add((nr, nc))
                queue.append((nr, nc, dist + 1))

    return -1  # unreachable

# BFS level-order traversal (tree)
def level_order(root):
    if not root:
        return []
    result = []
    queue = deque([root])
    while queue:
        level = []
        for _ in range(len(queue)):
            node = queue.popleft()
            level.append(node.val)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        result.append(level)
    return result

# Multi-source BFS (e.g., rotting oranges)
def multi_source_bfs(grid, sources):
    rows, cols = len(grid), len(grid[0])
    queue = deque()
    visited = set()
    for r, c in sources:
        queue.append((r, c, 0))
        visited.add((r, c))

    max_dist = 0
    while queue:
        r, c, dist = queue.popleft()
        max_dist = max(max_dist, dist)

        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) not in visited and grid[nr][nc] != 1:
                visited.add((nr, nc))
                queue.append((nr, nc, dist + 1))

    return max_dist
```

## Key Variations
- **Grid shortest path**: Walls and gates, shortest path in maze
- **Level-order tree**: Zigzag traversal, right side view
- **Multi-source BFS**: Rotting oranges, 01-matrix (start from all sources simultaneously)
- **BFS with state**: Open the lock (state = combination string)

## Problems Solved
| Problem | Date | Result | Notes |
|---------|------|--------|-------|

## My Mistakes
- (none yet)
