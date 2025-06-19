def dfs(graph, start, visited=None):
    if visited is None:
        visited = set()
    visited.add(start)
    print(start, end=" ")
    for voisin in sorted(graph[start]):
        if voisin not in visited:
            dfs(graph, voisin, visited)
    return visited

def has_cycle(graph):
    visited = set()
    def _dfs(u, parent):
        visited.add(u)
        for v in graph[u]:
            if v not in visited:
                if _dfs(v, u):
                    return True
            elif v != parent:
                return True
        return False
    for node in sorted(graph.keys()):
        if node not in visited:
            if _dfs(node, None):
                return True
    return False
