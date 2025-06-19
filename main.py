import json
import time
import random
import os
import sys
from algo.EX1.dfs import dfs, has_cycle
from algo.EX1.bfs import bfs, connected_components
from algo.EX2.dijkstra import dijkstra, reconstruct_path as reconstruct_dijkstra_path
from algo.EX3.bellman_ford import bellman_ford, reconstruct_path as reconstruct_bf_path
from algo.EX4.ford_fulkerson import ford_fulkerson
from algo.EX4.edmonds_karp import edmonds_karp
from algo.EX5.quicksort import deterministic_quicksort, randomized_quicksort
from algo.EX6.avl import insert, delete, inorder, Node
from algo.EX7.sat import parse_clause, verify_sat, solve_sat_backtrack
from algo.EX7.tsp import nearest_neighbor_tsp, verify_tsp_solution, brute_force_tsp

def clear_screen():
    """Efface l'écran selon l'OS"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """Affiche l'en-tête du programme"""
    print("=" * 60)
    print("         SUITE D'ALGORITHMES - MENU INTERACTIF")
    print("=" * 60)

def print_menu():
    """Affiche le menu principal"""
    print("\n📋 MENU PRINCIPAL")
    print("-" * 30)
    print("1  - DFS (Parcours en profondeur)")
    print("2  - BFS (Parcours en largeur)")
    print("3  - Détection de cycles")
    print("4  - Composantes connexes")
    print("5  - Algorithme de Dijkstra")
    print("6  - Algorithme de Bellman-Ford")
    print("7  - Ford-Fulkerson (Flux maximum)")
    print("8  - Edmonds-Karp (Flux maximum)")
    print("9  - Tri rapide (Quicksort)")
    print("10 - Arbres AVL")
    print("11 - Problème SAT")
    print("12 - Problème TSP")
    print("A  - Exécuter TOUS les algorithmes")
    print("Q  - Quitter")
    print("-" * 30)

def wait_for_key():
    """Attend que l'utilisateur appuie sur une touche"""
    input("\n📍 Appuyez sur Entrée pour continuer...")

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

def test_dfs():
    print("\n🔍 === Test DFS (Parcours en profondeur) ===")
    graphs = load_graphs()
    for gid, graph in graphs.items():
        print(f"\n📊 Graphe: {gid}")
        for start in sorted(graph.keys()):
            print(f"Départ: {start} =>", end=" ")
            t0 = time.perf_counter()
            visited = dfs(graph, start)
            t1 = time.perf_counter()
            print(f"\nSommet(s) visités depuis {start}: {sorted(visited)}")
            print(f"⏱️  Temps DFS({start}): {(t1 - t0) * 1e3:.6f} ms\n")

def test_bfs():
    print("\n🔍 === Test BFS (Parcours en largeur) ===")
    graphs = load_graphs()
    for gid, graph in graphs.items():
        print(f"\n📊 Graphe: {gid}")
        for start in sorted(graph.keys()):
            print(f"Départ: {start} =>", end=" ")
            t0 = time.perf_counter()
            ordre = bfs(graph, start)
            t1 = time.perf_counter()
            print(f"\nSommet(s) visités depuis {start}: {ordre}")
            print(f"⏱️  Temps BFS({start}): {(t1 - t0) * 1e3:.6f} ms\n")

def test_cycle():
    print("\n🔄 === Détection de cycle ===")
    graphs = load_graphs()
    for gid, graph in graphs.items():
        print(f"\n📊 Graphe: {gid}")
        t0 = time.perf_counter()
        cycle = has_cycle(graph)
        t1 = time.perf_counter()
        if cycle:
            print("✅ Cycle détecté")
        else:
            print("❌ Pas de cycle")
        print(f"⏱️  Temps détection: {(t1 - t0) * 1e3:.6f} ms")

