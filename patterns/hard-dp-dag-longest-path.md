# Hard DP: DAG Longest Path (Graph + DP)

## When to Use
When you need to find the **longest path in a directed acyclic graph (DAG)**. Key signals: "minimum semesters", "longest dependency chain", "maximum depth", "critical path". This combines graph traversal (DFS) with dynamic programming (memoization).

## Core Idea
Use DFS with memoization to find the longest path from each node. The key insight: **leaf nodes (nodes with no outgoing edges) are the base case** — they're the deepest layer of the recursive call stack.

## Two Variants

### Variant 1: Count Edges (Path Length)
Returns the number of **edges** in the longest path.

```python
def longest_path(graph):
  memo = {}
  max_path = 0

  for node in graph:
    current_path = dfs(graph, node, memo)
    max_path = max(max_path, current_path)

  return max_path

def dfs(graph, node, memo):
  if node in memo:
    return memo[node]

  max_length = 0
  for neighbor in graph[node]:
    length = dfs(graph, neighbor, memo) + 1  # +1 for the edge
    max_length = max(length, max_length)

  memo[node] = max_length
  return memo[node]
```

**Key**: Add `+1` **inside the loop** when processing each neighbor (counting edges).

**Base case (implicit)**: Leaf nodes have no neighbors, loop doesn't run, `max_length = 0` (zero edges from a leaf).

---

### Variant 2: Count Nodes (Semesters Required)
Returns the number of **nodes** in the longest path.

```python
def semesters_required(num_courses, prereqs):
  graph = build_graph(num_courses, prereqs)
  memo = {}

  max_length = 0
  for node in graph:
    current_length = dfs(graph, node, memo)
    max_length = max(max_length, current_length)

  return max_length

def dfs(graph, node, memo):
  if node in memo:
    return memo[node]

  max_length = 0
  for neighbor in graph[node]:
    neighbor_length = dfs(graph, neighbor, memo)
    max_length = max(neighbor_length, max_length)

  # +1 for the node itself (after processing all neighbors)
  memo[node] = 1 + max_length
  return memo[node]

def build_graph(num_courses, prereqs):
  graph = {i: [] for i in range(num_courses)}
  for a, b in prereqs:
    graph[a].append(b)  # a unlocks b
  return graph
```

**Key**: Add `+1` **after the loop** when storing the result (counting nodes).

**Base case (implicit)**: Leaf nodes have no neighbors, loop doesn't run, `max_length = 0`, so result is `1 + 0 = 1` (the leaf node itself).

---

## Key Insights

### 1. Where You Add +1 Determines What You Count

| What to Count | Add +1 Where? | Leaf Node Value |
|---------------|---------------|-----------------|
| **Edges** | Inside loop: `dfs(neighbor) + 1` | 0 edges |
| **Nodes** | After loop: `1 + max_length` | 1 node |

---

### 2. Leaf Nodes Are the Base Case

Leaf nodes (no outgoing edges) are:
- The **deepest layer** of the recursive call stack
- The **base case** that stops recursion
- Handled **implicitly** when the neighbor loop doesn't run

**Call stack visualization:**
```
graph = {0: [1], 1: [2], 2: []}

dfs(0) calls dfs(1)
  dfs(1) calls dfs(2)
    dfs(2) has no neighbors → returns 1  ← Base case (deepest)
  dfs(1) returns 1 + 1 = 2
dfs(0) returns 1 + 2 = 3
```

---

### 3. Why Use max() Not sum()?

When a node has multiple neighbors, you take the **maximum** of their paths, not the sum.

**Why?** Because in problems like course scheduling, you can take multiple courses **in parallel**. You're limited by the **longest sequential chain**, not the sum of all chains.

Example:
```python
graph = {
  0: [1, 2],  # 0 unlocks both 1 and 2
  1: [3],     # Chain: 0→1→3 (3 nodes)
  2: [],      # Chain: 0→2 (2 nodes)
  3: []
}

# From node 0:
# - Path through 1: length 2 (nodes 1, 3)
# - Path through 2: length 1 (node 2)
# Result: 1 + max(2, 1) = 3  ← Take the LONGER path

# If we used sum: 1 + (2 + 1) = 4  ← WRONG!
```

