import sys

INF = float("+inf")

def read_data(n: int) -> list[list[float]]:
    matrix = []
    for _ in range(n):
        line = [INF if x == "-1" else float(x) for x in input().split(" ")]
        matrix.append(line)
    print("Матрица загружена")
    return matrix

def matrix_copy(matrix: list[list[float]]) -> list[list[float]]:
    return [row[:] for row in matrix]

def reduce_matrix(matrix: list[list[float]]) -> float:
    lower_bound = 0
    n = len(matrix)
    
    print("  Приведение матрицы...")
    
    # вычитаем минимум из строк
    for i in range(n):
        min_val = min(matrix[i])
        if min_val == 0 or min_val == INF:
            continue
        lower_bound += min_val
        print(f"    Строка {i}: вычитаем {min_val:.2f}")
        for j in range(n):
            if matrix[i][j] != INF:
                matrix[i][j] -= min_val
                
    # вычитаем минимум из столбцов
    for j in range(n):
        min_val = min(matrix[i][j] for i in range(n))
        if min_val == 0 or min_val == INF:
            continue
        lower_bound += min_val
        print(f"    Столбец {j}: вычитаем {min_val:.2f}")
        for i in range(n):
            if matrix[i][j] != INF:
                matrix[i][j] -= min_val
    
    print(f"  Нижняя граница после приведения: {lower_bound:.2f}")
    return lower_bound

def remove_row_col(matrix: list[list[float]], rows: list[int], cols: list[int],
                   row_idx: int, col_idx: int) -> tuple[list[list[float]], list[int], list[int]]:
    n = len(matrix)
    new_matrix = []
    new_rows = []
    new_cols = []
    
    for i in range(n):
        new_row = []
        if i != row_idx:
            for j in range(n):
                if j != col_idx:
                    new_row.append(matrix[i][j])
            new_matrix.append(new_row)
            new_rows.append(rows[i])

    for j in range(n):
        if j != col_idx:
            new_cols.append(cols[j])
    
    return new_matrix, new_rows, new_cols

def forbid_edge(matrix: list[list[float]], rows: list[int], cols: list[int],
                from_city: int, to_city: int) -> None:
    n = len(matrix)
    row_idx = col_idx = -1
    
    for i in range(n):
        if rows[i] == from_city:
            row_idx = i
            break
    
    for j in range(n):
        if cols[j] == to_city:
            col_idx = j
            break
        
    if row_idx != -1 and col_idx != -1:
        matrix[row_idx][col_idx] = INF
        print(f"    Запрещаем обратное ребро {from_city}->{to_city}")

def estimate_zero(matrix: list[list[float]], n: int, i: int, j: int) -> float:
    row_min = INF
    for k in range(n):
        if k != j and matrix[i][k] != INF:
            row_min = min(row_min, matrix[i][k])
    if row_min == INF:
        row_min = 0

    col_min = INF
    for k in range(n):
        if k != i and matrix[k][j] != INF:
            col_min = min(col_min, matrix[k][j])
    if col_min == INF:
        col_min = 0
    
    return row_min + col_min

def find_best_zero(matrix: list[list[float]]) -> tuple[tuple[int, int] | None, float]:
    n = len(matrix)
    best_pos = None
    best_penalty = -1
    
    for i in range(n):
        for j in range(n):
            if matrix[i][j] != 0:
                continue
            penalty = estimate_zero(matrix, n, i, j)
            if penalty > best_penalty:
                best_penalty = penalty
                best_pos = (i, j)
    
    if best_pos:
        print(f"  Лучший ноль: ({best_pos[0]},{best_pos[1]}) со штрафом {best_penalty:.2f}")
    return best_pos, best_penalty

def reconstruct_path(edges: list[tuple[int, int]], n: int) -> list[int]:
    next_map = {u: v for u, v in edges}
    
    path = [0]
    cur = 0
    
    for _ in range(n - 1):
        cur = next_map[cur]
        path.append(cur)
    
    return path

def find_chain_endpoints(edges: list[tuple[int, int]], u: int, v: int) -> tuple[int, int]:
    next_map = {}
    prev_map = {}
    
    for a, b in edges:
        next_map[a] = b
        prev_map[b] = a
    
    next_map[u] = v
    prev_map[v] = u
    
    # Ищем начало
    start = u
    while start in prev_map:
        start = prev_map[start]
    
    # Ищем конец
    end = v
    while end in next_map:
        end = next_map[end]
    
    return start, end

