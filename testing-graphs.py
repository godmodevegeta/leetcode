from collections import deque, defaultdict
from typing import List


tickets = [["MUC","LHR"],["JFK","MUC"],["SFO","SJC"],["LHR","SFO"]]
def findItinerary(tickets: List[List[str]]) -> List[str]:
    