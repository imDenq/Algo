import json
import time
import random
from algo.dfs import dfs, has_cycle
from algo.bfs import bfs, connected_components
from algo.dijkstra import dijkstra, reconstruct_path as reconstruct_dijkstra_path
from algo.bellman_ford import bellman_ford, reconstruct_path as reconstruct_bf_path
from algo.ford_fulkerson import ford_fulkerson
from algo.edmonds_karp import edmonds_karp
from algo.quicksort import deterministic_quicksort, randomized_quicksort
from algo.avl import insert, delete, inorder, Node
from algo.sat import parse_clause, verify_sat, solve_sat_backtrack
from algo.tsp import nearest_neighbor_tsp, verify_tsp_solution, brute_force_tsp

def load_graphs():
    with open("matrice.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    graphs = {}
    for g in data["graphs"]:
        if g["id"] in ["graphe1", "graph_cycle"]:
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

def load_weighted_graph(graph_id):
    with open("matrice.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    for g in data["graphs"]:
        if g["id"] == graph_id:
            nodes = g["nodes"]
            mat = g["matrix"]
            nlen = len(nodes)
            adj = {n: [] for n in nodes}
            edge_list = []
            for i in range(nlen):
                for j in range(nlen):
                    w = mat[i][j]
                    if w != 0:
                        u = nodes[i]
                        v = nodes[j]
                        if graph_id == "graphe_dijkstra":
                            adj[u].append((v, w))
                        else:
                            edge_list.append((u, v, w))
                        if graph_id == "graphe_dijkstra" and i != j:
                            adj[v].append((u, w))
            if graph_id == "graphe_dijkstra":
                return adj
            else:
                return nodes, edge_list, mat
    return None

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

def test_dijkstra_algo():
    print("=== Algorithme de Dijkstra (source = 'A') ===")
    weighted_graph = load_weighted_graph("graphe_dijkstra")
    source = "A"
    t0 = time.perf_counter()
    dist, parent = dijkstra(weighted_graph, source)
    t1 = time.perf_counter()
    print("Distances depuis A :")
    for node in sorted(dist.keys()):
        print(f"  A -> {node} = {dist[node]}")
    print("\nChemins reconstruits depuis A :")
    for node in sorted(parent.keys()):
        path = reconstruct_dijkstra_path(parent, node)
        print(f"  A -> {node} : {'->'.join(path)}")
    print(f"\nTemps Dijkstra: {(t1 - t0) * 1e3:.6f} ms\n")

def test_bellman_ford_algo():
    print("=== Algorithme de Bellman-Ford (source = 'A') ===")
    nodes, edge_list, _ = load_weighted_graph("graphe_bellman")
    source = "A"
    t0 = time.perf_counter()
    dist, parent, has_neg_cycle = bellman_ford(nodes, edge_list, source)
    t1 = time.perf_counter()
    if has_neg_cycle:
        print("Cycle de poids négatif détecté dans le graphe.")
    else:
        print("Distances depuis A :")
        for node in sorted(dist.keys()):
            print(f"  A -> {node} = {dist[node]}")
        print("\nChemins reconstruits depuis A :")
        for node in sorted(parent.keys()):
            if dist[node] < float("inf"):
                path = reconstruct_bf_path(parent, node)
                print(f"  A -> {node} : {'->'.join(path)}")
    print(f"\nTemps Bellman-Ford: {(t1 - t0) * 1e3:.6f} ms\n")

def test_ford_fulkerson_algo():
    print("=== Algorithme de Ford-Fulkerson (A -> F) ===")
    nodes, _, capacity_mat = load_weighted_graph("graphe_flux")
    index_map = {node: idx for idx, node in enumerate(nodes)}
    source = index_map["A"]
    sink = index_map["F"]
    t0 = time.perf_counter()
    max_flow = ford_fulkerson(capacity_mat, source, sink)
    t1 = time.perf_counter()
    print(f"Flux maximum de A vers F = {max_flow}")
    print(f"Temps Ford-Fulkerson: {(t1 - t0) * 1e3:.6f} ms\n")

def test_edmonds_karp_algo():
    print("=== Algorithme d'Edmonds-Karp (A -> F) ===")
    nodes, _, capacity_mat = load_weighted_graph("graphe_flux")
    index_map = {node: idx for idx, node in enumerate(nodes)}
    source = index_map["A"]
    sink = index_map["F"]
    t0 = time.perf_counter()
    max_flow = edmonds_karp(capacity_mat, source, sink)
    t1 = time.perf_counter()
    print(f"Flux maximum de A vers F = {max_flow}")
    print(f"Temps Edmonds-Karp: {(t1 - t0) * 1e3:.6f} ms\n")

def test_quicksort():
    print("=== Tri Rapide : comparaison déterministe vs randomisé ===")
    exemples = [
        [10, 7, 8, 9, 1, 5],
        random.sample(range(1000), 1000),
    ]
    for arr in exemples:
        copie1 = arr[:]
        copie2 = arr[:]
        print(f"\nTableau initial ({len(arr)} éléments) : {arr if len(arr)<=10 else '...'}")
        t0 = time.perf_counter()
        tri_det = deterministic_quicksort(copie1)
        t1 = time.perf_counter()
        t2 = time.perf_counter()
        tri_rand = randomized_quicksort(copie2)
        t3 = time.perf_counter()
        print(f"Tri déterministe (temps): {(t1 - t0) * 1e3:.6f} ms")
        print(f"Tri randomisé   (temps): {(t3 - t2) * 1e3:.6f} ms")
        if len(arr) <= 10:
            print(f"Resultat déterministe : {tri_det}")
            print(f"Resultat randomisé    : {tri_rand}")

def test_avl():
    print("=== Arbre AVL : insertion, suppression et rééquilibrage ===")
    sequence = [10, 20, 30, 40, 50, 25]
    root = None
    for key in sequence:
        root = insert(root, key)
    result = inorder(root, [])
    print(f"Après insertions {sequence} => Infixe (valeur,hauteur) : {result}")
    print(f"Hauteur de la racine : {root.height}\n")
    to_delete = [40, 30]
    for key in to_delete:
        root = delete(root, key)
        result = inorder(root, [])
        print(f"Après suppression de {key} => Infixe (valeur,hauteur) : {result}")
        print(f"Hauteur de la racine : {root.height}\n")

def test_sat():
    print("=== Vérificateur SAT ===")
    clauses_str = [
        "(A ∨ ¬B)",
        "(B ∨ C ∨ ¬D)", 
        "(¬A ∨ D)"
    ]
    
    clauses = [parse_clause(clause) for clause in clauses_str]
    variables = ['A', 'B', 'C', 'D']
    
    print("Clauses:")
    for i, clause_str in enumerate(clauses_str, 1):
        print(f"  {i}: {clause_str}")
    
    assignment_examples = [
        {'A': True, 'B': False, 'C': True, 'D': True},
        {'A': False, 'B': True, 'C': False, 'D': False},
        {'A': True, 'B': True, 'C': True, 'D': False}
    ]
    
    for i, assignment in enumerate(assignment_examples, 1):
        t0 = time.perf_counter()
        result = verify_sat(clauses, assignment)
        t1 = time.perf_counter()
        print(f"\nAssignation {i}: {assignment}")
        print(f"Satisfiable: {result}")
        print(f"Temps vérification: {(t1 - t0) * 1e3:.6f} ms")
    
    print("\n--- Résolution par backtracking ---")
    t0 = time.perf_counter()
    solvable = solve_sat_backtrack(clauses, variables)
    t1 = time.perf_counter()
    print(f"Formule satisfiable: {solvable}")
    print(f"Temps résolution: {(t1 - t0) * 1e3:.6f} ms\n")

def test_tsp():
    print("=== Heuristique TSP (Problème du Voyageur de Commerce) ===")
    distances = [
        [0, 10, 15, 20],
        [10, 0, 35, 25], 
        [15, 35, 0, 30],
        [20, 25, 30, 0]
    ]
    
    cities = ['A', 'B', 'C', 'D']
    print("Matrice des distances:")
    print("    ", "  ".join(f"{city:>3}" for city in cities))
    for i, row in enumerate(distances):
        print(f"{cities[i]:>3} ", "  ".join(f"{dist:>3}" for dist in row))
    
    print("\n--- Heuristique du plus proche voisin ---")
    t0 = time.perf_counter()
    heuristic_path, heuristic_distance = nearest_neighbor_tsp(distances, 0)
    t1 = time.perf_counter()
    heuristic_path_cities = [cities[i] for i in heuristic_path]
    print(f"Chemin heuristique: {' -> '.join(heuristic_path_cities)}")
    print(f"Distance totale: {heuristic_distance}")
    print(f"Temps heuristique: {(t1 - t0) * 1e3:.6f} ms")
    
    print(f"\nVérification solution (distance <= 100): {verify_tsp_solution(distances, heuristic_path, 100)}")
    
    print("\n--- Solution optimale (force brute) ---")
    t0 = time.perf_counter()
    optimal_path, optimal_distance = brute_force_tsp(distances)
    t1 = time.perf_counter()
    optimal_path_cities = [cities[i] for i in optimal_path]
    print(f"Chemin optimal: {' -> '.join(optimal_path_cities)}")
    print(f"Distance optimale: {optimal_distance}")
    print(f"Temps force brute: {(t1 - t0) * 1e3:.6f} ms")
    
    ratio = heuristic_distance / optimal_distance
    print(f"\nRatio heuristique/optimal: {ratio:.2f}")
    print(f"Écart relatif: {(ratio - 1) * 100:.1f}%\n")

def main():
    graphs = load_graphs()
    for gid, graph in graphs.items():
        print(f"\n***** Graphe non pondéré: {gid} *****\n")
        test_dfs(graph)
        test_bfs(graph)
        test_cycle(graph)
        test_connected_components(graph)

    print("\n***** Graphe pondéré pour Dijkstra *****\n")
    test_dijkstra_algo()

    print("\n***** Graphe pondéré pour Bellman-Ford *****\n")
    test_bellman_ford_algo()

    print("\n***** Réseau de capacités pour Ford-Fulkerson *****\n")
    test_ford_fulkerson_algo()

    print("\n***** Réseau de capacités pour Edmonds-Karp *****\n")
    test_edmonds_karp_algo()

    print("\n***** Exercice 5 : Tri Rapide Randomisé et Déterministe *****\n")
    test_quicksort()

    print("\n***** Exercice 6 : Arbres AVL *****\n")
    test_avl()

    print("\n***** Exercice 7 : Problèmes NP-complets et NP-difficiles *****\n")
    test_sat()
    test_tsp()

if __name__ == "__main__":
    main()