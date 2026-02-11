#!/usr/bin/env python3
"""
Interactive drill for `or` vs `and` in boundary conditions.
Run this before any DP/recursion problem to reinforce the pattern.
"""

import sys

# ANSI color codes
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
BOLD = '\033[1m'
RESET = '\033[0m'

def print_header(text):
    print(f"\n{BOLD}{BLUE}{'='*70}{RESET}")
    print(f"{BOLD}{BLUE}{text}{RESET}")
    print(f"{BOLD}{BLUE}{'='*70}{RESET}\n")

def print_rule():
    print(f"{BOLD}The Rule:{RESET}")
    print(f"  • {GREEN}Destination (ONE specific place){RESET} → use {BOLD}AND{RESET}")
    print(f"  • {RED}Failure (ANY problem){RESET} → use {BOLD}OR{RESET}")
    print()

def check_answer(user_input, correct_keywords, question_num):
    """Check if user's answer contains the key concepts."""
    user_lower = user_input.lower().strip()

    # Normalize the input
    has_and = ' and ' in user_lower or user_lower.startswith('and ') or user_lower.endswith(' and')
    has_or = ' or ' in user_lower or user_lower.startswith('or ') or user_lower.endswith(' or')

    # Check for required keywords
    required_present = all(keyword.lower() in user_lower for keyword in correct_keywords['required'])

    # Determine correctness based on question
    if correct_keywords['operator'] == 'and':
        is_correct = has_and and not has_or and required_present
    elif correct_keywords['operator'] == 'or':
        is_correct = has_or and required_present
    else:  # single condition
        is_correct = required_present and not has_and and not has_or

    return is_correct

questions = [
    {
        'num': 1,
        'title': 'Grid Path Counting',
        'prompt': 'You\'re at (r, c) and need to reach bottom-right corner (rows-1, cols-1).\nWhat\'s the base case for "I\'ve arrived"?\n\nWrite the condition (the part after "if"): ',
        'answer': 'if r == len(grid) - 1 and c == len(grid[0]) - 1:\n    return 1',
        'explanation': f'{BOLD}Why `and`?{RESET} You must be at the last row {BOLD}AND{RESET} last column simultaneously.\nBeing at just the last row or just the last column isn\'t the destination.',
        'keywords': {'operator': 'and', 'required': ['r', 'len(grid)', 'c', 'len(grid[0])']}
    },
    {
        'num': 2,
        'title': 'String Index (Word Break)',
        'prompt': 'You\'re building a string from index i.\nWhat\'s the base case for "I\'ve successfully built the entire string"?\n\nWrite the condition: ',
        'answer': 'if i == len(s):\n    return True',
        'explanation': f'{BOLD}Only one condition here{RESET} — no `or`/`and` needed.\nYou\'ve reached the end when the index equals the length.',
        'keywords': {'operator': 'single', 'required': ['i', 'len(s)']}
    },
    {
        'num': 3,
        'title': 'Out of Bounds Check (Grid)',
        'prompt': 'You\'re traversing a grid.\nWhat condition means "I\'ve gone out of bounds"?\n\nWrite the full bounds check (including the variable assignments): ',
        'answer': 'rinbounds = 0 <= r < len(grid)\ncinbounds = 0 <= c < len(grid[0])\n\nif not rinbounds or not cinbounds:\n    return 0',
        'explanation': f'{BOLD}Why `or`?{RESET} {BOLD}Any one{RESET} dimension being out of bounds means the cell is invalid.\nYou don\'t need both to be out of bounds — just one is enough to fail.',
        'keywords': {'operator': 'or', 'required': ['rinbounds', 'cinbounds', 'not']}
    },
    {
        'num': 4,
        'title': 'Two-Pointer Palindrome',
        'prompt': 'You\'re checking if a string is a palindrome using pointers i (left) and j (right).\nWhat\'s the base case for "I\'ve checked the whole string successfully"?\n\nWrite the condition: ',
        'answer': 'if i >= j:\n    return True',
        'explanation': f'{BOLD}One condition{RESET} — when left pointer passes or meets right pointer, we\'re done.',
        'keywords': {'operator': 'single', 'required': ['i', 'j']}
    },
    {
        'num': 5,
        'title': 'Amount Remaining (Coin Change)',
        'prompt': 'You\'re making change for `amount` using coins.\nWhat\'s the base case for "I\'ve successfully made exact change"?\n\nWrite the condition: ',
        'answer': 'if amount == 0:\n    return 0  # or 1 for counting, or True for boolean',
        'explanation': f'{BOLD}One condition{RESET} — exact match means success.',
        'keywords': {'operator': 'single', 'required': ['amount', '0']}
    },
    {
        'num': 6,
        'title': 'Grid Path with Obstacles',
        'prompt': 'You\'re at (r, c) in a grid with obstacles marked \'X\'.\nWhat\'s the condition for "this cell is invalid"?\n\nWrite the full check: ',
        'answer': 'rinbounds = 0 <= r < len(grid)\ncinbounds = 0 <= c < len(grid[0])\n\nif not rinbounds or not cinbounds or grid[r][c] == \'X\':\n    return 0',
        'explanation': f'{BOLD}Why `or`?{RESET} {BOLD}Any one{RESET} of these problems (out of bounds OR obstacle) makes this cell invalid.\nYou don\'t need multiple problems — just one is enough to stop.\n\n{YELLOW}Note:{RESET} You must check bounds BEFORE accessing grid[r][c], otherwise you\'ll get an index error.',
        'keywords': {'operator': 'or', 'required': ['rinbounds', 'cinbounds', 'not', 'X']}
    },
    {
        'num': 7,
        'title': 'The One That Got You: Max Path Sum Grid',
        'prompt': 'You\'re finding the max sum path from (0,0) to (rows-1, cols-1) moving only right/down.\nWhat\'s the base case for reaching the destination?\n\nWrite the condition and return: ',
        'answer': 'if r == len(grid) - 1 and c == len(grid[0]) - 1:\n    return grid[r][c]',
        'explanation': f'{BOLD}Why `and`?{RESET} The destination is ONE specific cell — you must be at the last row {BOLD}AND{RESET} the last column.\n\n{RED}{BOLD}Why not `or`?{RESET} If you used `or`, you\'d return grid[r][c] for ANY cell on the last row\nor ANY cell on the last column — ignoring the remaining path to the actual corner.\n\n{YELLOW}This was your exact bug!{RESET}',
        'keywords': {'operator': 'and', 'required': ['r', 'len(grid)', 'c', 'len(grid[0])']}
    },
    {
        'num': 8,
        'title': 'Multiple Valid Endpoints',
        'prompt': 'You\'re doing DFS in a graph looking for ANY exit node.\nExit nodes are marked exit[node] == True.\nWhat\'s the base case?\n\nWrite the condition: ',
        'answer': 'if exit[node]:\n    return True',
        'explanation': f'{BOLD}One condition{RESET} — any exit works. No `and` needed because there\'s not a compound condition.\n\nIf there were multiple properties an exit needs:\n  if exit[node] and unlocked[node]:  # both required\n      return True',
        'keywords': {'operator': 'single', 'required': ['exit', 'node']}
    },
]

