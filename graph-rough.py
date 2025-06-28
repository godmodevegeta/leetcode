from collections import deque
graph = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F'],
    'D': [],
    'E': ['F'],
    'F': []
}

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