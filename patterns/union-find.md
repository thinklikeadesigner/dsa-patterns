# Union Find (Disjoint Set Union) [Meta Heavy]

## When to Use
When you need to **group elements into sets** and efficiently check if two elements are in the same set, or merge sets. Key signals: "connected components", "accounts merge", "redundant connection", "friend circles". Union Find is often simpler than DFS/BFS for dynamic connectivity.

## Core Idea
Maintain a forest where each tree is a set. Two operations: `find(x)` returns the root of x's tree, `union(x, y)` merges two trees. With **path compression** and **union by rank**, both operations are nearly O(1) amortized.

## Template Code

```python
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
        self.components = n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # path compression
        return self.parent[x]

    def union(self, x, y):
        px, py = self.find(x), self.find(y)
        if px == py:
            return False  # already connected
        # union by rank
        if self.rank[px] < self.rank[py]:
            px, py = py, px
        self.parent[py] = px
        if self.rank[px] == self.rank[py]:
            self.rank[px] += 1
        self.components -= 1
        return True

    def connected(self, x, y):
        return self.find(x) == self.find(y)

# Number of connected components
def count_components(n, edges):
    uf = UnionFind(n)
    for u, v in edges:
        uf.union(u, v)
    return uf.components

# Redundant connection (find the edge that creates a cycle)
def find_redundant(edges):
    uf = UnionFind(len(edges) + 1)
    for u, v in edges:
        if not uf.union(u, v):
            return [u, v]

# Accounts merge (group by connected email)
def accounts_merge(accounts):
    uf = UnionFind(len(accounts))
    email_to_id = {}
    for i, account in enumerate(accounts):
        for email in account[1:]:
            if email in email_to_id:
                uf.union(i, email_to_id[email])
            email_to_id[email] = i

    # Group emails by root account
    from collections import defaultdict
    groups = defaultdict(set)
    for email, idx in email_to_id.items():
        groups[uf.find(idx)].add(email)

    return [[accounts[root][0]] + sorted(emails)
            for root, emails in groups.items()]
```

## Key Variations
- **Basic connectivity**: Number of connected components, friend circles
- **Cycle detection**: Redundant connection — union returns False when already connected
- **Grouping by equivalence**: Accounts merge, similar string groups
- **With weights**: Track relative relationships (e.g., evaluate division)

## Problems Solved
| Problem | Date | Result | Notes |
|---------|------|--------|-------|

## My Mistakes
- (none yet)
