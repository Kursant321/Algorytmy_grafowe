'''Dla każdego wierzchołka będziemy trzymać odległość max_min_weight[v], czyli największą minimalną wagę jaką da się dostać do v. Następnie robimy coś ala algorytm Dijkstry tylko
na max_heap a nie min_heap'''

from dimacs import *

import heapq

def edges_to_adj_list(V,L):
    G = [[] for _ in range(V + 1)]

    for u, v, w in L:
        G[u].append((v,w))
        G[v].append((u,w))

    return G



def Dijkstra_mod(V, L):

    G = edges_to_adj_list(V, L)

    max_min_dist = [0 for _ in range(V+1)]
    max_min_dist[1] = float("inf")
    visited = [False for _ in range(V+1)]
    max_heap = [(-float("inf"), 1)]

    while max_heap:

        max_min_weight, u = heapq.heappop(max_heap)
        max_min_weight *= -1

        if u == 0 or visited[u]:
            continue

        if u == 2:
            return max_min_weight

        visited[u] = True
        for v, w in G[u]:
            new_weight = min(w, max_min_weight)
            if new_weight > max_min_dist[v]:
                max_min_dist[v] = new_weight
                heapq.heappush(max_heap, (-max_min_dist[v], v))


    return None




# wybierz jeden z plików z folderu graphs-lab1
filename = "graphs-lab1/clique1000"

V, L = loadWeightedGraph(filename)

print(Dijkstra_mod(V, L))






