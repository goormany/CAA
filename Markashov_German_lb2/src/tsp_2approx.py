import sys

INF = float("+inf")

def read_data() -> tuple[int, list[list[float]]]:
    print("Чтение входных данных")
    lines = sys.stdin.read().strip().split('\n')
    start_vertex = int(lines[0])
    print(f"  Стартовая вершина: {start_vertex}")
    
    matrix = []
    for i in range(1, len(lines)):
        row = []
        for value in map(float, lines[i].split()):
            if value < 0:
                row.append(INF)
            else:
                row.append(value)
        matrix.append(row)
    
    n = len(matrix)
    print(f"  Размер матрицы: {n}x{n}")
    print("  Матрица расстояний загружена")
    return start_vertex, matrix

def create_mst(matrix: list[list[float]], start_vertex_idx: int) -> tuple[list[int], list[float]]:
    n = len(matrix)
    print(f"\nНачинаем построение минимального остовного дерева (алгоритм Прима)")
    print(f"  Стартуем с вершины {start_vertex_idx}")
    
    visited = []
    min_edge = [INF] * n
    parent = [-1] * n
    parent_weight = [0] * n
    
    min_edge[start_vertex_idx] = 0
    
    step = 1
    for _ in range(n):
        u = -1
        best = INF
        
        # Ищем непосещённую вершину с минимальным ребром
        for i in range(n):
            if i not in visited and min_edge[i] < best:
                best = min_edge[i]
                u = i
        
        if u == -1:
            print(f"  Предупреждение: не удалось найти вершину для добавления на шаге {step}")
            break
        
        visited.append(u)
        if parent[u] != -1:
            print(f"  Шаг {step}: добавляем вершину {u} через ребро ({parent[u]} -> {u}) весом {parent_weight[u]:.2f}")
        else:
            print(f"  Шаг {step}: начинаем с вершины {u}")
        
        # Обновляем минимальные рёбра до соседей
        for v in range(n):
            if v not in visited and matrix[u][v] < min_edge[v]:
                min_edge[v] = matrix[u][v]
                parent[v] = u
                parent_weight[v] = matrix[u][v]
        
        step += 1
    
    print(f"\nПостроение MST завершено. Всего добавлено вершин: {len(visited)}")
    
    # Выводим список рёбер MST для наглядности
    print("  Рёбра минимального остовного дерева:")
    for v in range(n):
        p = parent[v]
        if p != -1:
            print(f"    {p} -- {v}  (вес = {parent_weight[v]:.2f})")
    
    total_mst_weight = sum(parent_weight[v] for v in range(n) if parent_weight[v] > 0)
    print(f"  Общий вес минимального остовного дерева: {total_mst_weight:.2f}")
    
    return parent, parent_weight

def build_adjacency(parent: list[int], parent_weight: list[float]) -> list[list[tuple[int, float]]]:
    print("\nСтроим список смежности для обхода дерева")
    n = len(parent)
    adj = [[] for _ in range(n)]
    for v in range(n):
        p = parent[v]
        if p != -1:
            w = parent_weight[v]
            adj[p].append((v, w))
            adj[v].append((p, w))
    
    print("  Список смежности построен")
    for i, neighbors in enumerate(adj):
        if neighbors:
            neighbors_str = ", ".join(f"{nbr}({w:.2f})" for nbr, w in neighbors)
            print(f"    Вершина {i}: {neighbors_str}")
    
    return adj

def dfs_preorder(adj: list[list[tuple[int, float]]], start: int) -> list[int]:
    print(f"\nВыполняем обход дерева в глубину (DFS), начиная с вершины {start}")
    visited = []
    path = []
    
    def dfs(v: int):
        visited.append(v)
        path.append(v)
        print(f"    Посещаем вершину {v}")
        
        # Сортируем соседей по весу для детерминированного порядка
        for neighbor, weight in sorted(adj[v], key=lambda x: (x[1], x[0])):
            if neighbor not in visited:
                print(f"      Переходим из {v} в {neighbor} (вес ребра = {weight:.2f})")
                dfs(neighbor)
    
    dfs(start)
    
    print(f"\nПорядок обхода вершин (без возврата к старту): {path}")
    return path

def path_len(path: list[int], matrix: list[list[float]]) -> float:
    total = 0
    print("\nВычисляем длину полученного маршрута:")
    for i in range(len(path) - 1):
        edge_weight = matrix[path[i]][path[i+1]]
        total += edge_weight
        print(f"  {path[i]} -> {path[i+1]}: {edge_weight:.2f} (накоплено: {total:.2f})")
    return total

def analyze_approximation(optimal_cost_estimate: float, our_cost: float) -> None:
    """Анализирует качество приближения (теоретическая оценка)"""
    ratio = our_cost / optimal_cost_estimate if optimal_cost_estimate > 0 else 0
    print("\nАНАЛИЗ КАЧЕСТВА ПРИБЛИЖЕНИЯ")
    print(f"Вес минимального остовного дерева (MST): {optimal_cost_estimate:.2f}")
    print(f"Длина полученного маршрута: {our_cost:.2f}")
    print(f"Теоретическая нижняя граница оптимального маршрута: не меньше {optimal_cost_estimate:.2f}")
    print(f"Коэффициент приближения = {our_cost:.2f} / {optimal_cost_estimate:.2f} = {ratio:.2f}")

if __name__ == "__main__":
    print("\nПРИБЛИЖЁННЫЙ АЛГОРИТМ КОММИВОЯЖЁРА (ЧЕРЕЗ MST)")
    print("Теоретическая гарантия: найденный путь ≤ 2 × оптимальный")
    
    start_vertex_idx, matrix = read_data()
    
    print("\nЭТАП 1: ПОСТРОЕНИЕ МИНИМАЛЬНОГО ОСТОВНОГО ДЕРЕВА")
    parent, parent_weight = create_mst(matrix, start_vertex_idx)
    
    print("\nЭТАП 2: ПРЕОБРАЗОВАНИЕ ДЕРЕВА В ГАМИЛЬТОНОВ ЦИКЛ")
    adj = build_adjacency(parent, parent_weight)
    
    print("\nЭТАП 3: ОБХОД ДЕРЕВА В ГЛУБИНУ (ПОЛУЧЕНИЕ МАРШРУТА)")
    path = dfs_preorder(adj, start_vertex_idx)
    
    # Замыкаем цикл: возвращаемся в стартовую вершину
    print(f"\nЗамыкаем маршрут: возвращаемся из {path[-1]} в {start_vertex_idx}")
    path.append(start_vertex_idx)
    
    print("\nЭТАП 4: ВЫЧИСЛЕНИЕ ДЛИНЫ МАРШРУТА")
    length = path_len(path, matrix)
    
    print("\nИТОГОВЫЙ РЕЗУЛЬТАТ")
    print(f"Длина маршрута: {length:.2f}")
    print(f"Порядок обхода городов: {' -> '.join(map(str, path))}")
    
    # Теоретический анализ (сравнение с весом MST как нижней границей)
    total_mst_weight = sum(parent_weight[v] for v in range(len(parent)) if parent_weight[v] > 0)
    analyze_approximation(total_mst_weight, length)
    
    # Вывод в требуемом формате
    print("\nВЫВОД В ТРЕБУЕМОМ ФОРМАТЕ")
    print(f"{length:.2f}")
    print(" ".join(list(map(str, path))))