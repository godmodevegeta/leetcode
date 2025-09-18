from collections import deque, defaultdict
from typing import List
import heapq


tickets = [["MUC","LHR"],["JFK","MUC"],["SFO","SJC"],["LHR","SFO"]]
def findItinerary(tickets: List[List[str]]) -> List[str]:
    graph = defaultdict(list)
    for _from, _to in tickets:
        heapq.heappush(graph[_from], _to)
    visited = set()
    path = []
    def dfs(node):
        if node in visited: return
        visited.add(node)
        
    dfs("JFK")
    return path

# print(findItinerary(tickets))