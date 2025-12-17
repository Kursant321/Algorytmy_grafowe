from dimacs import *
import os
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

def greedy_coloring(V, L):
    """
    poszukuję liczby chromatycznej grafu przekątniowego
    """
    G = bulid_graph(V, L)
    order = lexbfs(G)
    n = len(G) - 1
    color = [0] * (n + 1)
    chrom = 0
    
    for v in order:
        used = set()
        for u in G[v].out:
            if color[u] != 0:
                used.add(color[u])

        c = 1
        while c in used:
            c += 1

        color[v] = c # sprawdzamy jaki kolor musi mieć v, żeby można go było dodać do sąsiadów
        if c > chrom:
            chrom = c

    return chrom

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
        got = int(greedy_coloring(V, L))          

        if got != expected:
            print("FAIL:", path, " expected=", expected, " got=", got)
            flag = False

    if flag:
        print("All tests passed")

if __name__ == "__main__":
    check_folder("coloring")
