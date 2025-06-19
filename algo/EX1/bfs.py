def bfs(graph, start):
    visited = set()
    queue = [start]
    ordre = []
    while queue:
        u = queue.pop(0)
        if u not in visited:
            visited.add(u)
            ordre.append(u)
            print(u, end=" ")
            for voisin in sorted(graph[u]):
                if voisin not in visited:
                    queue.append(voisin)
    return ordre

def connected_components(graph):
    visited = set()
    components = []
    for node in sorted(graph.keys()):
        if node not in visited:
            comp = []
            queue = [node]
            while queue:
                u = queue.pop(0)
                if u not in visited:
                    visited.add(u)
                    comp.append(u)
                    for v in graph[u]:
                        if v not in visited:
                            queue.append(v)
            components.append(comp)
    return components