In the scheduling interpretation:
- Semester 1: Take course 0
- Semester 2: Take courses 1 and 2 **in parallel**
- Semester 3: Take course 3 (after 1 is done)
- **Total: 3 semesters** (limited by the longest chain 0→1→3)

---

### 4. Graph Direction Matters

For "prerequisites" problems, the edge direction means:
- `(A, B)` means "A must come before B"
- Build graph as: `graph[A].append(B)` (A unlocks B)
- **NOT** bidirectional! Don't add `graph[B].append(A)`

---

### 5. Why Loop Through All Nodes?

```python
for node in graph:
    current_length = dfs(graph, node, memo)
    max_length = max(max_length, current_length)
```

**Why try every node as a starting point?**
- You don't know which node(s) are at the "top" of the dependency chain
- Some nodes might not be reachable from others (disconnected components)
- Memoization ensures each node is only calculated once, even if reached from multiple starting points

---

### 6. Edges vs Nodes Conversion

```
nodes = edges + 1
```

If you have a path with 2 edges, it contains 3 nodes.

Example: `0 → 1 → 2`
- 2 edges (arrows)
- 3 nodes (courses/semesters)

---

## Template: DAG Longest Path with DFS + Memo

```python
def longest_path(graph):
  memo = {}

  # Try all nodes as potential starting points
  result = [initial_value]  # 0 for max, inf for min, etc.
  for node in graph:
    value = dfs(graph, node, memo)
    result = update(result, value)  # max, min, sum, etc.

  return result

def dfs(graph, node, memo):
  # Memoization check
  if node in memo:
    return memo[node]

  # Process all neighbors
  accumulator = [initial_value]
  for neighbor in graph[node]:
    neighbor_value = dfs(graph, neighbor, memo)
    accumulator = combine(accumulator, neighbor_value)  # max, min, sum, etc.

  # Store and return result
  # Add +1 here for node counting, or add +1 in the loop for edge counting
  memo[node] = finalize(accumulator)
  return memo[node]
```

---

## Common Mistakes

### Mistake 1: Pre-initializing Leaf Nodes (Unnecessary)

```python
# ❌ Unnecessary complexity
for node in graph:
    if len(graph[node]) == 0:
        memo[node] = 1

# ✅ Let the algorithm handle it naturally
# Leaf nodes get max_length = 0 (empty loop), then 1 + 0 = 1
```

---

### Mistake 2: Using sum() Instead of max()

```python
# ❌ WRONG: Adds all paths together
total = 0
for neighbor in graph[node]:
    total += dfs(graph, neighbor, memo)

# ✅ CORRECT: Take the longest path
max_length = 0
for neighbor in graph[node]:
    max_length = max(max_length, dfs(graph, neighbor, memo))
```

---

### Mistake 3: Building Undirected Graph

```python
# ❌ WRONG: Creates bidirectional edges
for a, b in prereqs:
    graph[a].append(b)
    graph[b].append(a)  # Don't do this!

# ✅ CORRECT: Directed graph only
for a, b in prereqs:
    graph[a].append(b)
```

---

### Mistake 4: Not Initializing All Nodes

```python
# ❌ WRONG: Missing nodes that aren't in prereqs
graph = {}
for a, b in prereqs:
    if a not in graph:
        graph[a] = []
    graph[a].append(b)
# Node 3 might not exist if it's never mentioned!

# ✅ CORRECT: Initialize all nodes upfront
graph = {i: [] for i in range(num_courses)}
for a, b in prereqs:
    graph[a].append(b)
```

---

## Related Patterns

- **Topological Sort (Kahn's Algorithm)**: BFS-based alternative for finding levels/layers
- **DFS Cycle Detection**: Similar structure but tracks WHITE/GRAY/BLACK states
- **Tree DP**: Same memoized DFS pattern but on trees (no need to track visited since no cycles)

---

## Problems That Use This Pattern

- Semesters Required (count nodes in longest chain)
- Longest Path in DAG (count edges)
- Course Schedule III (with weights)
- Parallel Course scheduling
- Critical Path Method (project management)

---

## My Mistakes

- **2026-02-11**: Forgot the `+ 1` when counting nodes. Wrote `memo[node] = max_path` instead of `memo[node] = 1 + max_path`. This caused leaf nodes to return 0 instead of 1, and the entire calculation was off. **Remember: Add `+ 1` AFTER the loop to count nodes (the node itself). Add `+ 1` INSIDE the loop to count edges.**
