# Decompress Braces (LC 394 Decode String)

**Problem:** Given `"3{a2{b}}"`, return `"abbbabbb"`

**Difficulty:** Medium-Hard (nested structures + stack state management)

---

## Why This Is Hard

1. **Nested structures** — braces inside braces
2. **Two pieces of state** — need to track BOTH string and number
3. **Non-obvious when to save/restore** — when do you push? when do you pop?

---

## The Core Insight

When you encounter nested braces, you need to **pause** what you're building, handle the inner part, then **resume** where you left off.

```
"3{a2{b}}"
     ^
     └─ When you hit this '{', you need to remember:
        - The "a" you were building
        - The "2" that tells you how many times to repeat what comes next
```

**Stack lets you save and restore this state.**

---

## The Algorithm (Step by Step)

### State Variables

```python
stack = []          # Stores (prev_string, repeat_count) pairs
current_string = "" # What you're building right now
current_num = 0     # The number before the current '{'
```

### For Each Character

| Character | Action |
|-----------|--------|
| **Digit** | Build up `current_num` (might be multi-digit like "12") |
| **`{`** | Push `(current_string, current_num)` to stack, reset both |
| **`}`** | Pop stack, multiply `current_string` by popped number, append to popped string |
| **Letter** | Append to `current_string` |

---

## Walkthrough: `"3{a2{b}}"`

### Initial State
```python
stack = []
current_string = ""
current_num = 0
```

### Step 1: Read `'3'` (digit)
```python
current_num = 3
```

### Step 2: Read `'{'` (opening brace)
```python
# Save current state
stack.push(("", 3))  # prev_string="", repeat_count=3

# Reset for what's inside the braces
current_string = ""
current_num = 0
```

**Stack:** `[("", 3)]`

### Step 3: Read `'a'` (letter)
```python
current_string = "a"
```

### Step 4: Read `'2'` (digit)
```python
current_num = 2
```

### Step 5: Read `'{'` (opening brace)
```python
# Save current state
stack.push(("a", 2))  # prev_string="a", repeat_count=2

# Reset
current_string = ""
current_num = 0
```

**Stack:** `[("", 3), ("a", 2)]`

### Step 6: Read `'b'` (letter)
```python
current_string = "b"
```

### Step 7: Read `'}'` (closing brace)
```python
# Pop: prev_string="a", repeat_count=2
prev_string, repeat_count = stack.pop()

# Multiply current_string by repeat_count
current_string = "b" * 2  # "bb"

# Append to what came before
current_string = "a" + "bb"  # "abb"
```

**Stack:** `[("", 3)]`

### Step 8: Read `'}'` (closing brace)
```python
# Pop: prev_string="", repeat_count=3
prev_string, repeat_count = stack.pop()

# Multiply current_string by repeat_count
current_string = "abb" * 3  # "abbabbabb"

# Append to what came before
current_string = "" + "abbabbabb"  # "abbabbabb"
```

**Stack:** `[]`

### Result: `"abbabbabb"` ✓

---

## The Template Code

```python
def decompress_braces(s):
    stack = []
    current_string = ""
    current_num = 0

    for char in s:
        if char.isdigit():
            # Build up number (could be multi-digit)
            current_num = current_num * 10 + int(char)

        elif char == '{':
            # Save state and reset
            stack.append((current_string, current_num))
            current_string = ""
            current_num = 0

        elif char == '}':
            # Pop and reconstruct
            prev_string, repeat_count = stack.pop()
            current_string = prev_string + (current_string * repeat_count)

        else:  # Letter
            current_string += char

    return current_string
```

---

## Key Patterns to Remember

### 1. Stack Stores BOTH Pieces of State

```python
stack.append((current_string, current_num))
#             ^^^^^^^^^^^^^^^  ^^^^^^^^^^^
#             what you built   how many times to repeat next part
```

### 2. Opening Brace = "Save and Reset"

```python
if char == '{':
    stack.append((current_string, current_num))  # Save
    current_string = ""                          # Reset
    current_num = 0
```

### 3. Closing Brace = "Pop, Multiply, Append"

```python
if char == '}':
    prev_string, repeat_count = stack.pop()          # Pop
    current_string = current_string * repeat_count   # Multiply
    current_string = prev_string + current_string    # Append
```

---

## Visual Model: Stack as "Pause Points"

```
"3{a2{b}}"

    Start
      ↓
    '3' → current_num = 3
      ↓
    '{' → PAUSE! Push ("", 3) to stack
      ↓         Start fresh inside
    'a' → current_string = "a"
      ↓
    '2' → current_num = 2
      ↓
    '{' → PAUSE AGAIN! Push ("a", 2) to stack
      ↓         Start fresh inside inner braces
    'b' → current_string = "b"
      ↓
    '}' → RESUME! Pop ("a", 2)
          current_string = "a" + ("b" * 2) = "abb"
      ↓
    '}' → RESUME! Pop ("", 3)
          current_string = "" + ("abb" * 3) = "abbabbabb"
```

---

## Common Edge Cases

### Adjacent Groups
```python
"2{a}3{b}"
# Result: "aabbb"
# After first '}', current_string="aa", stack is empty
# Continue building with '3' and '{b}'
```

### Letters Outside Braces
```python
"x2{a}y"
# Result: "xaay"
# 'x' gets added to current_string before any braces
```

### Multi-digit Numbers
```python
"12{a}"
# Result: "aaaaaaaaaaaa" (12 a's)
# current_num = 1*10 + 2 = 12
```

---

## Why You Need to Watch It First

This problem requires understanding:
1. **State management** (what to save, when to save it)
2. **Stack restoration** (how popping rebuilds the string)
3. **Multi-digit number handling** (building up `current_num`)

These patterns aren't obvious — seeing the walkthrough once plants the seed. Next time you'll recognize "nested structure with state = stack of tuples".

---

## Review Strategy

When you review this problem later:
1. **Don't look at the code** — try to explain the algorithm in words
2. **Draw the stack state** for `"3{a2{b}}"` at each step
3. **Code it from memory** using the template structure
4. **Test with nested + adjacent** cases

The pattern will stick after 2-3 reviews.
