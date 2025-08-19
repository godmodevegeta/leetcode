from collections import deque, defaultdict
from typing import List
graph = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F'],
    'D': [],
    'E': ['F'],
    'F': []
}
def printArray(a):
    for row in range(len(a)):
        for col in range (len(a)):
            print("T" if a[row][col] else "F", end=" ")
        print()

# print(graph)
def bfs(graph, start):
    visited = set()
    queue = deque([start])

    while queue:
        node = queue.popleft()
        if node not in visited:
            
            print(queue, node)  # process node
            visited.add(node)
            queue.extend(neighbor for neighbor in graph[node] if neighbor not in visited)

# bfs(graph, "B")

# def topsortDFS(graph):
#     visited = set()
#     stack = []

#     def dfs(node):
#         if node in visited:
#             return
#         visited.add(node)
#         for next in graph[node]:
#             dfs(next)
#         stack.append(node)
#     for node in graph:
#         if node not in visited:
#             dfs(node)
#     return stack[::-1]

# print(topsortDFS(graph))

# def topoSortWithCycleDetection(graph):
#     state = {node: 0 for node in graph}  # 0=unvisited, 1=visiting, 2=visited
#     result = []
#     has_cycle = False
#     print(state)

#     def dfs(node):
#         nonlocal has_cycle
#         if state[node] == 1:
#             has_cycle = True
#             return
#         if state[node] == 2:
#             return

#         state[node] = 1  # mark as visiting
#         for neighbor in graph.get(node, []):
#             dfs(neighbor)
#         state[node] = 2  # mark as visited
#         result.append(node)

#     for node in graph:
#         if state[node] == 0:
#             dfs(node)
#         if has_cycle:
#             break

#     if has_cycle:
#         return None  # cycle detected
#     return result[::-1]  # topological order

# (topoSortWithCycleDetection(graph))
# numCourses = 3
# prerequisites = [[1,2],[1,0],[2,0]]
# queries = [[1,0],[1,2]]

# numCourses = 13
# prerequisites = [[2,1],[2,7],[2,0],[2,10],[2,11],[1,7],[1,0],[1,9],[1,4],[1,11],[7,3],[7,9],[7,4],[7,11],[7,8],[3,6],[3,12],[3,5],[6,10],[6,8],[0,4],[12,9],[12,8],[9,4],[9,11],[9,8],[9,5],[10,8],[4,8]]
# queries = [[12,11],[11,1],[10,12],[9,10],[10,11],[11,12],[2,7],[6,8],[3,2],[9,5],[8,7],[1,4],[3,12],[9,6],[4,3],[11,4],[5,7],[3,9],[3,1],[8,12],[5,12],[0,8],[10,5],[10,11],[12,11],[12,9],[5,4],[11,5],[12,10],[11,0],[6,10],[11,7],[8,10],[2,1],[3,4],[8,7],[11,6],[9,11],[1,4],[10,8],[7,1],[8,7],[9,7],[5,1],[8,10],[11,8],[8,12],[9,12],[12,11],[6,12],[12,11],[6,10],[9,12],[8,10],[8,11],[8,5],[7,9],[12,11],[11,12],[8,0],[12,11],[7,0],[8,7],[5,11],[11,8],[1,9],[4,10],[11,6],[10,12]]

# def checkIfPrerequisite(numCourses: int, prerequisites: List[List[int]], queries: List[List[int]]) -> List[bool]:
#     graph = defaultdict(list)
#     reachable = [[False] * numCourses for i in range(numCourses)]
#     for u, v in prerequisites:
#         graph[u].append(v)
#         reachable[u][v] = True
    
#     for i in range(numCourses):
#         for k in range(numCourses):
#             for j in range(numCourses):
#                 if reachable[i][k] and reachable[k][j]:
#                     reachable[i][j] = True
#     printArray(reachable)
    
#     print(graph)
#     return [reachable[u][v] for u, v in queries]

# print(checkIfPrerequisite(numCourses, prerequisites, queries))

class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))  # or: {i: i for i in range(n)}
        self.rank = [0] * n           # optional: for union by rank

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # path compression
        return self.parent[x]

    def union(self, x, y):
        px, py = self.find(x), self.find(y)
        if px == py:
            return False  # already in the same set
        # union by rank (optional optimization)
        if self.rank[px] < self.rank[py]:
            self.parent[px] = py
        elif self.rank[px] > self.rank[py]:
            self.parent[py] = px
        else:
            self.parent[py] = px
            self.rank[px] += 1
        return True

    def connected(self, x, y):
        return self.find(x) == self.find(y)
    
