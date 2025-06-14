graph = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F'],
    'D': [],
    'E': ['F'],
    'F': []
}

from collections import deque
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

bfs(graph, "B")