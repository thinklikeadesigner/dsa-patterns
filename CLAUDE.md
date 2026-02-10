# DSA Pattern Memory Bank — System Instructions

This directory is a spaced-repetition DSA review system. When the user opens Claude Code here, use these instructions to operate the system.

## How It Works

- **`tracker.csv`** holds spaced repetition state for each pattern
- **`patterns/*.md`** hold detailed notes, templates, and problem logs for each pattern
- The user interacts conversationally; you read/write these files to manage the system

---

## Commands

### "What am I working on today?"

1. Read `tracker.csv`.
2. Get today's date.
3. Categorize each pattern:
   - **Overdue**: `next_review < today`
   - **Due today**: `next_review == today`
   - **New**: `interval_days == 0` (never reviewed)
   - **Not due**: `next_review > today`
4. If the user has stated a target company (Google, Meta, or both), filter out irrelevant patterns using `company_relevance`:
   - Meta-only → skip patterns tagged `google` (e.g., DP, Trie, Dijkstra)
   - Google-only → skip patterns tagged `meta`
   - Both or unspecified → include everything
5. Prioritize: **overdue first** (oldest first) → **due today** → **new patterns**.
6. Output a focused plan of **2–3 items max**. For each item, show:
   - Pattern name
   - Why it's up (overdue by X days / due today / new)
   - A suggested action (review the template, solve a specific problem, etc.)
7. Ask: "Want to start with [first item]?"

### "Log a problem"

When the user says they solved (or attempted) a problem:

1. Identify which pattern it belongs to.
2. Add a row to the **Problems Solved** table in the pattern's `.md` file:
   - Problem name/number, today's date, result (Solved/Struggled/Failed), notes from what the user said.
3. If the user mentions a mistake, add it to **My Mistakes** with today's date.
4. Ask for confidence if not obvious: "How confident did you feel? (0-5)"
   - Or infer from what they said (e.g., "nailed it" → 5, "struggled with edge cases" → 3, "couldn't solve it" → 1)
5. Update `tracker.csv` using the SM-2 algorithm below.

### "Add new pattern"

1. Ask for the pattern name and company relevance (google+meta, google, meta).
2. Create `patterns/<kebab-case-name>.md` using the template below.
3. Add a row to `tracker.csv` with:
   - `interval_days=0`, `next_review=<today>`, `ease_factor=2.5`, `times_reviewed=0`, `streak=0`

### "Review [pattern]"

1. Read and display the pattern's `.md` file (When to Use, Core Idea, Template Code).
2. Quiz the user: "When would you use this pattern? Can you write the template from memory?"
3. Based on how they do, ask for confidence (0-5) and update `tracker.csv`.

---

## SM-2 Spaced Repetition Algorithm

When updating `tracker.csv` after a review:

### Confidence 4–5 (Got it):
```
interval_days = max(1, round(interval_days * ease_factor))
ease_factor = min(3.0, ease_factor + 0.1)
streak += 1
```
Special case: if `interval_days` was 0 (first review), set `interval_days = 1`.

### Confidence 2–3 (Struggled):
```
interval_days = max(1, round(interval_days * 0.5))
ease_factor = max(1.3, ease_factor - 0.15)
streak = 0
```

### Confidence 0–1 (Failed):
```
interval_days = 1
ease_factor = max(1.3, ease_factor - 0.3)
streak = 0
```

### Always:
```
last_reviewed = today
next_review = today + interval_days
times_reviewed += 1
```

Expected progression (at ease 2.5): 1 → 3 → 7 → 18 → 44 → 90+

---

## tracker.csv Format

```csv
pattern,company_relevance,last_reviewed,next_review,interval_days,ease_factor,times_reviewed,streak
two-pointers,google+meta,,2026-02-08,0,2.5,0,0
```

- `pattern`: kebab-case, matches filename in `patterns/`
- `company_relevance`: `google+meta`, `google`, or `meta`
- `last_reviewed`: YYYY-MM-DD or empty if never reviewed
- `next_review`: YYYY-MM-DD (set to creation date for new patterns)
- `interval_days`: integer, 0 = new/never reviewed
- `ease_factor`: float, starts at 2.5, clamped to [1.3, 3.0]
- `times_reviewed`: integer count
- `streak`: consecutive correct reviews

---

## Pattern File Template

```markdown
# Pattern Name

## When to Use
(1-2 sentences: the trigger/signal that says "use this pattern")

## Core Idea
(Brief explanation)

## Template Code
(Python skeleton)

## Problems Solved
| Problem | Date | Result | Notes |
|---------|------|--------|-------|

## My Mistakes
- (none yet)
```

---

## Important Notes

- Dates are always YYYY-MM-DD format.
- When reading tracker.csv, parse it carefully — it's a real CSV with headers.
- When writing tracker.csv, preserve the header row and all existing rows. Only modify the row being updated.
- Keep daily plans short and actionable. Don't overwhelm. 2–3 items max.
- Be encouraging but honest about progress.
