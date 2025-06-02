import heapq

def dijkstra(graph, source):
    dist = {node: float("inf") for node in graph}
    dist[source] = 0
    parent = {node: None for node in graph}
    pq = [(0, source)]
    visited = set()
    while pq:
        d_u, u = heapq.heappop(pq)
        if u in visited:
            continue
        visited.add(u)
        for v, w_uv in graph[u]:
            if dist[u] + w_uv < dist[v]:
                dist[v] = dist[u] + w_uv
                parent[v] = u
                heapq.heappush(pq, (dist[v], v))
    return dist, parent

def reconstruct_path(parent, target):
    path = []
    u = target
    while u is not None:
        path.append(u)
        u = parent[u]
    return list(reversed(path))
