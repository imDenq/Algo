from collections import deque

def edmonds_karp(capacity_matrix, source, sink):
    n = len(capacity_matrix)
    parent = [-1] * n

    def bfs(residual, s, t):
        visited = [False] * n
        queue = deque()
        queue.append(s)
        visited[s] = True
        parent[:] = [-1] * n
        while queue:
            u = queue.popleft()
            for v in range(n):
                if not visited[v] and residual[u][v] > 0:
                    queue.append(v)
                    visited[v] = True
                    parent[v] = u
                    if v == t:
                        return True
        return False

    residual = [row[:] for row in capacity_matrix]
    max_flow = 0

    while bfs(residual, source, sink):
        path_flow = float("inf")
        v = sink
        while v != source:
            u = parent[v]
            path_flow = min(path_flow, residual[u][v])
            v = u
        v = sink
        while v != source:
            u = parent[v]
            residual[u][v] -= path_flow
            residual[v][u] += path_flow
            v = u
        max_flow += path_flow

    return max_flow
