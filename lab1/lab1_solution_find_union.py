'''Łączymy krawędzie od tych o największej wadze, po każdym połączeniu sprawdzamy czy istanieje połączenie poniędzy wierzchołkami 1 oraz 2.
Jeśli istanieje no to zwracamy wartość ostatnio dodanej krawędzi. Ponieważ łączymy od największych krawędzi to napewno wykryjemy optymlane rozwiązanie '''


from dimacs import *

class Node:
    def __init__(self, val):
        self.parent = self
        self.val = val
        self.rank = 0

def find(x):

    if x != x.parent:
        x.parent = find(x.parent)

    return x.parent

def union(x, y):

    x_root = find(x)
    y_root = find(y)

    if x_root.rank > y_root.rank:
        y_root.parent = x_root

    else:

        if x_root.rank == y_root.rank:
            y_root.rank += 1

        x_root.parent = y_root

def edges_decreasing(E):
    E.sort(key = lambda x: x[2], reverse = True)
    return E

def solution(V, L):

    Nodes = [Node(i) for i in range(V+1)]

    L_sorted = edges_decreasing(L)
    max_min_weight = 0
    for u, v, w in L_sorted:
        union(Nodes[u], Nodes[v])
        if find(Nodes[1]) == find(Nodes[2]):
            return w




# wybierz jeden z plików z folderu graphs-lab1
filename = "graphs-lab1/g1"

V, L = loadWeightedGraph(filename)

print(solution(V, L))