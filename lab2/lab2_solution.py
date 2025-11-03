''' Zaimplementujemy algorytm Forda-Fulkesona przy użyciu listy sąsiedztwa oraz alorytmu BFS do wyszukiwania ścieżek rozszerzających'''

from dimacs import *

def edges_to_adj_list(E, V):
    g = [[] for _ in range(V + 1)]
    for u, v, w in E:
        g[u].append({'to': v, 'cap': w, 'rev': len(g[v])})
        g[v].append({'to': u, 'cap': 0, 'rev': len(g[u]) - 1})
    return g

def dfs(g, v, t, f, vis):
    if v == t:
        return f
    vis[v] = True
    for e in g[v]:
        if e['cap'] > 0 and not vis[e['to']]:
            pushed = dfs(g, e['to'], t, min(f, e['cap']), vis)
            if pushed:

                e['cap'] -= pushed
                g[e['to']][e['rev']]['cap'] += pushed
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

filename = "flow/grid100x100"

V, E = loadWeightedGraph(filename)
g = edges_to_adj_list(E, V)
print(ford_fulkerson(g, 1, V, V))
























