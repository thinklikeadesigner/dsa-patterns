# Stack [Google + Meta]

## When to Use
When you need **LIFO (Last In First Out)** behavior. Key signals: "reverse", "matching pairs" (parentheses, brackets), "most recent", "undo", "backtrack", or when processing elements where **order matters** and you need to come back to previous elements.

## Core Idea
A stack is a linear data structure where you can only add/remove from one end (the "top"). Operations are O(1):
- `push(x)` - add to top
- `pop()` - remove from top
- `peek()` - look at top without removing

The key property: **last thing you put in is the first thing you take out** (LIFO).

## Template Code

### Basic Stack Operations

```python
# Python lists work as stacks
stack = []

# Push
stack.append(x)

# Pop
top = stack.pop()

# Peek
top = stack[-1]  # Don't remove

# Check if empty
if stack:
    # has elements
if not stack:
    # empty
```

---

## Common Patterns

### Pattern 1: Reversal

**Use stack's LIFO property to reverse a sequence.**

```python
# Reverse entire string
def reverse_string(s):
    stack = []
    for char in s:
        stack.append(char)

    result = []
    while stack:
        result.append(stack.pop())

    return ''.join(result)

# Reverse specific characters
def reverse_some_chars(s, chars):
    stack = []

    # Collect target characters in order
    for char in s:
        if char in chars:
            stack.append(char)

    # Rebuild string, popping from stack for targets
    result = []
    for char in s:
        if char in chars:
            result.append(stack.pop())  # LIFO = reversed!
        else:
            result.append(char)

    return ''.join(result)

# Example:
# s = "abcabc", chars = ["a", "b"]
# Stack collects: ["a", "b", "a", "b"]
# Rebuild pops: "b", "a", "b", "a" (reversed!)
# Result: "bacbac"
```

---

### Pattern 2: Matching Pairs (Parentheses)

**Use stack to track opening brackets, pop when you see closing.**

```python
def valid_parentheses(s):
    stack = []
    pairs = {'(': ')', '[': ']', '{': '}'}

    for char in s:
        if char in pairs:  # Opening bracket
            stack.append(char)
        else:  # Closing bracket
            if not stack or pairs[stack.pop()] != char:
                return False

    return len(stack) == 0  # All opened brackets closed?

# Example:
# "({[]})" → True
# "({[}])" → False (wrong order)
# "((("     → False (not closed)
```

---

### Pattern 3: Backtracking / Undo

**Stack stores history, pop to undo.**

```python
# Text editor with undo
class TextEditor:
    def __init__(self):
        self.text = ""
        self.history = []  # Stack of previous states

    def type(self, char):
        self.history.append(self.text)  # Save state
        self.text += char

    def undo(self):
        if self.history:
            self.text = self.history.pop()

# Path backtracking in maze
def explore_maze(position, stack):
    stack.append(position)  # Save where we are

    if is_dead_end(position):
        stack.pop()  # Backtrack
        return

    # Try next moves...
```

---

### Pattern 4: Expression Evaluation

**Use stack to evaluate postfix notation or parse expressions.**

```python
# Evaluate Reverse Polish Notation (postfix)
def eval_rpn(tokens):
    stack = []

    for token in tokens:
        if token in ['+', '-', '*', '/']:
            b = stack.pop()
            a = stack.pop()
            if token == '+':
                stack.append(a + b)
            elif token == '-':
                stack.append(a - b)
            elif token == '*':
                stack.append(a * b)
            else:
                stack.append(int(a / b))
        else:
            stack.append(int(token))

    return stack[0]

# Example:
# ["2", "1", "+", "3", "*"] → (2 + 1) * 3 = 9
```

---

### Pattern 5: Next Greater Element

**Use stack to find next greater element for each item (monotonic stack variant).**

```python
def next_greater_element(nums):
    result = [-1] * len(nums)
    stack = []  # Store indices

    for i, num in enumerate(nums):
        while stack and nums[stack[-1]] < num:
            idx = stack.pop()
            result[idx] = num
        stack.append(i)

    return result

# Example:
# [2, 1, 3, 4] → [3, 3, 4, -1]
```

---

## Key Insights

### 1. Build Result with a List, Not String Concatenation

```python
# ❌ WRONG: String concatenation is O(n) per operation
result = ""
for char in stack:
    result += stack.pop()  # O(n²) total!

# ✅ CORRECT: List append is O(1), join is O(n) once
result = []
while stack:
    result.append(stack.pop())  # O(n) total
return ''.join(result)
```

---

### 2. Don't Modify While Iterating

```python
# ❌ WRONG: Modifying s while iterating over it
for i, char in enumerate(s):
    if condition:
        s = s[:i] + replacement + s[i+1:]  # Breaks iteration!

# ✅ CORRECT: Build new result separately
result = []
for char in s:
    if condition:
        result.append(replacement)
    else:
        result.append(char)
return ''.join(result)
```

---

### 3. enumerate() Returns (index, value)

```python
# ❌ WRONG: Backwards parameter order
for value, idx in enumerate(s):
    print(s[value])  # value is actually the index!

# ✅ CORRECT: (index, value) order
for idx, value in enumerate(s):
    print(value)

# ✅ BETTER: Often you don't need the index
for char in s:
    print(char)
```

---

## Time & Space Complexity

| Operation | Time | Space |
|-----------|------|-------|
| Push | O(1) | O(1) per element |
| Pop | O(1) | - |
| Peek | O(1) | - |
| Process n items | O(n) | O(n) for stack |

**Total for reversal pattern:** O(n) time, O(n) space

---

## When NOT to Use a Stack

- If you need **random access** to elements → use array/list
- If you need **FIFO** behavior → use queue (deque)
- If you need **min/max in O(1)** → use heap
- If you're just reversing → Python's `[::-1]` is simpler

---

## Problems Solved

| Problem | Date | Result | Notes |
|---------|------|--------|-------|
| Reverse Some Chars | 2026-02-11 | Struggled | 2 bugs: enumerate() order wrong, modified string during iteration. Solved in 4 min but had implementation bugs. |
| Paired Parentheses | 2026-02-11 | Failed | 3 bugs: swapped open/closed variable assignments, didn't check for negative count, used if/if instead of if/elif. |

---

## My Mistakes

- **2026-02-11 (Reverse Some Chars)**: Used `for value, idx in enumerate(s)` instead of `for idx, value in enumerate(s)`. Remember: enumerate returns **(index, value)** not (value, index).
- **2026-02-11 (Reverse Some Chars)**: Modified string during iteration with string slicing: `s = s[:i] + new + s[i+1:]`. This is O(n) per operation and breaks iteration. Use a result list instead.
- **2026-02-11 (Paired Parentheses)**: Swapped variable names — assigned `open = ")"` and `closed = "("`. Always double-check variable assignments match their names.
- **2026-02-11 (Paired Parentheses)**: Only checked if count equals zero at the end, but didn't check if count ever goes **negative** during iteration. Need: `if count < 0: return False` inside the loop to catch invalid orderings like `")("`.
- **2026-02-11 (Paired Parentheses)**: The counter technique only works for single bracket type. For multiple types `()[]{}`, you need a full stack to track which opening bracket to match.
