
# 🧩 Graph/Heap Problem-Solving Checklist  

| **Step** | **Question to Ask Yourself** | **What It Means / Why It Matters** | **How to Apply (Self-Elaboration)** |
|----------|------------------------------|------------------------------------|--------------------------------------|
| **1. Problem Category** | “What *type* of problem is this?” | Identifies the core template: DFS, BFS, Dijkstra/Prim (heap + visited), Kruskal (DSU), etc. | If it says *shortest path/min cost* → Dijkstra; *connect all nodes with min cost* → MST; *explore everything* → BFS/DFS. |
| **2. Invariant / Principle** | “What must always hold true as I progress?” | Keeps you focused on the rule the algorithm enforces. | MST grows with the cheapest edge that keeps graph connected. Swim always guarantees min of max elevations. Dijkstra always pops the true shortest node. |
| **3. State to Track** | “What minimal information do I need at each step?” | Avoids over-storing things like full paths when only a number matters. | In Swim: just track `max_so_far` (not full path). In MST: track `visited` + heap of candidate edges. |
| **4. Dry Run (Mini Example)** | “How does this play out on a 3×3 grid or 4-node graph?” | Forces you to simulate 2–3 steps and see the invariant in action. | Write heap contents: after first pop, what do I push? After 2nd pop, which state do I update? This clarifies correctness before coding. |
| **5. Pseudocode First** | “Can I express this in 5–8 lines of pseudocode?” | Ensures you code the principle, not trial-and-error. | Example for Swim: `PQ=[(grid[0][0],0,0)] → pop → if end return cost → push neighbors`. If it fits, start coding; if not, rethink. |

---

### ✅ How to Use This in Practice
1. Print/write this table next to your workspace.  
2. For every new problem, spend **5–7 minutes** just filling in Steps 1–5 *before touching Python*.  
3. Only after you can confidently write the pseudocode, open the editor.  
4. After solving, revisit Step 2 + Step 3 → ask: *Did my code actually follow the invariant with minimal state?*  

---

Example: Let’s run **778. Swim in Rising Water** through the checklist step by step so you see how to *apply it before coding*.  


# 🧩 Example Walkthrough: 778. Swim in Rising Water  

| **Step** | **Answer for This Problem** | **Self-Elaboration** |
|----------|------------------------------|-----------------------|
| **1. Problem Category** | Shortest-path style on a grid → use **Dijkstra’s algorithm / Prim-like heap expansion**. | Why? We need the *minimum time until bottom-right is reachable*. This is like finding the “least-cost path” where cost is the **max height so far**. BFS won’t work (different weights), plain DFS won’t minimize. |
| **2. Invariant / Principle** | Every time I pop from the min-heap, that cell is the **earliest time I can swim there**. | Just like Dijkstra: once a cell is popped, I know the minimal possible max-height to reach it. I never need to revisit it. |
| **3. State to Track** | `time_so_far` = the max(height) along path to current cell. Keep a `visited` set. | I don’t need to store the *entire path*, only the **current best effort** (time_so_far). That’s the key difference from your first trial. |
| **4. Dry Run (Mini Example)** | Grid = `[[0,2],[1,3]]`. <br> PQ = [(0,(0,0))]. Pop → (0,(0,0)). Push neighbors: (2,(0,1)), (1,(1,0)). Pop → (1,(1,0)). Time= max(0,1)=1. Push neighbor (3,(1,1)). PQ = [(2,(0,1)), (3,(1,1))]. Pop → (2,(0,1)). Push neighbor (3,(1,1)). PQ = [(2,(1,1)), (3,(1,1))]. Pop → (2,(1,1)) → reached end. Return 2. | Dry run shows clearly how PQ evolves and why the result is correct. Confirms invariant. |
| **5. Pseudocode First** | ```<br>pq = [(grid[0][0], 0,0)]<br>visited = set()<br>while pq:<br>    time, r, c = heappop(pq)<br>    if (r,c) == end: return time<br>    if (r,c) in visited: continue<br>    visited.add((r,c))<br>    for each neighbor:<br>        heappush(pq, (max(time, grid[nr][nc]), nr, nc))<br>``` | Notice how compact this is. Captures the invariant. Now when I implement, it’s just a translation exercise. |

---

✅ See the shift?  
Instead of: *“Let me code and hope it works”* → you first confirm:  
- This is Dijkstra-like.  
- Invariant is “earliest possible arrival”.  
- State is just `(time_so_far, r, c)`.  
- Dry run shows correctness.  
- Pseudocode nails it in <10 lines.  

By the time you type Python, you’re not “debugging the idea” anymore, only syntax.  

---

Do you want me to **do the same checklist fill-out for 1584. Min Cost to Connect All Points** too, so you see both MST and Dijkstra-style examples side by side?