import sys

INF = float("+inf")

def read_data() -> list[list[float]]:
    print("Чтение входных данных...")
    lines = sys.stdin.read().strip().split('\n')
    start_vertex = int(lines[0])
    print(f"Стартовая вершина: {start_vertex}")
    
    matrix = []
    for i in range(1, len(lines)):
        row = []
        for value in map(float, lines[i].split()):
            if value < 0:
                row.append(INF)
            else:
                row.append(value)
        matrix.append(row)
    
    print(f"Матрица размером {len(matrix)}x{len(matrix)} загружена")
    return start_vertex, matrix

def create_mst(matrix: list[list[float]], start_vertex_idx: int) -> tuple[list[int], list[float]]:
    print(f"\nПостроение минимального остовного дерева (алгоритм Прима)")
    print(f"Начинаем с вершины {start_vertex_idx}")
    
    n = len(matrix)
    visited = []
    min_edge = [INF] * n
    parent = [-1] * n
    parent_weight = [0] * n
    
    min_edge[start_vertex_idx] = 0
    
    for iteration in range(n):
        u = -1
        best = INF
        
        for i in range(n):
            if i not in visited and min_edge[i] < best:
                best = min_edge[i]
                u = i
        
        if u == -1:
            print(f"  Итерация {iteration}: не найдено подходящих вершин, прерывание")
            break
        
        visited.append(u)
        print(f"  Итерация {iteration}: добавляем вершину {u} (вес ребра: {best:.2f})")
        
        for v in range(n):
            if v not in visited and matrix[u][v] < min_edge[v]:
                min_edge[v] = matrix[u][v]
                parent[v] = u
                parent_weight[v] = matrix[u][v]
                print(f"    Обновляем ребро {u}->{v}: новый вес {matrix[u][v]:.2f}")

    print(f"Остовное дерево построено. Добавлено вершин: {len(visited)}")
    return parent, parent_weight
                            

def build_adjacency(parent: list[int], parent_weight: list[float]) -> list[list[tuple[int, float]]]:
    print("\nПостроение списка смежности...")
    n = len(parent)
    adj = [[] for _ in range(n)]
    edge_count = 0
    
    for v in range(n):
        p = parent[v]
        if p != -1:
            w = parent_weight[v]
            adj[p].append((v, w))
            adj[v].append((p, w))
            print(f"  Добавлено ребро {p}--{v} весом {w:.2f}")
            edge_count += 1
    
    print(f"Список смежности построен. Рёбер в дереве: {edge_count}")
    return adj

def dfs_preorder(adj: list[list[tuple[int, float]]], start: int) -> list[int]:
    print(f"\nОбход дерева в глубину (прямой порядок) с вершины {start}...")
    visited = []
    path = []
    
    def dfs(v: int, depth: int = 0):
        visited.append(v)
        path.append(v)
        indent = "  " * depth
        print(f"{indent}Посещаем вершину {v}")
        
        for neighbor, weight in sorted(adj[v], key=lambda x: (x[1], x[0])):
            if neighbor not in visited:
                print(f"{indent}  Переход {v} -> {neighbor} (вес {weight:.2f})")
                dfs(neighbor, depth + 1)
        
    dfs(start)
    print(f"Обход завершён. Порядок обхода: {path}")
    return path

def path_len(path: list[int], matrix: list[list[float]]):
    print(f"\nВычисление длины гамильтонова цикла...")
    total = 0
    print(f"Путь: {path}")
    
    for i in range(len(path) - 1):
        edge_weight = matrix[path[i]][path[i+1]]
        total += edge_weight
        print(f"  {path[i]} -> {path[i+1]}: +{edge_weight:.2f} = {total:.2f}")
    
    print(f"Итоговая длина цикла: {total:.2f}")
    return total

if __name__ == "__main__":
    start_vertex_idx, matrix = read_data()
    print(f"\nСтартовая вершина index: {start_vertex_idx}")
    
    parent, parent_weight = create_mst(matrix, start_vertex_idx)
    adj = build_adjacency(parent, parent_weight)
    path = dfs_preorder(adj, start_vertex_idx)
    path.append(start_vertex_idx)
    print(f"\nГамильтонов цикл (с возвратом в начало): {path}")
    
    l = path_len(path, matrix)
    
    print(f"Длина цикла: {l:.2f}")
    print(f"Маршрут: {' -> '.join(map(str, path))}")
    
    print(f"\n{l:.2f}")
    print(" ".join(list(map(str, path))))