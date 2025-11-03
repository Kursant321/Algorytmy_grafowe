from collections import deque

from dimacs import *

def edges_to_adj_list(E, V):
    g = [[] for _ in range(V + 1)]
    for u, v, w in E:
        g[u].append({'to': v, 'cap': w, 'rev': len(g[v])})
        g[v].append({'to': u, 'cap': 0, 'rev': len(g[u]) - 1})
    return g

def bfs(g, s, t, parent):

    for i in range(len(parent)):
        parent[i] = (-1, -1)
    parent[s] = (s, -1)

    q = deque([s])
    while q:
        v = q.popleft()
        for idx, e in enumerate(g[v]):
            if e['cap'] > 0 and parent[e['to']][0] == -1:
                parent[e['to']] = (v, idx)
                if e['to'] == t:
                    return True
                q.append(e['to'])
    return False


def edmonds_karp(E, V, s, t):
    g = edges_to_adj_list(E, V)
    parent = [(-1, -1)]*(V+1)
    flow = 0

    while bfs(g, s, t, parent):
        bottleneck = float('inf')
        v = t
        while v != s:
            u, idx = parent[v]
            bottleneck = min(bottleneck, g[u][idx]['cap'])
            v = u
        v = t
        while v != s:
            u, idx = parent[v]
            rev = g[u][idx]['rev']
            g[u][idx]['cap']       -= bottleneck
            g[v][rev]['cap'] += bottleneck
            v = u
        flow += bottleneck
    return flow

filename = "flow/rand100_500"

V, E = loadWeightedGraph(filename)
print(edmonds_karp(E,V,1,V))