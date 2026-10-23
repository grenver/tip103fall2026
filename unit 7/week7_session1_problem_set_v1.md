# Unit 7 · Session 1 · Problem Set Version 1

Connected components and Union Find. Runnable solutions and labeled checks: [Python file](week7_session1_problem_set_v1.py).

| Problem | Callable | Main concept | Prerequisite / explanation goal |
| --- | --- | --- | --- |
| [1. Number of Provinces](#problem-1-number-of-provinces) | `find_circle_num` | Matrix connections | Explain indirect connectivity |
| [2. Redundant Connection](#problem-2-redundant-connection) | `find_redundant_connection` | Detect a cycle | Explain a failed merge |
| [3. Graph Valid Tree](#problem-3-graph-valid-tree) | `valid_tree` | Connectivity and no cycles | Explain why edge count alone is insufficient |
| [4. Number of Connected Components](#problem-4-number-of-connected-components) | `count_components` | Count successful merges | Include isolated nodes |
| [5. Accounts Merge](#problem-5-accounts-merge) | `accounts_merge` | Map emails to components | Distinguish shared emails from shared names |

## Shared prerequisite: Union Find

A component is a group joined by paths. Union Find stores each group as a parent tree: a root points to itself, and following parents reaches the group's representative. For example, `parent = [0, 0, 2]` means nodes 0 and 1 belong together; node 2 is separate. A root is an internal label, not necessarily the smallest node.

`find(node)` returns its root. `union(a, b)` returns `True` when two different groups merge, or `False` when they already belong together. Starting with n singleton groups, only successful merges subtract one from the count. Path halving points nodes toward their grandparents; union by size attaches the smaller tree to the larger. Together they make operations almost constant on average.

In the helper, `self` refers to the particular UnionFind object. `self.parent`, `self.size`, and `self.components` are state shared by that object's methods. A fresh object is created for each function call. The parent array changes internally; input graphs do not.

<details>
<summary>Shared helper required by all five solutions</summary>

```python
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n
        self.components = n

    def find(self, node):
        while node != self.parent[node]:
            # Point toward the grandparent to shorten future searches.
            self.parent[node] = self.parent[self.parent[node]]
            node = self.parent[node]
        return node

    def union(self, a, b):
        root_a, root_b = self.find(a), self.find(b)
        if root_a == root_b:
            return False  # Already in the same component.
        if self.size[root_a] < self.size[root_b]:
            root_a, root_b = root_b, root_a
        self.parent[root_b] = root_a
        self.size[root_a] += self.size[root_b]
        self.components -= 1
        return True
```

</details>

For complexity, alpha(n) is the inverse Ackermann function, which grows extremely slowly. A sequence of Union Find operations costs O(alpha(n)) per operation amortized; initialization still costs O(n). Dictionary operations below use expected constant time. Copy the helper along with a solution when submitting it independently.

## Problem 1: Number of Provinces

**Learning goal / recognition clue:** Identify groups joined by paths when input gives a symmetric adjacency matrix. An indirect connection matters just as much as a direct one.

### U — Understand

`find_circle_num(is_connected)` returns an integer province count. Assume a square symmetric matrix for an undirected graph. Diagonal 1s describe each city's connection to itself and do not join separate cities. `[[1,1,0],[1,1,0],[0,0,1]]` returns `2`; the identity matrix of size 3 returns `3`.

### P — Plan

1. Create one component for each city.
2. Scan entries above the diagonal; merge each pair marked 1.
3. Return the remaining component count.

**Trace:** Start with `{0}, {1}, {2}` and count 3. Entry (0,1) merges 0 and 1, making count 2. Entries (0,2) and (1,2) are 0, so the answer stays 2.

**Why it works:** Each processed connection places its endpoints in the same component. Repeated merges also join entire paths. Every undirected pair appears once above the diagonal, so no needed connection is missed. The finite pair scan terminates.

**Try first:** Why can you skip the lower triangle? Next hint: compare entries (i,j) and (j,i). Final hint: loop over `neighbor` starting at `city + 1`.

### I — Implement

<details>
<summary>Show solution</summary>

```python
def find_circle_num(is_connected):
    n = len(is_connected)
    groups = UnionFind(n)
    for city in range(n):
        for neighbor in range(city + 1, n):
            if is_connected[city][neighbor] == 1:
                groups.union(city, neighbor)
    return groups.components
```

</details>

**Code connection / checks:** `groups.components` is the group's current count, not a count of matrix 1s. The runnable checks include both supplied examples, one city, and a chain where 0 reaches 2 only through 1.

**Cost:** Let n be the number of cities. There are n(n−1)/2 inspected pairs and at most that many unions: O(n² alpha(n)) amortized time, a simple upper bound, and O(n) auxiliary space. The input matrix already occupies O(n²) space. DFS on the matrix is an alternative with O(n²) time.

**Common mistakes:** Counting direct pairs misses paths → merge entire groups. Subtracting even when roots match undercounts provinces → subtract only for a successful union.

**Interview explanation:** I start with one province per city and union each direct connection. The roots encode indirect paths too, so the final number of groups is the answer. Scanning the matrix dominates the work, with the Union Find bound given above.

**Check your understanding:** How many provinces does a three-city chain have? How would an adjacency-list input change the scan?

<details>
<summary>Reasoning and answers</summary>

One: connectivity follows the whole chain. With adjacency lists, scan listed edges instead of every possible pair; the bound becomes O(n + E alpha(n)) for E listed connections.

</details>

## Problem 2: Redundant Connection

**Learning goal / recognition clue:** Recognize an edge whose endpoints already have a path between them. Adding that edge closes a cycle.

### U — Understand

`find_redundant_connection(edges)` returns a two-item list. The graph is a tree plus one extra undirected edge, with labels 1..n. Under this contract n equals the number of edges. Return the last input edge that can be removed to restore a tree. The supplied examples return `[2,3]` and `[1,4]`.

### P — Plan

1. Allocate n+1 parent entries to support labels 1..n; ignore slot 0.
2. Process edges in input order, joining different components.
3. Return the edge whose union fails.

**Trace:** `[1,2]` joins two groups; `[1,3]` puts 3 with 1 and 2. For `[2,3]`, both endpoints now share a root. Return `[2,3]`.

**Why it works / last-edge rule:** The unique cycle's last input edge has all the other cycle edges processed before it, forming an existing path between its endpoints. Earlier cycle edges cannot close that cycle yet. Edges outside the cycle cannot close any cycle. Therefore the first failed union is precisely the last removable cycle edge. The return is correct even when later non-cycle edges remain.

**Try first:** What makes a new edge redundant? Next hint: test whether the endpoints share a root. Final hint: use the Boolean returned by `union`.

### I — Implement

<details>
<summary>Show solution</summary>

```python
def find_redundant_connection(edges):
    groups = UnionFind(len(edges) + 1)  # Index 0 is unused.
    for a, b in edges:
        if not groups.union(a, b):
            return [a, b]
    return []  # Unused for the guaranteed tree-plus-one-edge input.
```

</details>

**Code connection / checks:** `not groups.union(a, b)` means an existing path already connects a and b. Checks include both supplied examples and a reordered cycle. The fallback `[]` is outside the guaranteed valid input behavior.

**Cost:** For n edges and n nodes, O(n alpha(n)) amortized time and O(n) auxiliary space.

**Common mistakes:** Comparing immediate parents can miss a shared root → call `find`. Returning the numerically largest edge misreads “last” → preserve input order.

**Interview explanation:** I process edges in order and maintain connected components. A failed union identifies a cycle-closing edge; with exactly one cycle, it is the last input edge on that cycle. This uses O(n) space and almost linear time.

**Check your understanding:** Why not return the final input edge unconditionally? Would this early return solve the same removal task for a graph with several cycles?

<details>
<summary>Reasoning and answers</summary>

The final edge may attach a leaf, as `[1,5]` does in the second example. Several cycles violate the contract: removing one detected edge may leave another cycle, so this argument would no longer solve the task.

</details>

## Problem 3: Graph Valid Tree

**Learning goal / recognition clue:** Combine two requirements: all nodes must connect, and no cycle may exist.

### U — Understand

`valid_tree(n, edges)` returns a Boolean for nodes 0..n−1. Assume n >= 1 and valid node labels; the prompt does not define an empty graph as a tree. The supplied star with a branch returns `True`; the graph with cycle 1–2–3–1 returns `False`.

### P — Plan

1. Reject unless there are exactly n−1 edges.
2. Union every edge; reject if any merge fails.
3. Confirm that one component remains.

**Trace:** For n=4 and `[[0,1],[1,2],[2,0]]`, the edge count is 3, so it passes the first test. The first two merges succeed; the third closes a cycle. Return `False`; node 3 is isolated.

**Why it works:** A tree on n nodes has n−1 edges. If all n−1 unions succeed, the component count decreases from n to 1 without a cycle. Each edge is examined at most once, so the algorithm terminates.

**Try first:** Is n−1 edges sufficient alone? Next hint: a triangle plus an isolated node has the right count. Final hint: reject a failed merge.

### I — Implement

<details>
<summary>Show solution</summary>

```python
def valid_tree(n, edges):
    if len(edges) != n - 1:
        return False
    groups = UnionFind(n)
    for a, b in edges:
        if not groups.union(a, b):
            return False
    return groups.components == 1
```

</details>

**Code connection / checks:** The final component check states the connectivity requirement explicitly. Checks cover both examples, a single node, too few edges, and a disconnected graph with n−1 edges.

**Cost:** Let E be the number of edges. A wrong edge count returns in O(1) time and space. Otherwise E=n−1; the bound is O(n + E alpha(n)) amortized time and O(n) auxiliary space.

**Common mistakes:** Checking only the edge count accepts a disconnected cycle → also check unions. Rejecting a single node with no edges is incorrect → it is connected and acyclic.

**Interview explanation:** I check the necessary edge count and reject cycle-closing edges. Every accepted edge merges two components, so n−1 successes leave exactly one component. This establishes both tree properties.

**Check your understanding:** Is `valid_tree(2, [])` true? What changes if the task asks only whether the graph is a forest?

<details>
<summary>Reasoning and answers</summary>

False: the two nodes are disconnected. For a forest, allow multiple components and any appropriate edge count; only reject cycles.

</details>

## Problem 4: Number of Connected Components

**Learning goal / recognition clue:** Count groups using the effect of successful merges, including nodes absent from the edge list.

### U — Understand

`count_components(n, edges)` returns an integer for an undirected graph labeled 0..n−1. The examples return 2 for `[[0,1],[1,2],[3,4]]` and 1 for a five-node chain. Cycles do not create additional components.

### P — Plan

1. Start with n singleton components.
2. Union endpoints of every edge.
3. Return the component count; ignore failed unions.

**Trace:** With n=5, counts after `[0,1]`, `[1,2]`, and `[3,4]` are 4, 3, and 2. An additional `[0,2]` would leave the count at 2.

**Why it works:** Every successful merge joins exactly two groups and reduces the count by one. Internal edges leave the partition unchanged. After the finite edge scan, every path is represented by a shared group.

**Try first:** How many components exist before reading edges? Next hint: isolated nodes still count. Final hint: initialize with n, not the number of labels appearing in edges.

### I — Implement

<details>
<summary>Show solution</summary>

```python
def count_components(n, edges):
    groups = UnionFind(n)
    for a, b in edges:
        groups.union(a, b)
    return groups.components
```

</details>

**Code connection / checks:** The helper maintains the count, so the loop need not subtract manually. Checks cover the examples, no edges, and a cycle with an isolated node.

**Cost:** For n nodes and E edges, O(n + E alpha(n)) amortized time and O(n) auxiliary space.

**Common mistakes:** Returning n−E undercounts when there is a cycle → count successful unions. Building state only for edge endpoints omits isolated nodes → initialize all n nodes.

**Interview explanation:** I initialize one group per node and merge the endpoints of each edge. Failed unions preserve the count, so cycles do not cause overcounting of merges. The final count includes isolated nodes automatically.

**Check your understanding:** What is the result for 4 nodes and no edges? What if an existing edge appears twice?

<details>
<summary>Reasoning and answers</summary>

Four singleton components. If duplicates are allowed as an extension, the second copy cannot merge groups again and does not change the answer.

</details>

## Problem 5: Accounts Merge

**Learning goal / recognition clue:** Use a dictionary to translate shared identifiers into connections, then group by final roots. Shared emails, rather than matching names, define identity.

### U — Understand

`accounts_merge(accounts)` returns lists containing a name followed by sorted unique emails. Assume every account has at least one email and all accounts connected through emails have a consistent name. The prompt does not specify handling name-only entries or conflicting names. The outer account order is unspecified; this solution sorts it for reproducibility and to match the supplied output.

The supplied four accounts produce two separate John groups and one Mary group. The John account with `johnnybravo@mail.com` shares no email with the other Johns, so it remains separate.

### P — Plan

1. Give each account index its own component. Store the first owner index of each email in a dictionary.
2. When an email repeats, union the current account with its stored owner.
3. After all merges, visit each unique email, find its owner's final root, and append it to that root's list.
4. Sort each email list, prepend the component's name, and sort the returned account lists.

**Trace:** Accounts `['A','x','y']`, `['A','z']`, `['A','y','z']` start separately. Account 2 shares y with account 0, then z with account 1. All three merge even though accounts 0 and 1 share no direct email. Grouping afterward yields `['A','x','y','z']`.

**Why it works:** A union occurs only for an actual shared email, so unrelated equal names remain separate. Repeated unions capture transitive sharing. Each unique email is then assigned to exactly one final component. Both passes inspect finite input collections.

**Try first:** What can serve as evidence that two accounts connect? Next hint: map an email to an account index. Final hint: finish unions before collecting emails by root.

### I — Implement

<details>
<summary>Show solution</summary>

```python
def accounts_merge(accounts):
    groups = UnionFind(len(accounts))
    email_owner = {}
    for index, account in enumerate(accounts):
        for email_index in range(1, len(account)):
            email = account[email_index]
            if email in email_owner:
                groups.union(index, email_owner[email])
            else:
                email_owner[email] = index

    emails_by_root = {}
    for email, owner in email_owner.items():
        root = groups.find(owner)
        if root not in emails_by_root:
            emails_by_root[root] = []
        emails_by_root[root].append(email)

    merged = []
    for root, emails in emails_by_root.items():
        merged.append([accounts[root][0]] + sorted(emails))
    # Outer order is unspecified; sort for a reproducible displayed result.
    return sorted(merged)
```

</details>

**Code connection:** In `email_owner`, keys are email strings and values are account indices. `email in email_owner` tests keys. In `emails_by_root`, keys are integer roots and values are lists of emails. `.items()` gives key/value pairs. Iterating the first dictionary once removes duplicate email occurrences without needing a separate set. The stored owner may no longer be a root; `find(owner)` resolves its current component.

**Checks:** The Python file checks the supplied output, a transitive bridge, equal names with disjoint emails, and a repeated email within one account.

**Cost:** Let A be accounts, T total email occurrences, and U unique emails. With constant-time string hashing/comparison as the usual model, the total is expected O(A + T alpha(A) + U log(U+1)) amortized time. Each email occurrence may cause a union; sorting all email groups costs at most O(U log(U+1)). The outer sort fits the same bound: there are at most U groups, and two different groups differ by name or by their first email, because their emails are disjoint. For actual strings, include character-processing costs as well. Auxiliary space is O(A+U), with O(A+U) returned entries.

**Common mistakes:** Merging by name combines different people → merge by email. Grouping before all unions can leave stale root buckets → collect after merging. Sorting accounts does not sort their emails → sort each component's email list too.

**Interview explanation:** I map each email to an account index and union accounts whenever that email reappears. After all transitive merges, I group unique emails by final root and sort each group's emails. Equal names alone never cause a merge; sorting and Union Find determine the costs above.

**Check your understanding:** Do two John accounts with disjoint emails merge? Why can an email's stored owner remain unchanged after unions?

<details>
<summary>Reasoning and answers</summary>

No: names alone are insufficient. The owner is still a valid node in the right component; `find` follows its updated parents to the final root.

</details>

## Run the checks

From the repository root, run `python "unit 7/week7_session1_problem_set_v1.py"` using the selected Python interpreter. A successful run prints five labeled passing messages. Assertions check the supplied examples and the boundary cases described above.