def test_connected_components():
    print("\n🔗 === Composantes connexes (BFS) ===")
    graphs = load_graphs()
    for gid, graph in graphs.items():
        print(f"\n📊 Graphe: {gid}")
        t0 = time.perf_counter()
        comps = connected_components(graph)
        t1 = time.perf_counter()
        for idx, comp in enumerate(comps, start=1):
            print(f"Composante {idx}: {sorted(comp)}")
        print(f"⏱️  Temps composants: {(t1 - t0) * 1e3:.6f} ms")

def test_dijkstra():
    print("\n🛣️  === Algorithme de Dijkstra (source = 'A') ===")
    weighted_graph = load_weighted_graph("graphe_dijkstra")
    source = "A"
    t0 = time.perf_counter()
    dist, parent = dijkstra(weighted_graph, source)
    t1 = time.perf_counter()
    print("📏 Distances depuis A :")
    for node in sorted(dist.keys()):
        print(f"  A -> {node} = {dist[node]}")
    print("\n🗺️  Chemins reconstruits depuis A :")
    for node in sorted(parent.keys()):
        path = reconstruct_dijkstra_path(parent, node)
        print(f"  A -> {node} : {'->'.join(path)}")
    print(f"\n⏱️  Temps Dijkstra: {(t1 - t0) * 1e3:.6f} ms")

def test_bellman_ford():
    print("\n🛣️  === Algorithme de Bellman-Ford (source = 'A') ===")
    nodes, edge_list, _ = load_weighted_graph("graphe_bellman")
    source = "A"
    t0 = time.perf_counter()
    dist, parent, has_neg_cycle = bellman_ford(nodes, edge_list, source)
    t1 = time.perf_counter()
    if has_neg_cycle:
        print("⚠️  Cycle de poids négatif détecté dans le graphe.")
    else:
        print("📏 Distances depuis A :")
        for node in sorted(dist.keys()):
            print(f"  A -> {node} = {dist[node]}")
        print("\n🗺️  Chemins reconstruits depuis A :")
        for node in sorted(parent.keys()):
            if dist[node] < float("inf"):
                path = reconstruct_bf_path(parent, node)
                print(f"  A -> {node} : {'->'.join(path)}")
    print(f"\n⏱️  Temps Bellman-Ford: {(t1 - t0) * 1e3:.6f} ms")

def test_ford_fulkerson():
    print("\n💧 === Algorithme de Ford-Fulkerson (A -> F) ===")
    nodes, _, capacity_mat = load_weighted_graph("graphe_flux")
    index_map = {node: idx for idx, node in enumerate(nodes)}
    source = index_map["A"]
    sink = index_map["F"]
    t0 = time.perf_counter()
    max_flow = ford_fulkerson(capacity_mat, source, sink)
    t1 = time.perf_counter()
    print(f"💦 Flux maximum de A vers F = {max_flow}")
    print(f"⏱️  Temps Ford-Fulkerson: {(t1 - t0) * 1e3:.6f} ms")

def test_edmonds_karp():
    print("\n💧 === Algorithme d'Edmonds-Karp (A -> F) ===")
    nodes, _, capacity_mat = load_weighted_graph("graphe_flux")
    index_map = {node: idx for idx, node in enumerate(nodes)}
    source = index_map["A"]
    sink = index_map["F"]
    t0 = time.perf_counter()
    max_flow = edmonds_karp(capacity_mat, source, sink)
    t1 = time.perf_counter()
    print(f"💦 Flux maximum de A vers F = {max_flow}")
    print(f"⏱️  Temps Edmonds-Karp: {(t1 - t0) * 1e3:.6f} ms")

