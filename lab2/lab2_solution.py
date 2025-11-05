''' Zaimplementujemy algorytm Forda-Fulkesona przy użyciu listy sąsiedztwa oraz alorytmu DFS do wyszukiwania ścieżek rozszerzających'''

'''Złożoność algorytmu wynosi O(E*f), gdzie f to maksymalny przepływ z wierzchołka s, bo w najgorszym razie algorytm DFS wykona się właśnie f razy'''

from dimacs import *

def edges_to_adj_list(E, V):
    g = [[] for _ in range(V + 1)]
    for u, v, w in E:
        g[u].append({'to': v, 'cap': w, 'rev_idx': len(g[v])}) # (dokąd, krawędź, ile jeszcze jest przepustowości, numer krawędzi w sieci rexydualnej (numer krawędzi wychodzącej z wierzchołka v))
        g[v].append({'to': u, 'cap': 0, 'rev_idx': len(g[u]) - 1})
    return g

def dfs(g, v, t, f, vis):
    if v == t:
        return f
    vis[v] = True
    for e in g[v]:
        if e['cap'] > 0 and not vis[e['to']]:
            pushed = dfs(g, e['to'], t, min(f, e['cap']), vis)
            if pushed:

                e['cap'] -= pushed # zmniejszamy dostępną przepustowość kanału dla krawedzi e
                g[e['to']][e['rev_idx']]['cap'] += pushed # zwiększamy przepływ tą krawędzią w sieci rezydualnej
                return pushed
    return 0

def ford_fulkerson(g, s, t, V):
    flow = 0
    while True:
        vis = [False]*(V+1)
        add = dfs(g, s, t, float('inf'), vis)
        if not add:
            break
        flow += add
    return flow

filename = "flow/rand100_500"

V, E = loadDirectedWeightedGraph(filename)
g = edges_to_adj_list(E, V)
print(ford_fulkerson(g, 1, V, V))
























