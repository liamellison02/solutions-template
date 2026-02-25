# dsa solutions

DSA solutions repo template based on my [personal solutions repository](https://github.com/liamellison02/dsa-solutions).

The goal is to get (_or git_ :smirk:) credit for your DSA grind while making your practice sessions more organized, and hopefully gamify things a bit in the process.

This repo structure groups solutions by algorithmic/solution patterns in order to build stronger **active recall** and reinforce each problem-solving pattern when working through new problems.

## get started

1. fork or clone this repository
2. create your first solution:
   ```bash
   ./scripts/new lc 1 two-sum py arrays/hashing hashmap,complement
   ```
3. open the generated file, paste the leetcode method signature, and solve
4. fill in the `complexity:` and `notes:` fields in the metadata header
5. track your progress with `./scripts/stats`

## stats

<!-- stats-start -->
| | count |
|---|---|
| total solutions | 0 |
<!-- stats-end -->

Run `./scripts/stats` for a full breakdown by difficulty, pattern, and tags.

## pattern directory structure

solutions are organized by algorithm pattern in `problems/`:

```
problems/
├── arrays/
│   ├── hashing/          # hashmaps, hashsets, frequency counting
│   ├── intervals/        # merge, insert, overlap detection
│   ├── prefix_sum/       # prefix sums, 2D prefix sums
│   ├── simulation/       # step-by-step simulation
│   ├── sorting/          # sort-based solutions
│   └── two_pointers/     # left/right pointers, fast/slow
├── bit/                  # bit manipulation, bitwise operations
├── backtracking/         # subset/permutation generation, constraint satisfaction
├── binary_search/
│   └── on_array/         # binary search on sorted data
├── design/               # system/class design problems
├── dp/
│   ├── bitmask/          # bitmask DP, subset enumeration
│   ├── grid/             # 2D grid traversal DP
│   ├── interval/         # interval DP (burst balloons, etc.)
│   ├── linear/           # 1D DP, rolling state
│   ├── lis/              # longest increasing subsequence variants
│   ├── state_machine/    # multi-state transitions (buy/sell stock, etc.)
│   └── two_string/       # 2-sequence DP (edit distance, LCS, interleaving)
├── graphs/
│   ├── bfs/              # breadth-first search, multi-source BFS
│   ├── dsu/              # disjoint set union (union-find)
│   ├── mst/              # minimum spanning tree (Prim's, Kruskal's)
│   ├── shortest_path/    # Dijkstra's, Bellman-Ford
│   ├── topo/             # topological sort, Kahn's algorithm
│   └── traversal/        # DFS/BFS traversal, Eulerian paths
├── greedy/               # greedy choice property
├── heap/                 # heap/priority queue solutions
├── linked_list/
│   └── fast_slow/        # Floyd's cycle detection, middle finding
├── math/
│   ├── geometry/         # coordinate geometry, area calculations
│   └── number_theory/    # primes, divisibility, factorization
├── sliding_window/       # fixed and variable size windows
├── stack/
│   └── monotonic/        # monotonic stack (next greater, histogram)
├── strings/              # string manipulation, pattern matching
└── trees/
    ├── bfs/              # level-order traversal
    ├── bst/              # BST operations, balancing
    ├── construct/        # tree construction
    ├── dfs/              # pre/in/post-order traversal
    ├── lca/              # lowest common ancestor
    ├── segment_tree/     # segment tree operations
    └── traversal/        # iterative traversal
```

## usage

### create a new solution

```bash
./scripts/new <platform> <id> <slug> <lang> <pattern> [tags]

# leetcode
./scripts/new lc 125 valid-palindrome cpp arrays/two_pointers palindrome,string
./scripts/new lc 3 longest-substring-without-repeating py sliding_window hashset

# codeforces
./scripts/new cf 4A watermelon cpp math divisibility

# CSC2720 (Data Structures)
./scripts/new csc2720 hw3 graph-traversal py graphs/traversal bfs,dfs
```

### solution metadata format

each solution includes a header with important metadata:

```python
"""
platform: lc
id: 1
name: two sum
difficulty: easy
url: https://leetcode.com/problems/two-sum/
pattern: arrays/hashing
tags: hashmap,complement
complexity:
- time = O(n)
- space = O(n)
notes: use hashmap to store complement; for each num check if target - num already seen/in hashmap
"""
```

### view stats

```bash
./scripts/stats
```

### regenerate track READMEs

```bash
python3 scripts/gen_tracks.py
```

## tracks

solutions can also be browsed by platform in `tracks/`:

- [LeetCode](tracks/leetcode/)
- [Codeforces](tracks/codeforces/)
- [CSC 2720](tracks/csc_2720/)

## tags

tags describe the techniques, data structures, and problem characteristics used in a solution. they are comma-separated in the `tags:` metadata field.

**formatting rules:**
- lowercase, hyphen-separated (e.g. `two-pointers`, not `two_pointers`)
- no spaces around commas: `tags: greedy,sorting,hashing`
- use singular form: `array` not `arrays`, `string` not `strings`

**common tags by category:**

| category | tags |
|----------|------|
| Data structures | `array`, `linked-list`, `tree`, `binary-tree`, `bst`, `stack`, `queue`, `heap`, `matrix`, `grid`, `hashing`, `hashmap`, `hashset` |
| Traversal / search | `bfs`, `dfs`, `binary-search`, `two-pointers`, `sliding-window`, `recursion`, `iterative` |
| Sorting / ordering | `sorting`, `greedy`, `intervals`, `merge` |
| DP techniques | `dp`, `bottom-up`, `1d-dp`, `2d-dp`, `grid-dp`, `interval-dp`, `kadanes`, `subsequence`, `bitmask` |
| Graph algorithms | `dijkstras`, `topological`, `kahns`, `union-find`, `shortest-path`, `mst`, `dag`, `cycle` |
| Tree techniques | `lca`, `inorder-traversal`, `postorder` |
| String techniques | `string`, `palindrome`, `substring`, `subsequence` |
| Math | `math`, `geometry`, `number-theory`, `combinatorics`, `divisibility`, `primes` |
| Stack / queue variants | `monotonic-stack`, `monotonic-queue`, `minheap`, `priority-queue` |
| Problem characteristics | `simulation`, `design`, `backtracking`, `precompute`, `prefix-sum`, `counting`, `frequency`, `complement` |
| Bit manipulation | `bit`, `bitmask`, `bit-manipulation` |

