
'''Złożoność O(V*E^2) = liczba iteracji * koszt BFS, każde wykonanie algorytmu Edmondsa Karpa dla danej długości "zapelnia nam jedną krawędź maksynalnie będzie więc (E)
zapełnień a mamy V różnych długości"'''

from collections import deque

from dimacs import *

def edges_to_adj_list(E, V):
    g = [[] for _ in range(V + 1)]
    for u, v, w in E:
        g[u].append({'to': v, 'cap': w, 'rev': len(g[v])}) # rev to numer krawędzi w sieci rezydualnej dla danego u lub v
        g[v].append({'to': u, 'cap': 0, 'rev': len(g[u]) - 1})
    return g

def bfs(g, s, t, parent): # szukamy BFS-em najkrótszej ścieżki, która jest ścieżką rozszerzającą

    for i in range(len(parent)):
        parent[i] = (-1, -1)
    parent[s] = (s, -1)

    q = deque([s])
    while q:
        v = q.popleft()
        for idx, e in enumerate(g[v]):
            if e['cap'] > 0 and parent[e['to']][0] == -1: # jeżeli jest jeszzce jakaś przepustowość na tej ścieżce
                parent[e['to']] = (v, idx)
                if e['to'] == t:
                    return True
                q.append(e['to'])
    return False


def edmonds_karp(E, V, s, t):
    g = edges_to_adj_list(E, V)
    parent = [(-1, -1)]*(V+1)
    flow = 0

    while bfs(g, s, t, parent): # dopóki istanieje jakś ścieżka rozszerzająca
        bottleneck = float('inf')
        v = t
        while v != s:
            u, idx = parent[v]
            bottleneck = min(bottleneck, g[u][idx]['cap']) # szukamy najmniejszej przepustowości na tej ścieżce
            v = u
        v = t
        while v != s:
            u, idx = parent[v]
            rev = g[u][idx]['rev']
            g[u][idx]['cap']       -= bottleneck # zmienjszamy przepustowość na każdej krawędzi ścieżki rozszerzającej
            g[v][rev]['cap'] += bottleneck # w krawędzi odwrotnej zapisujemy ile "popłynie tą krawędzią"
            v = u
        flow += bottleneck
    return flow

filename = "flow/pp100"

V, E = loadWeightedGraph(filename)
print(edmonds_karp(E,V,1,V))