import json
import time
from algo.dfs import dfs, has_cycle
from algo.bfs import bfs, connected_components

def load_graphs():
    with open("matrice.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    graphs = {}
    for g in data["graphs"]:
        nodes = g["nodes"]
        mat = g["matrix"]
        adj = {n: set() for n in nodes}
        nlen = len(nodes)
        for i in range(nlen):
            for j in range(nlen):
                if mat[i][j] == 1:
                    adj[nodes[i]].add(nodes[j])
        graphs[g["id"]] = adj
    return graphs

def test_dfs(graph):
    print("=== Test DFS pour chaque sommet comme départ ===")
    for start in sorted(graph.keys()):
        print(f"Départ: {start} =>", end=" ")
        t0 = time.perf_counter()
        visited = dfs(graph, start)
        t1 = time.perf_counter()
        print(f"\nSommet(s) visités depuis {start}: {sorted(visited)}")
        print(f"Temps DFS({start}): {(t1 - t0) * 1e3:.6f} ms\n")

def test_bfs(graph):
    print("=== Test BFS pour chaque sommet comme départ ===")
    for start in sorted(graph.keys()):
        print(f"Départ: {start} =>", end=" ")
        t0 = time.perf_counter()
        ordre = bfs(graph, start)
        t1 = time.perf_counter()
        print(f"\nSommet(s) visités depuis {start}: {ordre}")
        print(f"Temps BFS({start}): {(t1 - t0) * 1e3:.6f} ms\n")

def test_cycle(graph):
    print("=== Détection de cycle ===")
    t0 = time.perf_counter()
    cycle = has_cycle(graph)
    t1 = time.perf_counter()
    if cycle:
        print("Cycle détecté")
    else:
        print("Pas de cycle")
    print(f"Temps détection: {(t1 - t0) * 1e3:.6f} ms\n")

def test_connected_components(graph):
    print("=== Composantes connexes (BFS) ===")
    t0 = time.perf_counter()
    comps = connected_components(graph)
    t1 = time.perf_counter()
    for idx, comp in enumerate(comps, start=1):
        print(f"Composante {idx}: {sorted(comp)}")
    print(f"Temps composants: {(t1 - t0) * 1e3:.6f} ms\n")

def main():
    graphs = load_graphs()
    for gid, graph in graphs.items():
        print(f"\n***** Graphe: {gid} *****\n")
        test_dfs(graph)
        test_bfs(graph)
        test_cycle(graph)
        test_connected_components(graph)

if __name__ == "__main__":
    main()