def creates_small_cycle(edges: list[tuple[int, int]], u: int, v: int, total_n: int) -> bool:
    next_map = {a: b for a, b in edges}
    next_map[u] = v
    
    cur = v
    length = 1
    
    while cur in next_map:
        cur = next_map[cur]
        length += 1
        if cur == u:
            return length < total_n
    
    return False

def print_matrix(matrix: list[list[float]]):
    n = len(matrix)
    for i in range(n):
        row_str = []
        for j in range(n):
            val = matrix[i][j]
            if val == INF:
                row_str.append(" INF")
            else:
                row_str.append(f"{val:6.2f}")
        print("    " + " ".join(row_str))

def tsp_branch_and_bound(matrix: list[list[float]]):
    print("АЛГОРИТМ ВЕТВЕЙ И ГРАНИЦ ДЛЯ ЗАДАЧИ КОММИВОЯЖЁРА")
    
    n = len(matrix)
    orig = matrix_copy(matrix)
    
    reduced = matrix_copy(matrix)
    start_bound = reduce_matrix(reduced)
    print(f"\nНачальная нижняя граница: {start_bound:.2f}\n")

    rows = list(range(n))
    cols = list(range(n))

    best_cost = INF
    best_path = None
    
    def rec_branch_and_bound(matrix: list[list[float]], rows: list[int], cols: list[int],
                  edges: list[tuple[int, int]], bound: float):
        nonlocal best_cost, best_path
        
        if bound >= best_cost:
            print("Отсечение: нижняя граница >= лучшему решению")
            return

        print(f"Текущие рёбра: {edges}")
        print(f"Нижняя граница: {bound:.2f}")
        print("Матрица:")
        print_matrix(matrix)
        
        if len(matrix) == 1:
            print("Достигнута матрица 1x1!")
            u = rows[0]
            v = cols[0]
            final_edges = edges + [(u, v)]
            path = reconstruct_path(final_edges, n)
            cost = sum(orig[path[i]][path[(i + 1) % n]] for i in range(n))
            print(f"  Полный путь: {path}")
            print(f"  Стоимость: {cost:.2f}")
            
            if cost < best_cost:
                print(f"Найдено новое лучшее решение! Было: {best_cost:.2f}, стало: {cost:.2f}")
                best_cost = cost
                best_path = path
            return
        
        pos, penalty = find_best_zero(matrix)
        if pos is None:
            print("Нет доступных нулей, возврат")
            return
        
        i, j = pos
        u = rows[i]
        v = cols[j]
        
        force_left = penalty >= INF / 2

        # ветка 1 - не включаем ребро (u, v)
        if not force_left:
            print(f"\nВЕТКА 1 (исключаем ребро {u}→{v})")
            right_matrix = matrix_copy(matrix)
            right_matrix[i][j] = INF
            right_bound = bound + reduce_matrix(right_matrix)
            
            rec_branch_and_bound(right_matrix, rows, cols, edges, right_bound)
        
        # ветка 2 - включаем ребро (u, v)
        if not creates_small_cycle(edges, u, v, n):
            print(f"\nВЕТКА 2 (включаем ребро {u}→{v})")
            left_matrix = matrix_copy(matrix)
            start, end = find_chain_endpoints(edges, u, v)
            left_matrix, left_rows, left_cols = remove_row_col(left_matrix, rows, cols, i, j)
            forbid_edge(left_matrix, left_rows, left_cols, end, start)
            left_bound = bound + reduce_matrix(left_matrix)
            
            rec_branch_and_bound(left_matrix, left_rows, left_cols, edges + [(u, v)], left_bound)
        else:
            print(f"Ребро {u}→{v} создаст преждевременный цикл, пропускаем")
    
    rec_branch_and_bound(reduced, rows, cols, [], start_bound)
    
    print("РЕЗУЛЬТАТ АЛГОРИТМА:")
    print(f"Оптимальный маршрут: {best_path}")
    print(f"Минимальная стоимость: {best_cost:.2f}")
    
    return best_path, best_cost

if __name__ == "__main__":
    n = int(input())
    matrix = read_data(n)
    
    path, cost = tsp_branch_and_bound(matrix)
    print(' '.join(map(str, path)))
    print(f"{cost:.2f}")