accounts = [["John","johnsmith@mail.com","john_newyork@mail.com"],
            ["John","johnsmith@mail.com","john00@mail.com"],
            ["Mary","mary@mail.com"],
            ["John","johnnybravo@mail.com"]]

def accountsMerge(accounts: List[List[str]]) -> List[List[str]]:
    uf = UnionFind(len(accounts))
    emailToAcc = {}
    for i, a in enumerate(accounts):
        for e in a[1:]:
            if e in emailToAcc:
                uf.union(i, emailToAcc.get(e))
            else:
                emailToAcc[e] = i
    # print(emailToAcc)
    # print(uf.parent)
    # print(uf.rank)

    emailGroup = defaultdict(list)
    for e, i in emailToAcc.items():
        leader = uf.find(i)
        emailGroup[leader].append(e)

    res = []
    for i, emails in emailGroup.items():
        name = accounts[i][0]
        res.append([name] + sorted(emailGroup[i]))
    return res

# print(accountsMerge(accounts))
equations = [["a","b"],["b","c"]]
values = [2.0,3.0]
queries = [["a","c"],["b","a"],["a","e"],["a","a"],["x","x"]]
def calcEquation(equations: List[List[str]], values: List[float], queries: List[List[str]]) -> List[float]:
    graph = defaultdict(list)
    res = []
    
        
    for i, equation in enumerate(equations):
        graph[equation[0]].append([equation[1], values[i]])
        graph[equation[1]].append([equation[0], 1.0/values[i]])
    for query in queries:
        src, dst = query[0], query[1]
        ans, visited = 1, set()
        
    return res

# print(calcEquation(equations, values, queries))


# 200. Number of Islands
grid = [
  ["1","1","0","0","0"],
  ["1","0","0","1","1"],
  ["0","0","1","1","0"],
  ["0","0","0","0","0"],
  ["1","0","1","0","1"]
]


def numIslands(grid: List[List[str]]) -> int:
    row, col = len(grid), len(grid[0])
    visited = set()
    ans = 0
    def dfs(r, c):
        if ((r < 0 or r >= row) or (c < 0 or c >= col) or grid[r][c] == "0" or ((r,c) in visited)): return False
        visited.add((r,c))
        dir = [[-1, 0], [0, 1], [0, -1], [1, 0]]
        for dr, dc in dir:
            dfs(r + dr,  c + dc)
        return True
    for r in range(row):
        for c in range(col):
            if dfs(r, c): ans += 1
    return ans

# 695. Max Area of Island
grid = [
    [0,0,1,0,0,0,0,1,0,0,0,0,0],
    [0,0,0,0,0,0,0,1,1,1,0,0,0],
    [0,1,1,0,1,0,0,0,0,0,0,0,0],
    [0,1,0,0,1,1,0,0,1,0,1,0,0],
    [0,1,0,0,1,1,0,0,1,1,1,0,0],
    [0,0,0,0,0,0,0,0,0,0,1,0,0],
    [0,0,0,0,0,0,0,1,1,1,0,0,0],
    [0,0,0,0,0,0,0,1,1,0,0,0,0]
]

def maxAreaOfIsland(grid: List[List[int]]) -> int:
    row, col = len(grid), len(grid[0])
    visited = set()
    def findArea(r, c) -> int:
        if (r < 0 or r >= row or c < 0 or c >= col or grid[r][c] == 0 or (r,c) in visited): return 0
        visited.add((r,c))
        area = 1
        directions = [(1, 0), (0, -1), (-1, 0), (0, 1)]
        for dr,dc in directions:
            area += findArea(r + dr, c + dc)
        return area
    maxArea = 0
    for r in range(row):
        for c in range(col):
            area = findArea(r,c)
            maxArea = max(area, maxArea)
    return maxArea
    
# 994. Rotting Oranges
grid = [[2,1,1],
        [1,1,2],
        [0,1,1]]

def orangesRotting(grid: List[List[int]]) -> int:
    
    row, col = len(grid), len(grid[0])
    freshOranges = 0
    maxTime = 0
    visited = set()

    queue = deque()
    for r in range(row):
        for c in range(col):
            if grid[r][c] == 1: freshOranges += 1
            if grid[r][c] == 2: 
                queue.append((r, c, 0))
    
    while queue:
        r, c, time = queue.popleft()
        maxTime = time
        # print(r, c, time, sep=" () ")
        directions = [(1, 0), (0, -1), (-1, 0), (0, 1)]
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if (nr >= 0 and nr < row) and (nc >= 0 and nc < col) and grid[nr][nc] == 1 and (nr, nc) not in visited:
                freshOranges -= 1
                visited.add((nr, nc))
                queue.append((nr, nc, time + 1))

    return maxTime if freshOranges == 0 else -1
    


