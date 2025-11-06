''' Zaimplementujemy algorytm Forda-Fulkesona przy użyciu listy sąsiedztwa oraz alorytmu DFS do wyszukiwania ścieżek rozszerzających'''

'''Złożoność algorytmu wynosi O(E*f), gdzie f to maksymalny przepływ z wierzchołka s, bo w najgorszym razie algorytm DFS wykona się właśnie f razy'''

from dimacs import *


def build_graph(E, V):
    g = [[] for _ in range(V + 1)]
    for u, v, w in E:
        g[u].append([v, w, len(g[v])])   # [wierzchołek do którego prowadzi krawędź, przepustowość, indeks krawędzi odwrotnej]
        g[v].append([u, 0, len(g[u]) - 1])
    return g

def dfs(g, v, t, flow, vis):
    if v == t:
        return flow
    vis[v] = True
    for e in g[v]:
        u, cap, rev = e
        if cap > 0 and not vis[u]:
            pushed = dfs(g, u, t, min(flow, cap), vis)
            if pushed:
                e[1] -= pushed
                g[u][rev][1] += pushed
                return pushed
    return 0

def ford_fulkerson(E, V, s, t):
    g = build_graph(E, V)
    max_flow = 0
    while True:
        vis = [False] * (V + 1)
        pushed = dfs(g, s, t, float('inf'), vis)
        if not pushed:
            break
        max_flow += pushed
    return max_flow


filename = "flow/rand20_100"

V, E = loadDirectedWeightedGraph(filename)
print(ford_fulkerson(E, V, 1, V))