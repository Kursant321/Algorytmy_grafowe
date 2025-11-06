'''Złożoność O(V*E^2) = liczba iteracji * koszt BFS, każde wykonanie algorytmu Edmondsa Karpa dla danej długości "zapelnia nam jedną krawędź maksynalnie będzie więc (E)
zapełnień a mamy V różnych długości"'''

from collections import deque

from dimacs import *

def build_graph(E, V): # tworzymy sieć rezydualną
    g = [[] for _ in range(V + 1)]
    for u, v, w in E:
        g[u].append([v, w, len(g[v])]) # (wierzchołek do którego prowadzi krawędź, przepustowość krawędzi, numer krawędzi w sieci rezydualnej dla tego wierzchołka)
        g[v].append([u, 0, len(g[u]) - 1])
    return g

def bfs(g, s, t, parent):
    for i in range(len(parent)):
        parent[i] = (-1, -1)
    parent[s] = (s, -1)

    q = deque([s])
    while q:
        v = q.popleft()
        for idx, (to, cap, _) in enumerate(g[v]):
            if cap > 0 and parent[to][0] == -1:
                parent[to] = (v, idx)
                if to == t:
                    return True
                q.append(to)
    return False

def edmonds_karp(E, V, s, t):
    g = build_graph(E, V)
    parent = [(-1, -1)] * (V + 1)
    max_flow = 0

    while bfs(g, s, t, parent):
        # znajdujemy najmniejszą przepustowość na ścieżce rozszerzającej o najkrótszej długości
        min_cap = float('inf')
        v = t
        while v != s:
            u, idx = parent[v]
            min_cap = min(min_cap, g[u][idx][1])
            v = u
        # aktualizuje przepływy
        v = t
        while v != s:
            u, idx = parent[v]
            to, cap, rev = g[u][idx]
            g[u][idx][1] -= min_cap
            g[v][rev][1] += min_cap
            v = u
        max_flow += min_cap

    return max_flow

filename = "flow/grid100x100"

V, E = loadDirectedWeightedGraph(filename)
print(edmonds_karp(E,V,1,V))