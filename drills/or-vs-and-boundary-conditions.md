# Drill: `or` vs `and` in Boundary Conditions

**Target weakness**: Confusing `or` and `and` when checking if you've reached a goal state.

**Time**: 5 minutes before any DP/recursion problem

---

## The Rule

> **When checking if you've reached a SPECIFIC destination, use `and` to ensure ALL conditions are met.**
>
> **Use `or` only when ANY of several conditions means you should stop/return.**

---

## Quick Mental Model

```python
# DESTINATION (one specific place) → use AND
if r == target_row and c == target_col:
    return 1

# FAILURE (any of these is bad) → use OR
if r < 0 or c < 0 or r >= rows or c >= cols:
    return 0
```

**Mnemonic**:
- **AND** = "I need to be **ALL the way there**"
- **OR** = "**ANY** of these problems means I fail"

---

## Drill Questions

For each scenario, write the correct condition. Then check your answer.

### 1. Grid Path Counting
You're at `(r, c)` and need to reach bottom-right corner `(rows-1, cols-1)`. What's the base case for "I've arrived"?

<details>
<summary>Answer</summary>

```python
if r == len(grid) - 1 and c == len(grid[0]) - 1:
    return 1
```

**Why `and`?** You must be at the last row **AND** last column simultaneously. Being at just the last row or just the last column isn't the destination.

</details>

---

### 2. String Index (Word Break)
You're building a string from index `i`. What's the base case for "I've successfully built the entire string"?

<details>
<summary>Answer</summary>

```python
if i == len(s):
    return True
```

**Only one condition here** — no `or`/`and` needed. You've reached the end when the index equals the length.

</details>

---

### 3. Out of Bounds Check (Grid)
You're traversing a grid. What condition means "I've gone out of bounds"?

<details>
<summary>Answer</summary>

```python
rinbounds = 0 <= r < len(grid)
cinbounds = 0 <= c < len(grid[0])

if not rinbounds or not cinbounds:
    return 0  # or float('-inf'), or whatever failure value
```

**Why `or`?** **Any one** dimension being out of bounds means the cell is invalid. You don't need both to be out of bounds — just one is enough to fail.

**The pattern**: Check each dimension separately, then combine with `or` because ANY failure disqualifies the cell.

</details>

---

### 4. Two-Pointer Palindrome
You're checking if a string is a palindrome using pointers `i` (left) and `j` (right). What's the base case for "I've checked the whole string successfully"?

<details>
<summary>Answer</summary>

```python
if i >= j:
    return True  # we've met in the middle or crossed
```

**One condition** — when left pointer passes or meets right pointer, we're done.

</details>

---

### 5. Amount Remaining (Coin Change)
You're making change for `amount` using coins. What's the base case for "I've successfully made exact change"?

<details>
<summary>Answer</summary>

```python
if amount == 0:
    return 0  # or 1 for counting, or True for boolean
```

**One condition** — exact match means success.

</details>

---

### 6. Tricky: Grid Path with Obstacles
You're at `(r, c)` in a grid with obstacles marked 'X'. What's the condition for "this cell is invalid"?

<details>
<summary>Answer</summary>

```python
rinbounds = 0 <= r < len(grid)
cinbounds = 0 <= c < len(grid[0])

if not rinbounds or not cinbounds or grid[r][c] == 'X':
    return 0
```

**Why `or`?** **Any one** of these problems (out of bounds OR obstacle) makes this cell invalid. You don't need multiple problems — just one is enough to stop.

**Note**: You must check bounds BEFORE accessing `grid[r][c]`, otherwise you'll get an index error. Some people write it as one compound condition, but your style (separate variables) is clearer and safer.

</details>

---

### 7. The One That Got You: Max Path Sum Grid
You're finding the max sum path from `(0,0)` to `(rows-1, cols-1)` moving only right/down. What's the base case for reaching the destination?

<details>
<summary>Answer</summary>

```python
if r == len(grid) - 1 and c == len(grid[0]) - 1:
    return grid[r][c]  # you're at the destination, return its value
```

**Why `and`?** The destination is ONE specific cell — you must be at the last row **AND** the last column.

**Why not `or`?** If you used `or`, you'd return `grid[r][c]` for ANY cell on the last row or ANY cell on the last column — ignoring the remaining path to the actual corner.

</details>

---

### 8. Multiple Valid Endpoints
You're doing DFS in a graph looking for **any** exit node. Exit nodes are marked `exit[node] == True`. What's the base case?

<details>
<summary>Answer</summary>

```python
if exit[node]:
    return True
```

**One condition** — any exit works. No `and` needed because there's not a compound condition. If there were multiple properties an exit needs:

```python
if exit[node] and unlocked[node]:  # both required
    return True
```

</details>

---

## The Pattern You Keep Hitting

```python
# ❌ WRONG (your recurring bug)
if r == last_row or c == last_col:
    return 1

# This returns 1 for:
# - (last_row, 5) ← not the destination!
# - (3, last_col) ← not the destination!
# - (last_row, last_col) ← this is the only right one

# ✅ CORRECT
if r == last_row and c == last_col:
    return 1

# This ONLY returns 1 for the actual destination
```

---

## Quick Reference Card

**Print this and keep it next to your keyboard:**

```
┌─────────────────────────────────────────────┐
│  Reaching ONE SPECIFIC place:   use AND    │
│  ANY of several failures:       use OR     │
└─────────────────────────────────────────────┘

Examples:
  Destination:     r == goal_r and c == goal_c
  Out of bounds:   r < 0 or c < 0 or r >= rows or c >= cols
  Invalid state:   amount < 0 or grid[r][c] == 'X'
```

---

## Before You Code Any Base Case

Ask yourself:
1. **"Am I checking for ONE specific destination?"** → Use `and` to ensure ALL coordinates match
2. **"Am I checking if ANY of several problems occurred?"** → Use `or` because one problem is enough to fail

---

## Commit This to Memory

Run this drill **right before** you start any DP or recursion problem. Read the rule out loud:

> "Destination needs AND. Failure needs OR."

Then code your base cases.
