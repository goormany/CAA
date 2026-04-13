import sys

INF = float("+inf")

def read_data() -> list[list[float]]:
    lines = sys.stdin.read().strip().split('\n')
    start_vertex = int(lines[0])
    
    matrix = []
    for i in range(1, len(lines)):
        row = []
        for value in map(float, lines[i].split()):
            if value < 0:
                row.append(INF)
            else:
                row.append(value)
        matrix.append(row)
    
    return start_vertex, matrix

def create_mst(matrix: list[list[float]], start_vertex_idx: int) -> tuple[list[int], list[float]]:
    n = len(matrix)
    vistited = []
    min_edge = [INF] * n
    parent = [-1] * n
    parent_weight = [0] * n
    
    min_edge[start_vertex_idx] = 0
    
    for _ in range(n):
        u = -1
        best = INF
        
        for i in range(n):
            if i not in vistited and min_edge[i] < best:
                best = min_edge[i]
                u = i
        
        if u == -1:
            break
        
        vistited.append(u)
        
        for v in range(n):
            if v not in vistited and matrix[u][v] < min_edge[v]:
                min_edge[v] = matrix[u][v]
                parent[v] = u
                parent_weight[v] = matrix[u][v]

    return parent, parent_weight
                            

def build_adjacency(parent: list[int], parent_weight: list[float]) -> list[list[tuple[int, float]]]:
    n = len(parent)
    adj = [[] for _ in range(n)]
    for v in range(n):
        p = parent[v]
        if p != -1:
            w = parent_weight[v]
            adj[p].append((v, w))
            adj[v].append((p, w))
    return adj

def dfs_preorder(adj: list[list[tuple[int, float]]], start: int) -> list[int]:
    visited = []
    path = []
    
    def dfs(v: int):
        visited.append(v)
        path.append(v)
        
        for neighbor, weight in sorted(adj[v], key=lambda x: (x[1], x[0])):
            if neighbor not in visited:
                dfs(neighbor)
        
    dfs(start)
    return path

def path_len(path: list[int], matrix: list[list[float]]):
    total = 0
    for i in range(len(path) - 1):
        total += matrix[path[i]][path[i+1]]
    return total

if __name__ == "__main__":
    start_vertex_idx, matrix = read_data()
    
    parent, parent_weight = create_mst(matrix, start_vertex_idx)
    adj = build_adjacency(parent, parent_weight)
    path = dfs_preorder(adj, start_vertex_idx)
    path.append(start_vertex_idx)
    
    l = path_len(path, matrix)
    
    print(f"{l:.2f}")
    print(" ".join(list(map(str, path))))