def run_drill():
    print_header("Interactive Drill: `or` vs `and` in Boundary Conditions")
    print_rule()

    print(f"{YELLOW}Instructions:{RESET}")
    print("  • For each question, write the Python condition")
    print("  • Focus on getting the logic right (and vs or)")
    print("  • Type 'skip' to see the answer")
    print("  • Type 'quit' to exit\n")

    input(f"{BOLD}Press Enter to start...{RESET}")

    correct_count = 0
    total = len(questions)

    for q in questions:
        print_header(f"Question {q['num']}/{total}: {q['title']}")
        print(f"{q['prompt']}", end='')

        user_answer = input().strip()

        if user_answer.lower() == 'quit':
            print(f"\n{YELLOW}Exiting drill. Come back soon!{RESET}\n")
            sys.exit(0)

        if user_answer.lower() == 'skip':
            print(f"\n{YELLOW}Showing answer:{RESET}")
            print(f"{GREEN}{q['answer']}{RESET}\n")
            print(q['explanation'])
            continue

        is_correct = check_answer(user_answer, q['keywords'], q['num'])

        if is_correct:
            correct_count += 1
            print(f"\n{GREEN}✓ Correct!{RESET}\n")
            print(q['explanation'])
        else:
            print(f"\n{RED}✗ Not quite.{RESET}\n")
            print(f"{YELLOW}Expected:{RESET}")
            print(f"{GREEN}{q['answer']}{RESET}\n")
            print(f"{YELLOW}Your answer:{RESET} {user_answer}\n")
            print(q['explanation'])

        input(f"\n{BOLD}Press Enter to continue...{RESET}")

    # Final score
    print_header("Drill Complete!")
    percentage = (correct_count / total) * 100

    if percentage == 100:
        print(f"{GREEN}{BOLD}Perfect score: {correct_count}/{total}! 🎉{RESET}")
        print(f"{GREEN}The pattern is locked in. You're ready to code.{RESET}\n")
    elif percentage >= 75:
        print(f"{YELLOW}{BOLD}Good work: {correct_count}/{total}{RESET}")
        print(f"{YELLOW}Review the questions you missed, then run the drill again.{RESET}\n")
    else:
        print(f"{RED}{BOLD}Score: {correct_count}/{total}{RESET}")
        print(f"{RED}Run through the drill again. The pattern will click.{RESET}\n")

    print(f"{BOLD}Remember:{RESET}")
    print(f"  {GREEN}Destination needs AND{RESET}")
    print(f"  {RED}Failure needs OR{RESET}\n")

if __name__ == '__main__':
    try:
        run_drill()
    except KeyboardInterrupt:
        print(f"\n\n{YELLOW}Interrupted. Run again when ready!{RESET}\n")
        sys.exit(0)
