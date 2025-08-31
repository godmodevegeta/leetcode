
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
