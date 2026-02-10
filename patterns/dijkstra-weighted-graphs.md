# Dijkstra / Weighted Graphs [Google Heavy]

## When to Use
When you need the **shortest path in a weighted graph** (with non-negative weights). Key signals: "shortest path with costs", "minimum cost to reach", "network delay time", "cheapest flights". If edges have weights and you need shortest distance, Dijkstra is the go-to.

## Core Idea
Greedy BFS using a min-heap. Always process the node with the smallest known distance first. When you pop a node, its distance is finalized. Relax neighbors: if going through current node gives a shorter path, update and push. O((V + E) log V) with a heap.

## Template Code

```python
import heapq
from collections import defaultdict

# Dijkstra's Algorithm
def dijkstra(graph, start, n):
    dist = [float('inf')] * n
    dist[start] = 0
    heap = [(0, start)]  # (distance, node)

    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:
            continue  # skip outdated entry
        for v, weight in graph[u]:
            if dist[u] + weight < dist[v]:
                dist[v] = dist[u] + weight
                heapq.heappush(heap, (dist[v], v))

    return dist

# Network Delay Time (shortest path from source to all, return max)
def network_delay(times, n, k):
    graph = defaultdict(list)
    for u, v, w in times:
        graph[u].append((v, w))

    dist = dijkstra(graph, k, n + 1)
    max_dist = max(dist[1:])
    return max_dist if max_dist < float('inf') else -1

# Cheapest Flights Within K Stops (modified Dijkstra / BFS)
def find_cheapest(n, flights, src, dst, k):
    graph = defaultdict(list)
    for u, v, w in flights:
        graph[u].append((v, w))

    # (cost, node, stops)
    heap = [(0, src, 0)]
    best = {}  # (node, stops) -> best cost

    while heap:
        cost, node, stops = heapq.heappop(heap)
        if node == dst:
            return cost
        if stops > k:
            continue
        if (node, stops) in best and best[(node, stops)] <= cost:
            continue
        best[(node, stops)] = cost

        for neighbor, weight in graph[node]:
            heapq.heappush(heap, (cost + weight, neighbor, stops + 1))

    return -1

# Shortest path with actual path reconstruction
def shortest_path(graph, start, end, n):
    dist = [float('inf')] * n
    prev = [-1] * n
    dist[start] = 0
    heap = [(0, start)]

    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:
            continue
        for v, weight in graph[u]:
            if dist[u] + weight < dist[v]:
                dist[v] = dist[u] + weight
                prev[v] = u
                heapq.heappush(heap, (dist[v], v))

    # Reconstruct path
    path = []
    node = end
    while node != -1:
        path.append(node)
        node = prev[node]
    return path[::-1] if dist[end] < float('inf') else []
```

## Key Variations
- **Standard Dijkstra**: Single-source shortest path
- **With constraints**: Cheapest flights within k stops — add constraints to state
- **Path reconstruction**: Track `prev[]` array
- **Multi-state**: When you need to track additional info (fuel, stops) — expand state in heap

## Important Notes
- Dijkstra does NOT work with negative edge weights (use Bellman-Ford instead)
- `if d > dist[u]: continue` is the key optimization — skip stale heap entries
- For unweighted graphs, use BFS instead (simpler and faster)

## Problems Solved
| Problem | Date | Result | Notes |
|---------|------|--------|-------|

## My Mistakes
- (none yet)
