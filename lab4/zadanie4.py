from dimacs import *
import os

'''Algorytm znajdowania minimalnego wierzchołkowego pokrycia 
opiera się na fakcie, że jeśli jakiś zbiór wierzchołków tworzy
zbiór niezallezny to pozostałe będę tworzyć właśnie pokrycie wierzchołkowe
No i teraz dość intuicyjny wydaje się fakt że znalezienie minimalnego
pokrycia wierzchiłkowego to tak naprawdę znalezienie. Maksymalnego zioru
wierzchołków niezależnych'''
class Node:
    def __init__(self, idx):
        self.idx = idx
        self.out = set()
    
    def connect_to(self, v):
        self.out.add(v)
    
'''bydowanie grafu z listy krawędzi L i liczby wierzchołków V'''

def bulid_graph(V, L):

    G = [None] + [Node(i) for i in range(1, V + 1)]

    for (u, v, _) in L:
        G[u].connect_to(v)
        G[v].connect_to(u)
    
    return G

def lexbfs(G):
    
    n = len(G) - 1
    visited = [False] * (n+1)

    order = []
    blocks = []
    rest = [i for i in range(2, n + 1)]
    if rest:
        blocks.append(rest)
    blocks.append([1]) # zakładamy, że starujemy algorytm w wierzchołku o indeksie 1

    while blocks:
        
        last_block = blocks[-1]
        v = last_block.pop()

        if visited[v]:
            continue

        visited[v] = True
        order.append(v)
        
        v_neighbours = G[v].out
        new_blocks = []

        for X in blocks:
            Y = []
            K = []
            for x in X:
                if x in v_neighbours:
                    Y.append(x)
                else:
                    K.append(x)
            if K:
                new_blocks.append(K)
            if Y:
                new_blocks.append(Y)
        blocks = new_blocks
    return order

def max_independent_set_chordal(G, order):
    I = set()
    for v in reversed(order):
        ok = True
        for u in G[v].out:
            if u in I:
                ok = False
                break
        if ok:
            I.add(v)
    return I


def min_vertex_cover_from_independent_set(V, L):
    G = bulid_graph(V, L)
    order = lexbfs(G)
    I = max_independent_set_chordal(G, order)
    n = len(G) - 1
    cover = set()
    for v in range(1, n + 1):
        if v not in I:
            cover.add(v)
    return len(cover)

def check_folder(folder):
    flag = True
    for fname in os.listdir(folder):
        path = os.path.join(folder, fname)

        if not os.path.isfile(path):
            continue
        if fname.endswith(".py"):
            continue

        V, L = loadWeightedGraph(path)

        expected = int(readSolution(path))      
        got = int(min_vertex_cover_from_independent_set(V, L))          

        if got != expected:
            print("FAIL:", path, " expected=", expected, " got=", got)
            flag = False

    if flag:
        print("All tests passed")

if __name__ == "__main__":
    check_folder("vcover")