def test_quicksort():
    print("\n⚡ === Tri Rapide : comparaison déterministe vs randomisé ===")
    exemples = [
        [10, 7, 8, 9, 1, 5],
        random.sample(range(1000), 1000),
    ]
    for arr in exemples:
        copie1 = arr[:]
        copie2 = arr[:]
        print(f"\n📋 Tableau initial ({len(arr)} éléments) : {arr if len(arr)<=10 else '...'}")
        t0 = time.perf_counter()
        tri_det = deterministic_quicksort(copie1)
        t1 = time.perf_counter()
        t2 = time.perf_counter()
        tri_rand = randomized_quicksort(copie2)
        t3 = time.perf_counter()
        print(f"⏱️  Tri déterministe (temps): {(t1 - t0) * 1e3:.6f} ms")
        print(f"⏱️  Tri randomisé   (temps): {(t3 - t2) * 1e3:.6f} ms")
        if len(arr) <= 10:
            print(f"✅ Resultat déterministe : {tri_det}")
            print(f"✅ Resultat randomisé    : {tri_rand}")

def test_avl():
    print("\n🌳 === Arbre AVL : insertion, suppression et rééquilibrage ===")
    sequence = [10, 20, 30, 40, 50, 25]
    root = None
    for key in sequence:
        root = insert(root, key)
    result = inorder(root, [])
    print(f"➕ Après insertions {sequence} => Infixe (valeur,hauteur) : {result}")
    print(f"📏 Hauteur de la racine : {root.height}\n")
    to_delete = [40, 30]
    for key in to_delete:
        root = delete(root, key)
        result = inorder(root, [])
        print(f"➖ Après suppression de {key} => Infixe (valeur,hauteur) : {result}")
        print(f"📏 Hauteur de la racine : {root.height}\n")

def test_sat():
    print("\n🧩 === Vérificateur SAT ===")
    clauses_str = [
        "(A ∨ ¬B)",
        "(B ∨ C ∨ ¬D)", 
        "(¬A ∨ D)"
    ]
    
    clauses = [parse_clause(clause) for clause in clauses_str]
    variables = ['A', 'B', 'C', 'D']
    
    print("📝 Clauses:")
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
        print(f"\n🔢 Assignation {i}: {assignment}")
        print(f"{'✅' if result else '❌'} Satisfiable: {result}")
        print(f"⏱️  Temps vérification: {(t1 - t0) * 1e3:.6f} ms")
    
    print("\n🔄 --- Résolution par backtracking ---")
    t0 = time.perf_counter()
    solvable = solve_sat_backtrack(clauses, variables)
    t1 = time.perf_counter()
    print(f"{'✅' if solvable else '❌'} Formule satisfiable: {solvable}")
    print(f"⏱️  Temps résolution: {(t1 - t0) * 1e3:.6f} ms")

def test_tsp():
    print("\n🗺️  === Heuristique TSP (Problème du Voyageur de Commerce) ===")
    distances = [
        [0, 10, 15, 20],
        [10, 0, 35, 25], 
        [15, 35, 0, 30],
        [20, 25, 30, 0]
    ]
    
    cities = ['A', 'B', 'C', 'D']
    print("📊 Matrice des distances:")
    print("    ", "  ".join(f"{city:>3}" for city in cities))
    for i, row in enumerate(distances):
        print(f"{cities[i]:>3} ", "  ".join(f"{dist:>3}" for dist in row))
    
    print("\n🎯 --- Heuristique du plus proche voisin ---")
    t0 = time.perf_counter()
    heuristic_path, heuristic_distance = nearest_neighbor_tsp(distances, 0)
    t1 = time.perf_counter()
    heuristic_path_cities = [cities[i] for i in heuristic_path]
    print(f"🛤️  Chemin heuristique: {' -> '.join(heuristic_path_cities)}")
    print(f"📏 Distance totale: {heuristic_distance}")
    print(f"⏱️  Temps heuristique: {(t1 - t0) * 1e3:.6f} ms")
    
    print(f"\n✅ Vérification solution (distance <= 100): {verify_tsp_solution(distances, heuristic_path, 100)}")
    
    print("\n💪 --- Solution optimale (force brute) ---")
    t0 = time.perf_counter()
    optimal_path, optimal_distance = brute_force_tsp(distances)
    t1 = time.perf_counter()
    optimal_path_cities = [cities[i] for i in optimal_path]
    print(f"🏆 Chemin optimal: {' -> '.join(optimal_path_cities)}")
    print(f"📏 Distance optimale: {optimal_distance}")
    print(f"⏱️  Temps force brute: {(t1 - t0) * 1e3:.6f} ms")
    
    ratio = heuristic_distance / optimal_distance
    print(f"\n📈 Ratio heuristique/optimal: {ratio:.2f}")
    print(f"📊 Écart relatif: {(ratio - 1) * 100:.1f}%")

