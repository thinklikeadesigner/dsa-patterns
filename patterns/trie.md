# Trie (Prefix Tree) [Google Heavy]

## When to Use
When you need **prefix-based operations**: autocomplete, spell check, word search in a grid, or checking if any word starts with a given prefix. Key signal: "search for words by prefix", "word dictionary", "word search II" (multiple words in a grid).

## Core Idea
A tree where each node represents a character. Paths from root to nodes spell out prefixes; nodes marked as "end" indicate complete words. Insert and search are both O(L) where L is word length. Much faster than sorting + binary search for prefix queries.

## Template Code

```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.is_end = True

    def search(self, word):
        node = self._find(word)
        return node is not None and node.is_end

    def starts_with(self, prefix):
        return self._find(prefix) is not None

    def _find(self, prefix):
        node = self.root
        for ch in prefix:
            if ch not in node.children:
                return None
            node = node.children[ch]
        return node

# Word Search II (Trie + DFS on grid)
def find_words(board, words):
    trie = Trie()
    for word in words:
        trie.insert(word)

    rows, cols = len(board), len(board[0])
    result = set()

    def dfs(r, c, node, path):
        if node.is_end:
            result.add(path)
            node.is_end = False  # avoid duplicates

        if r < 0 or r >= rows or c < 0 or c >= cols:
            return
        ch = board[r][c]
        if ch not in node.children:
            return

        board[r][c] = '#'  # mark visited
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            dfs(r + dr, c + dc, node.children[ch], path + ch)
        board[r][c] = ch   # restore

    for r in range(rows):
        for c in range(cols):
            dfs(r, c, trie.root, "")

    return list(result)

# Autocomplete (collect all words with prefix)
def autocomplete(trie, prefix):
    node = trie._find(prefix)
    if not node:
        return []
    results = []
    def collect(node, path):
        if node.is_end:
            results.append(path)
        for ch, child in node.children.items():
            collect(child, path + ch)
    collect(node, prefix)
    return results
```

## Key Variations
- **Basic operations**: Insert, search, startsWith
- **Word search on grid**: Trie + DFS — much faster than searching each word separately
- **Autocomplete**: DFS from prefix node to collect all completions
- **Count prefixes**: Store count in each node instead of boolean

## Problems Solved
| Problem | Date | Result | Notes |
|---------|------|--------|-------|

## My Mistakes
- (none yet)
