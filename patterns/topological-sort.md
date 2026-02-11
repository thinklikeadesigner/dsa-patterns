# Topological Sort [Google Heavy]

## When to Use
When you have **dependencies between tasks** and need to find a valid ordering, or detect if a valid ordering exists (cycle detection in directed graphs). Key signals: "course schedule", "build order", "prerequisites", "task scheduling".

## Core Idea
Given a DAG (directed acyclic graph), produce a linear ordering such that for every edge u→v, u comes before v. Two approaches: **Kahn's algorithm** (BFS with in-degrees) or **DFS post-order** (reverse finish order). If a cycle exists, topological sort is impossible.

## Template Code

```python
from collections import deque, defaultdict

# Kahn's Algorithm (BFS — preferred, easier to reason about)
def topo_sort_bfs(num_nodes, edges):
    graph = defaultdict(list)
    in_degree = [0] * num_nodes

    for u, v in edges:
        graph[u].append(v)
        in_degree[v] += 1

    queue = deque([i for i in range(num_nodes) if in_degree[i] == 0])
    order = []

    while queue:
        node = queue.popleft()
        order.append(node)
        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    if len(order) == num_nodes:
        return order  # valid topological order
    return []  # cycle detected

# Course Schedule (can you finish all courses?)
def can_finish(num_courses, prerequisites):
    return len(topo_sort_bfs(num_courses, prerequisites)) == num_courses

# Course Schedule II (return the order)
def find_order(num_courses, prerequisites):
    order = topo_sort_bfs(num_courses, prerequisites)
    return order if len(order) == num_courses else []

# DFS approach (alternative)
def topo_sort_dfs(num_nodes, edges):
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)

    WHITE, GRAY, BLACK = 0, 1, 2
    color = [WHITE] * num_nodes
    order = []

    def dfs(node):
        color[node] = GRAY
        for neighbor in graph[node]:
            if color[neighbor] == GRAY:
                return False  # cycle
            if color[neighbor] == WHITE:
                if not dfs(neighbor):
                    return False
        color[node] = BLACK
        order.append(node)
        return True

    for i in range(num_nodes):
        if color[i] == WHITE:
            if not dfs(i):
                return []  # cycle

    return order[::-1]  # reverse post-order
```

## Key Variations
- **Cycle detection**: If topo sort produces fewer nodes than total → cycle exists
- **All valid orderings**: Backtracking on Kahn's (pick any node with in-degree 0)
- **Parallel scheduling**: In Kahn's, all nodes in the queue at the same time can run in parallel (same "level")

## Problems Solved
| Problem | Date | Result | Notes |
|---------|------|--------|-------|
| Semesters Required | 2026-02-11 | Solved | Kahn's algorithm with level-order BFS. Struggled with understanding indegrees concept, building directed graph, and processing queue level-by-level. |

## My Mistakes
- **2026-02-11**: Initially built undirected graph (bidirectional edges) instead of directed
- **2026-02-11**: Didn't understand what indegree means (number of incoming edges = prerequisites count)
- **2026-02-11**: Had indentation issues - placed while loop and return inside the for loop