def run_all_algorithms():
    """Exécute tous les algorithmes"""
    print("\n🚀 === EXÉCUTION DE TOUS LES ALGORITHMES ===")
    print("Vérification des fichiers nécessaires...")
    
    # Vérifier que le fichier matrice.json existe
    if not os.path.exists("matrice.json"):
        print("❌ Erreur: Le fichier 'matrice.json' est introuvable!")
        return
    
    algorithms = [
        ("DFS", test_dfs),
        ("BFS", test_bfs),
        ("Détection de cycles", test_cycle),
        ("Composantes connexes", test_connected_components),
        ("Dijkstra", test_dijkstra),
        ("Bellman-Ford", test_bellman_ford),
        ("Ford-Fulkerson", test_ford_fulkerson),
        ("Edmonds-Karp", test_edmonds_karp),
        ("Tri rapide", test_quicksort),
        ("Arbres AVL", test_avl),
        ("SAT", test_sat),
        ("TSP", test_tsp)
    ]
    
    successful = 0
    failed = 0
    
    for i, (name, func) in enumerate(algorithms, 1):
        print(f"\n🔄 [{i}/{len(algorithms)}] Exécution de: {name}")
        print("─" * 40)
        try:
            func()
            successful += 1
            print(f"✅ {name} terminé avec succès")
        except Exception as e:
            failed += 1
            print(f"❌ Erreur lors de l'exécution de {name}: {e}")
            import traceback
            traceback.print_exc()
        
        if i < len(algorithms):
            print("\n" + "═" * 50)
    
    print(f"\n📊 RÉSUMÉ:")
    print(f"✅ Algorithmes réussis: {successful}")
    print(f"❌ Algorithmes échoués: {failed}")
    print(f"📈 Taux de succès: {(successful/(successful+failed)*100):.1f}%")

def main():
    """Fonction principale avec menu interactif"""
    while True:
        clear_screen()
        print_header()
        print_menu()
        
        try:
            choice = input("\n🎯 Votre choix: ").strip().upper()
            
            if choice == 'Q':
                print("\n👋 Au revoir!")
                sys.exit(0)
            elif choice == 'A':
                run_all_algorithms()
            elif choice == '1':
                test_dfs()
            elif choice == '2':
                test_bfs()
            elif choice == '3':
                test_cycle()
            elif choice == '4':
                test_connected_components()
            elif choice == '5':
                test_dijkstra()
            elif choice == '6':
                test_bellman_ford()
            elif choice == '7':
                test_ford_fulkerson()
            elif choice == '8':
                test_edmonds_karp()
            elif choice == '9':
                test_quicksort()
            elif choice == '10':
                test_avl()
            elif choice == '11':
                test_sat()
            elif choice == '12':
                test_tsp()
            else:
                print("\n❌ Choix invalide! Veuillez entrer un numéro valide, 'A' ou 'Q'.")
                wait_for_key()
                continue
                
            wait_for_key()
            
        except KeyboardInterrupt:
            print("\n\n👋 Au revoir!")
            sys.exit(0)
        except Exception as e:
            print(f"\n❌ Une erreur s'est produite: {e}")
            wait_for_key()

if __name__ == "__main__":
    main()