# 417. Pacific Atlantic Water Flow (DFS)

heights = [[1,2,2,3,5],[3,2,3,4,4],[2,4,5,3,1],[6,7,1,4,5],[5,1,1,2,4]]

def pacificAtlantic(heights: List[List[int]]) -> List[List[int]]:
    row, col = len(heights), len(heights[0])
    pacific_reachable = set()
    atlantic_reachable = set()

    def dfs(r,c, visited):
        if (r >= 0 and r < row and c >= 0 and c < col and (r,c) not in visited):

            visited.add((r,c)) # this cell is reachable from pacific
            directions = [(1, 0), (0, 1), (0, -1), (-1, 0)]
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < row and 0 <= nc < col:
                    if heights[nr][nc] >= heights[r][c]: dfs(nr, nc, visited)



    for c in range(col):
        dfs(0, c, pacific_reachable)
    for c in range(col):
        dfs(row - 1, c, atlantic_reachable)
    for r in range(row):
        dfs(r, 0, pacific_reachable)
    for r in range(row):
        dfs(r, col - 1, atlantic_reachable)

    return [[r, c] for (r, c) in pacific_reachable & atlantic_reachable]
    
# 417. Pacific Atlantic Water Flow (BFS)

def pacificAtlantic(heights: List[List[int]]) -> List[List[int]]:
    row, col = len(heights), len(heights[0])
    pacific_reachable = set()
    atlantic_reachable = set()
    queue = deque()

    # pacific
    for c in range(col):
        queue.append((0, c))
    for r in range(row):
        queue.append((r, 0))
        
    while queue:
        r,c = queue.popleft()
        directions = [(1, 0), (0, 1), (0, -1), (-1, 0)]
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if (0 <= nr < row and 0 <= nc < col and (nr, nc) not in pacific_reachable and heights[nr][nc] >= heights[r][c]):
                pacific_reachable.add((nr,nc))
                queue.append((nr,nc))


    # atlantic
    for c in range(col):
        queue.append((row - 1, c))
    for r in range(row):
        queue.append((r, col - 1))
        
    while queue:
        r,c = queue.popleft()
        
        directions = [(1, 0), (0, 1), (0, -1), (-1, 0)]
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if (0 <= nr < row and 0 <= nc < col and (nr, nc) not in atlantic_reachable and heights[nr][nc] >= heights[r][c]):
                atlantic_reachable.add((nr,nc))
                queue.append((nr,nc))

    return [[r,c] for (r,c) in pacific_reachable & atlantic_reachable]

# 130. Surrounded Regions

board = [["X","X","X","X"],
         ["X","O","O","X"],
         ["X","X","O","X"],
         ["X","O","X","X"]]

def solve(board: List[List[str]]) -> None:
    """
    Do not return anything, modify board in-place instead.
    """
    row, col = len(board), len(board[0])
    visited = set()
    def dfs(r,c):
        if ((r < 0 or r >= row) or (c < 0 or c >= col) or (r,c) in visited or board[r][c] == "X"):
            # print(f"Nothing at ({r}, {c})")
            return
        visited.add((r,c))
        # print(f"I'm at ({r},{c})")
        directions = [(1, 0), (0, 1), (0, -1), (-1, 0)]
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if (0 <= nr < row and 0 <= nc < col): dfs(nr,nc)
    for r in range(row):
        dfs(r,0)
        dfs(r,col - 1)
    for c in range(col):       
        dfs(0,c)
        dfs(row - 1, c)


    for r in range(row):
        for c in range(col):
            if board[r][c] == "O" and (r,c) not in visited: board[r][c] = "X"
          
# 207. Course Schedule
numCourses = 4
prerequisites = [[1,0],[2,1],[3,2]]

def canFinish(numCourses: int, prerequisites: List[List[int]]) -> bool:
    adj = defaultdict(list)
    for dst, src in prerequisites:
        adj[src].append(dst)

    visited = {}
    for i in range(numCourses):
        visited[i] = 0
    print(visited)
    loop_found = False
    def dfs(node):
        nonlocal loop_found
        if visited[node] == 2: return # already traversed in some other graph component
        if visited[node] == 1: 
            loop_found = True # recurring node, ie loop found
            return

        visited[node] = 1 # visited node
        print(f"The node {node} is status:{visited[node]}")
        
        for next in adj[node]:
            dfs(next)
        visited[node] = 2

    for node in list(adj.keys()):
        # print(node)
        dfs(node)
    return loop_found

print(canFinish(numCourses, prerequisites))