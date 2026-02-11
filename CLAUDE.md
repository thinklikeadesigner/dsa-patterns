# DSA Pattern Memory Bank — System Instructions

This directory is a spaced-repetition DSA review system. When the user opens Claude Code here, use these instructions to operate the system.

## How It Works

- **`tracker.csv`** holds spaced repetition state for each pattern
- **`patterns/*.md`** hold detailed notes, templates, and problem logs for each pattern
- **`problems.csv`** holds a master list of all problems attempted (one row per problem)
- **`problem_patterns.csv`** maps problems to patterns (many-to-many) with approach notes, complexity, and when to prefer each approach
- The user interacts conversationally; you read/write these files to manage the system

---

## Commands

### "What am I working on today?"

1. Read `tracker.csv` AND `problems.csv`.
2. Get today's date.
3. Categorize each **pattern** (from `tracker.csv`):
   - **Overdue**: `next_review < today`
   - **Due today**: `next_review == today`
   - **New**: `stability == 0` (never reviewed)
   - **Not due**: `next_review > today`
4. Categorize each **problem** (from `problems.csv`):
   - Same rules: overdue / due today / new (`stability == 0`) / not due
5. If the user has stated a target company (Google, Meta, or both), filter out irrelevant patterns using `company_relevance`:
   - Meta-only → skip patterns tagged `google` (e.g., DP, Trie, Dijkstra)
   - Google-only → skip patterns tagged `meta`
   - Both or unspecified → include everything
6. Prioritize: **overdue first** (oldest first) → **due today** → **new items**.
7. Output a focused plan of **2–3 items max**, mixing patterns and problems. For each item, show:
   - **[Pattern Review]** or **[Problem Review]** label
   - Item name
   - Why it's up (overdue by X days / due today / new)
   - A suggested action (write template from memory, explain approach from memory, etc.)
8. Ask: "Want to start with [first item]?"

### "Log a problem"

When the user says they solved (or attempted) a problem:

1. Identify **all patterns** it can be solved with (ask the user if not obvious).
2. Add a row to the **Problems Solved** table in the **primary** pattern's `.md` file:
   - Problem name/number, today's date, result (Solved/Struggled/Failed), notes from what the user said.
3. If the user mentions a mistake, add it to **My Mistakes** with today's date.
4. Ask for grade if not obvious: "How did that feel? Again (1) / Hard (2) / Good (3) / Easy (4)"
   - Or infer from what they said (e.g., "nailed it" → Easy, "struggled with edge cases" → Hard, "couldn't solve it" → Again)
5. Update `tracker.csv` for the primary pattern using the FSRS algorithm below.
6. Add or update the problem in `problems.csv` (one row — use the best result across attempts). Initialize FSRS state for new problems: `difficulty=5.0, stability=0, next_review=today, times_reviewed=0`. Then run FSRS with the grade to set the first real stability/next_review.
7. Add one row per pattern to `problem_patterns.csv` with:
   - `approach_notes`: how this pattern solves the problem
   - `time_complexity`: Big-O for this approach
   - `when_to_prefer`: when you'd choose this approach over the others

### "What patterns solve [problem]?"

1. Read `problem_patterns.csv` and filter by the given problem.
2. For each pattern match, show:
   - Pattern name
   - Approach notes
   - Time complexity
   - When to prefer this approach
3. Highlight trade-offs between approaches.

### "What problems use [pattern]?"

1. Read `problem_patterns.csv` and filter by the given pattern.
2. List all problems that can be solved with it, grouped by result (Solved/Struggled/Failed).
3. Show the `when_to_prefer` note for each — this reveals when this pattern is the right tool.

### "Show connections" or "Pattern overlap"

1. Read `problem_patterns.csv`.
2. Find problems that map to 2+ patterns.
3. Display them grouped by problem, showing all approaches side by side.
4. This is the "interview meta-skill" view — knowing multiple approaches and when each is better.

### "Add new pattern"

1. Ask for the pattern name and company relevance (google+meta, google, meta).
2. Create `patterns/<kebab-case-name>.md` using the template below.
3. Add a row to `tracker.csv` with:
   - `difficulty=5.0`, `stability=0`, `next_review=<today>`, `times_reviewed=0`

### "Review [pattern]" — Active Recall

1. Read the pattern's `.md` file but **only show** the pattern name and "When to Use" section.
2. Ask: **"Write the template code for this pattern from memory."**
3. Wait for the user's attempt.
4. **Then** show the saved Template Code side by side for comparison.
5. Ask: "How did that go? **Again (1) / Hard (2) / Good (3) / Easy (4)**"
6. Update `tracker.csv` using the FSRS algorithm below.

### "Review [problem]" — Active Recall

1. Show **only the problem name**.
2. Ask: **"What pattern(s) would you use? Walk through your approach."**
3. Wait for the user's explanation.
4. **Then** show the saved `approach_notes` and `time_complexity` from `problem_patterns.csv` for comparison.
5. Ask: "How did that go? **Again (1) / Hard (2) / Good (3) / Easy (4)**"
6. Update `problems.csv` using the FSRS algorithm below.

---

## FSRS Spaced Repetition Algorithm

When updating `tracker.csv` or `problems.csv` after a review.

