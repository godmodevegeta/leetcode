
## **1. BFS Template (Iterative, using Queue)**

### Grid BFS
This is the most common interview BFS setup for problems like "shortest path", "flood fill", "number of islands", etc.

```python
from collections import deque

def bfs_grid(start_r, start_c, grid):
    rows, cols = len(grid), len(grid[0])
    visited = set()
    q = deque()
    
    # 1️⃣ Push start into queue
    q.append((start_r, start_c))
    visited.add((start_r, start_c))
    
    # 2️⃣ Define directions (4-way or 8-way if needed)
    directions = [(1,0), (-1,0), (0,1), (0,-1)]
    
    while q:
        r, c = q.popleft()
        
        # ✏️ PROCESS node here (count, sum, collect coords, etc.)
        
        # 3️⃣ Traverse neighbors
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            
            # 4️⃣ Boundary + visit checks
            if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) not in visited:
                # Add more conditions here, e.g. grid[nr][nc] == 1
                visited.add((nr, nc))
                q.append((nr, nc))
```

**Adjustments you’ll usually make:**
- Change `directions` for diagonal moves:  
  `directions = [(1,0), (-1,0), (0,1), (0,-1), (1,1), (-1,-1), (1,-1), (-1,1)]`
- Add a condition inside neighbor check (`grid[nr][nc] == target_value`)
- Store extra info like **distance**: `q.append((nr, nc, dist+1))`

---

### Graph BFS
When you have adjacency lists (`graph = {node: [neighbors]}`):

```python
from collections import deque

def bfs_graph(start, graph):
    visited = set()
    q = deque([start])
    visited.add(start)
    
    while q:
        node = q.popleft()
        
        # ✏️ PROCESS node here
        
        for nei in graph[node]:
            if nei not in visited:
                visited.add(nei)
                q.append(nei)
```

---

## **2. DFS Template**

### Grid DFS (Recursive)
```python
def dfs_grid(r, c, grid, visited):
    rows, cols = len(grid), len(grid[0])
    
    # 1️⃣ Boundary + visited + condition check
    if (r < 0 or r >= rows or
        c < 0 or c >= cols or
        (r, c) in visited or
        grid[r][c] == 0):  # change this condition as needed
        return
    
    visited.add((r, c))
    
    # ✏️ PROCESS node here
    
    # 2️⃣ Explore neighbors
    directions = [(1,0), (-1,0), (0,1), (0,-1)]
    for dr, dc in directions:
        dfs_grid(r+dr, c+dc, grid, visited)
```

---

### Graph DFS (Recursive)
```python
def dfs_graph(node, graph, visited):
    if node in visited:
        return
    visited.add(node)
    
    # ✏️ PROCESS node here
    
    for nei in graph[node]:
        dfs_graph(nei, graph, visited)
```

---

### Graph DFS (Iterative with Stack)
Sometimes recursion depth could be a problem → iterative stack version:

```python
def dfs_graph_iterative(start, graph):
    visited = set()
    stack = [start]
    
    while stack:
        node = stack.pop()
        if node not in visited:
            visited.add(node)
            
            # ✏️ PROCESS node here
            
            # Append neighbors (order may matter)
            for nei in graph[node]:
                if nei not in visited:
                    stack.append(nei)
```

---

## Quick “Plug & Play” Rules
When adapting:
- **For grid problems:**  
  - Change the `directions`  
  - Adjust the **boundary checks**  
  - Change the **skip condition** (like `grid[r][c] == 0`)  
- **For graph problems:**  
  - Just adjust how you build your `graph` adjacency list
- **For weighted graphs:** BFS changes to **Dijkstra’s** (priority queue instead of deque)

---

If you want, I can give you a **universal BFS/DFS wrapper** that works for **both grids and graphs** so you don’t need to memorize two separate ones.  
