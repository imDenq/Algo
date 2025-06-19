def bellman_ford(nodes, edge_list, source):
    dist = {u: float("inf") for u in nodes}
    dist[source] = 0
    parent = {u: None for u in nodes}
    n = len(nodes)
    for _ in range(n - 1):
        updated = False
        for u, v, w_uv in edge_list:
            if dist[u] + w_uv < dist[v]:
                dist[v] = dist[u] + w_uv
                parent[v] = u
                updated = True
        if not updated:
            break
    for u, v, w_uv in edge_list:
        if dist[u] + w_uv < dist[v]:
            return None, None, True
    return dist, parent, False

def reconstruct_path(parent, target):
    path = []
    u = target
    while u is not None:
        path.append(u)
        u = parent[u]
    return list(reversed(path))
