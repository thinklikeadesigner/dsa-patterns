# ASCII Visual: The Recursive Exploration Pattern

## The Core Pattern

```
┌─────────────────────────────────────────────────────────────────┐
│  THE RECURSIVE EXPLORATION PATTERN                              │
│  "Try all options, keep the best/sum/count"                     │
└─────────────────────────────────────────────────────────────────┘

                    ┌───────────────┐
                    │   Function    │
                    │  (node/state) │
                    └───────┬───────┘
                            │
                    ┌───────▼────────┐
                    │  Base Case?    │
                    │  (memo check)  │
                    └───┬────────┬───┘
                     YES│        │NO
                ┌───────▼──┐     │
                │ Return   │     │
                │ cached   │     │
                └──────────┘     │
                                 │
                        ┌────────▼────────┐
                        │  accumulator =  │
                        │  initial_value  │
                        │                 │
                        │  (0, ∞, etc.)   │
                        └────────┬────────┘
                                 │
                    ┌────────────▼────────────┐
                    │   for option in opts:   │◄──┐
                    │                          │   │
                    │  ┌────────────────────┐ │   │
                    │  │ Recurse on option  │ │   │
                    │  │ value = f(option)  │ │   │
                    │  └──────────┬─────────┘ │   │
                    │             │            │   │
                    │  ┌──────────▼─────────┐ │   │
                    │  │ Combine results    │ │   │
                    │  │ acc = combine(acc, │ │   │
                    │  │         value)     │ │   │
                    │  └────────────────────┘ │   │
                    │                          │   │
                    └──────────┬───────────────┘   │
                               │                   │
                          More options? ───────────┘
                               │
                               │NO
                               │
                        ┌──────▼──────┐
                        │   Cache &   │
                        │   Return    │
                        │ accumulator │
                        └─────────────┘
```

---

## Visual Example: Max Path from Node 0

**Graph:**
```
  0 → 1 → 2
      ↓
      3
```

**Execution Tree:**

```
                    f(0)
                     │
                     ├─ acc = 0
                     │
         ┌───────────┼───────────┐
         │                       │
      f(1)                    f(3)
         │                       │
         ├─ acc = 0              ├─ acc = 0
         │                       │
    ┌────┼────┐              (no neighbors)
    │         │                  │
  f(2)      f(3)             return 0+1=1
    │         │
(no neigh) (no neigh)
    │         │
return 0+1=1  return 0+1=1
         │
         ├─ acc = max(0, 1, 1) = 1
         │
      return 1+1=2
                     │
                     ├─ acc = max(0, 2, 1) = 2
                     │
                  return 2+1=3  ✓
```

---

## The Combining Operations

Different problems use different ways to combine results:

```
┌──────────┬─────────────┬──────────────┬──────────────┐
│ Problem  │ Accumulator │   Combine    │    Result    │
├──────────┼─────────────┼──────────────┼──────────────┤
│ Max Path │   acc = 0   │ max(acc, x)  │   Longest    │
│ Min Cost │  acc = ∞    │ min(acc, x)  │   Shortest   │
│ Count    │   acc = 0   │   acc + x    │     Sum      │
│ Product  │   acc = 1   │   acc * x    │   Product    │
│ Any Path │ acc = False │  acc or x    │   Boolean    │
│ All Path │ acc = True  │  acc and x   │   Boolean    │
└──────────┴─────────────┴──────────────┴──────────────┘
```

---

## Code Skeleton with Visual Mapping

```python
def f(node, memo):
    # ┌─────────────────┐
    # │  Base Case      │
    # └─────────────────┘
    if node in memo:
        return memo[node]

    # ┌─────────────────┐
    # │  Initialize     │
    # └─────────────────┘
    acc = initial_value  # ← Box at top of loop

    # ┌─────────────────┐
    # │  Loop & Combine │ ◄──┐
    # └─────────────────┘    │
    for neighbor in graph[node]:  # │
        value = f(neighbor, memo)  # │ Repeat
        acc = combine(acc, value)  # │
    #                                │
    # ───────────────────────────────┘

    # ┌─────────────────┐
    # │  Store & Return │
    # └─────────────────┘
    memo[node] = finalize(acc)  # +1, or leave as-is
    return memo[node]
```

---

## Recursive Call Stack (Sideways Tree)

Showing how the recursion actually executes:

```
Start → f(0) ──┬─→ f(1) ──┬─→ f(2) → [leaf, return 1]
               │          │
               │          └─→ f(3) → [leaf, return 1]
               │
               └─→ f(3) → [memo hit, return 1]

Return Path (unwinding the stack):
[1] ← f(2)
[1] ← f(3)
      ↓
[2] ← f(1) = 1 + max(1,1)
[1] ← f(3)
      ↓
[3] ← f(0) = 1 + max(2,1)
```

---

## The Pattern at Two Levels

**This same structure appears twice in graph problems:**

### Outer Loop (Main Function)
```python
max_path = 0
for course in graph:                    # Try all starting nodes
    current_path = traverse(graph, course, memo)
    max_path = max(current_path, max_path)
```
**Meaning:** "What's the maximum across all possible starting points?"

### Inner Loop (Recursive Function)
```python
max_path = 0
for neighbor in graph[node]:            # Try all neighbors
    current_path = traverse(graph, neighbor, memo)
    max_path = max(current_path, max_path)
```
**Meaning:** "What's the maximum across all neighbors from this node?"

**Same pattern, different scope!**

---

## The Meta-Pattern

This is the fundamental structure of recursive exploration:

```python
# General form
accumulator = base_value  # 0 for max, inf for min, 0 for sum, etc.
for option in options:
    value = recursive_call(option)
    accumulator = combine(accumulator, value)  # max, min, +, etc.
return accumulator
```

**Every recursive DP problem follows this pattern:**
1. Initialize an accumulator
2. Try all options (loop)
3. Recursively solve each option
4. Combine the results
5. Return the final accumulator

---

## Real Examples

### Max Path (Longest Chain)
```python
max_length = 0  # Start with smallest
for neighbor in graph[node]:
    length = dfs(neighbor)
    max_length = max(max_length, length)  # Keep largest
return 1 + max_length
```

### Min Coins (Fewest Coins)
```python
min_coins = float('inf')  # Start with largest
for coin in coins:
    coins_needed = dfs(amount - coin)
    min_coins = min(min_coins, coins_needed)  # Keep smallest
return 1 + min_coins
```

### Count Paths (All Possible Ways)
```python
total = 0  # Start with nothing
for direction in [right, down]:
    paths = dfs(new_position)
    total += paths  # Add up all paths
return total
```

### Can Reach (Any Valid Path)
```python
possible = False  # Start assuming no
for neighbor in graph[node]:
    reachable = dfs(neighbor)
    possible = possible or reachable  # Any success = True
return possible
```

---

## Key Insight

**The loop pattern is the same everywhere:**
```
acc = initial
for option in options:
    val = recurse(option)
    acc = combine(acc, val)
return finalize(acc)
```

Only three things change:
1. **Initial value** (0, ∞, False, etc.)
2. **Combine operation** (max, min, +, or, etc.)
3. **Finalize** (+1, leave as-is, etc.)

The structure stays constant!
