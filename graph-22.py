# Whats a bipartite graph?
# Representing Graphs (Adjacency Graph, O(V^2) space and time complexity)
# Adjacency List, Edge List - good for sparse graphs, inefficient for dense graphs

# Common Graph Theory Problems:
# - Shortest path Problem (BFS, Dijkstra, Bellman-Ford, Floyd-Warshall, A*, ...)
# - Connectivity, does there exist a path between Node A and Node B? (Union-Find, any search algorithm like DFS/BFS)
# - Negative Cycle, does my digraph have negative cycle (Bellman-Ford, Floyd-Warshall)
# - Strongly Connected Components (Tarjan's, Kosaraju's) similar to connectivity but for digraph
# - Travelling Salesman Problem, NP-Hard
# - Bridges/Cut Edge
# - Articulation Point/Cut vertex
# - Minimum Spanning Tree (Kruskal's, Prim's, Boruvka's)
# - Network Flow: max flow ()

# Depth First Search
'''
n = number of nodes in graph
graph = adj list 
visited = [false, ..., false]
 
function dfs(node):
    if visited[node]: return 
    visited[node] = true

    # process, some kind of computation

    neighbors = graph[node]
    for next in neighbors:
        dfs(next)

start_node = 0
dfs(start_node)
'''

# Q. How can you use DFS to identify connected components?
# Try to write the code by yourself

# Breadth First Search
# shortest path on an *unweighted* graph
'''
n = number of nodes in the graph
g = adjacency list

function shortest_path(start, end):
    # start BFS at start node
    prev = bfs(start) 
    # return reconstructed path from start -> end node 
    return reconstructPath(start, end, prev)

function bfs(node):
    q = queue with enqueue and dequeue 
    q.enqueue(node)

    visited = [false, ..., false] # size of n
    visited[node] = true

    # tracks who the parent of node is
    prev = [null, ..., null] # size of n

    while !q.isEmpty():
        node = q.dequeue()
        neighbors = g.get(node)

        for (next : neighbors):
            if !visited[next]:
                q.enqueue(next)
                visited[next] = true
                prev[next] = node
    return prev
'''

# BFS on grid
# 1. convert the grid to a familiar format like adjacency list/matrix


