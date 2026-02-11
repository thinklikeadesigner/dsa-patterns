# DFS — Depth-First Search [Google + Meta]

## When to Use
When you need to **explore all paths**, find **connected components**, detect **cycles**, or solve problems that require exhaustive traversal. Key signal: "find all", "connected components", "is there a path", or any tree/graph problem where you process subtrees recursively.

## Core Idea
Go as deep as possible before backtracking. Use recursion (implicit stack) or an explicit stack. O(V + E) time. DFS is the natural choice for trees (pre/in/post-order) and for graph problems where you need to explore all reachable nodes.

## Template Code

```python
# DFS on graph (iterative)
def dfs_graph(graph, start):
    visited = set()
    stack = [start]
    while stack:
        node = stack.pop()
        if node in visited:
            continue
        visited.add(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                stack.append(neighbor)
    return visited

# DFS on graph (recursive) — connected components
def count_components(n, edges):
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    visited = set()
    count = 0

    def dfs(node):
        visited.add(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                dfs(neighbor)

    for i in range(n):
        if i not in visited:
            dfs(i)
            count += 1
    return count

# DFS on grid (flood fill / island counting)
def num_islands(grid):
    rows, cols = len(grid), len(grid[0])
    count = 0

    def dfs(r, c):
        if r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] == '0':
            return
        grid[r][c] = '0'  # mark visited
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            dfs(r + dr, c + dc)

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1':
                dfs(r, c)
                count += 1
    return count

# Cycle detection in directed graph
def has_cycle(graph, n):
    WHITE, GRAY, BLACK = 0, 1, 2
    color = [WHITE] * n

    def dfs(node):
        color[node] = GRAY
        for neighbor in graph[node]:
            if color[neighbor] == GRAY:
                return True  # back edge = cycle
            if color[neighbor] == WHITE and dfs(neighbor):
                return True
        color[node] = BLACK
        return False

    return any(color[i] == WHITE and dfs(i) for i in range(n))
```

## Key Variations
- **Grid DFS**: Number of islands, flood fill, surrounded regions
- **Graph DFS**: Connected components, cycle detection, path existence
- **Tree DFS**: All root-to-leaf paths, max depth, diameter
- **DFS with state/coloring**: Cycle detection in directed graphs (white/gray/black)

## Key Takeaways
- **Counting edges vs nodes**: When counting **edges**, start at 0 and add 1 for each edge traversed. When counting **nodes**, start at 1.
- **Longest path with multiple branches**: Always use **max()** to find the longest branch, never sum all paths.
- **DAG optimization**: For DAGs (directed acyclic graphs), add **memoization** to avoid recalculating overlapping subproblems. No need for visited set since there are no cycles.

## Problems Solved
| Problem | Date | Result | Notes |
|---------|------|--------|-------|
| Longest Path (DAG) | 2026-02-11 | Solved | DFS with memoization. Struggled with counting edges vs nodes (set count=1 initially instead of 0). Needed hint about using max() instead of sum for branches. |

## My Mistakes
- **2026-02-11**: Counted nodes instead of edges (initialized count=1 instead of 0 for base case)
- **2026-02-11**: Tried summing all neighbor paths instead of taking max of branches
