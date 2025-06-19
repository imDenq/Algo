def nearest_neighbor_tsp(distances, start=0):
    n = len(distances)
    unvisited = set(range(n))
    path = [start]
    unvisited.remove(start)
    total_distance = 0
    
    current = start
    while unvisited:
        nearest = min(unvisited, key=lambda city: distances[current][city])
        path.append(nearest)
        total_distance += distances[current][nearest]
        current = nearest
        unvisited.remove(nearest)
    
    total_distance += distances[current][start]
    path.append(start)
    return path, total_distance

def verify_tsp_solution(distances, path, max_distance):
    if len(path) < 2:
        return False
    
    total_distance = 0
    for i in range(len(path) - 1):
        total_distance += distances[path[i]][path[i + 1]]
    
    return total_distance <= max_distance

def brute_force_tsp(distances):
    from itertools import permutations
    n = len(distances)
    min_distance = float('inf')
    best_path = None
    
    for perm in permutations(range(1, n)):
        path = [0] + list(perm) + [0]
        distance = 0
        for i in range(len(path) - 1):
            distance += distances[path[i]][path[i + 1]]
        
        if distance < min_distance:
            min_distance = distance
            best_path = path
    
    return best_path, min_distance