### Grade Scale
```
1 = Again  (couldn't recall / completely forgot)
2 = Hard   (got it but struggled significantly)
3 = Good   (got it with reasonable effort)
4 = Easy   (nailed it, no hesitation)
```

### First Review (stability was 0 — new card):
```
stability = {1: 0.4, 2: 1.2, 3: 3.2, 4: 15.7}[grade]
difficulty = clamp(7.2 - 1.7 × (grade - 1), 1, 10)
```
Difficulty maps to: Again → 7.2, Hard → 5.5, Good → 3.8, Easy → 2.1

### Subsequent Reviews (stability > 0):
```
Step 1 — Retrievability (how likely you'd remember right now):
  days_elapsed = today - last_reviewed
  R = 0.9 ^ (days_elapsed / stability)

Step 2 — Update difficulty:
  D = clamp(D - 0.9 × (grade - 3), 1, 10)
  D = round(D × 0.9 + 5 × 0.1, 2)        // mean-revert toward 5

Step 3 — Update stability:
  If grade ≥ 2 (passed):
    SInc = 1 + 4.4 × ((11 - D) / 10) × S^(-0.11) × (e^(2.0 × (1 - R)) - 1)
    S_new = S × SInc
    If grade = 2 (Hard):  S_new = S_new × 0.8
    If grade = 4 (Easy):  S_new = S_new × 1.3
  If grade = 1 (Again):
    S_new = 0.9 × D^(-0.4) × ((S + 1)^0.1 - 1) × e^(2.3 × (1 - R))
    S_new = min(S_new, S)    // stability never increases on failure
```

### Always:
```
last_reviewed = today
next_review = today + max(1, round(S_new))
stability = S_new
times_reviewed += 1
```

### Key Differences from SM-2
- **Difficulty** and **stability** are tracked separately (SM-2 merged them into ease_factor)
- **Retrievability** accounts for how overdue a card is — reviewing an overdue card gives a bigger stability boost
- Intervals grow naturally from stability; no fixed progression

---

## tracker.csv Format

```csv
pattern,company_relevance,last_reviewed,next_review,difficulty,stability,times_reviewed
two-pointers,google+meta,,2026-02-08,5.0,0,0
```

- `pattern`: kebab-case, matches filename in `patterns/`
- `company_relevance`: `google+meta`, `google`, or `meta`
- `last_reviewed`: YYYY-MM-DD or empty if never reviewed
- `next_review`: YYYY-MM-DD (set to creation date for new patterns)
- `difficulty`: float [1, 10], starts at 5.0, represents inherent difficulty for the user
- `stability`: float (days), 0 = new/never reviewed, represents days until 90% recall probability
- `times_reviewed`: integer count

---

## problems.csv Format

```csv
problem,date_first_seen,best_result,difficulty,stability,last_reviewed,next_review,times_reviewed,notes
semesters-required,2026-02-11,Solved,5.0,0,,2026-02-11,0,"Kahn's algorithm with level-order BFS."
```

- `problem`: kebab-case unique identifier
- `date_first_seen`: YYYY-MM-DD when first attempted
- `best_result`: best outcome across all attempts (Solved > Struggled > Failed > Watched)
- `difficulty`: float [1, 10], starts at 5.0 (same as tracker.csv — FSRS state)
- `stability`: float (days), 0 = new/never reviewed
- `last_reviewed`: YYYY-MM-DD or empty if never reviewed as an SRS card
- `next_review`: YYYY-MM-DD (initialized to date_first_seen for new problems)
- `times_reviewed`: integer count of SRS reviews (not initial solve attempts)
- `notes`: brief summary of the problem and experience

## problem_patterns.csv Format

```csv
problem,pattern,approach_notes,time_complexity,when_to_prefer
semesters-required,topological-sort,Kahn's algorithm: BFS from zero-indegree nodes,O(V+E),When you need the number of levels/layers
semesters-required,dynamic-programming,DFS + memo: longest path from any start node,O(V+E),When thinking bottom-up from leaves
```

- `problem`: kebab-case, matches a row in `problems.csv`
- `pattern`: kebab-case, matches a row in `tracker.csv` and a file in `patterns/`
- `approach_notes`: how this pattern solves the problem
- `time_complexity`: Big-O for this specific approach
- `when_to_prefer`: when you'd choose this approach over alternatives

The many-to-many relationship is the key insight: one problem can map to multiple patterns, and one pattern solves many problems. The `when_to_prefer` column trains the meta-skill of knowing *which* approach to reach for.

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

## Git Workflow

After ANY change to files in this repository (tracker.csv, pattern files, CLAUDE.md, etc.):

1. Run `git add .`
2. Run `git commit -m "updated"`
3. Run `git push`

**CRITICAL**: This must happen after EVERY file modification. The user wants all changes automatically committed and pushed.

---

## User Workflow

When the user pastes in a problem or their code:

- **NEVER give the solution directly.**
- Only provide the **minimum viable hint** to get them unstuck.
- Focus on guiding their thinking, not solving it for them.
- Examples of good hints:
  - "What data structure would help you track X efficiently?"
  - "Consider what happens at the boundary when..."
  - "Your logic here handles case A, but what about case B?"
- Wait for them to try again before giving more hints.
