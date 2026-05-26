INF = float("+inf")

def read_data(n: int) -> list[list[float]]:
    matrix = []
    for _ in range(n):
        line = [INF if x == "-1" else float(x) for x in input().split(" ")]
        matrix.append(line)
    return matrix

def matrix_copy(matrix: list[list[float]]) -> list[list[float]]:
    return [row[:] for row in matrix]

def print_matrix(matrix: list[list[float]], title: str = "Матрица"):
    print(f"\n{title}:")
    for i, row in enumerate(matrix):
        row_str = "\t".join(f"{val:>6.2f}" if val != INF else "   inf" for val in row)
        print(f"  Строка {i}: {row_str}")

def reduce_matrix(matrix: list[list[float]]) -> float:
    lower_bound = 0
    n = len(matrix)
    
    print("\nНачинаем редукцию матрицы для вычисления нижней границы")
    
    # вычитаем минимумы из строк
    for i in range(n):
        min_val = min(matrix[i])
        if min_val == 0 or min_val == INF:
            continue
        print(f"  Из строки {i} вычитаем минимальное значение {min_val:.2f}")
        lower_bound += min_val
        for j in range(n):
            if matrix[i][j] != INF:
                matrix[i][j] -= min_val
                
    # вычитаем минимум из столбцов
    for j in range(n):
        min_val = min(matrix[i][j] for i in range(n))
        if min_val == 0 or min_val == INF:
            continue
        print(f"  Из столбца {j} вычитаем минимальное значение {min_val:.2f}")
        lower_bound += min_val
        for i in range(n):
            if matrix[i][j] != INF:
                matrix[i][j] -= min_val
    
    print(f"  Полученная нижняя граница после редукции: {lower_bound:.2f}")
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
        print(f"    Запрещаем ребро из города {from_city} в город {to_city} (ставим бесконечность)")

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
    
    print("  Поиск нуля с максимальной оценкой (штрафом)")
    for i in range(n):
        for j in range(n):
            if matrix[i][j] != 0:
                continue
            penalty = estimate_zero(matrix, n, i, j)
            print(f"    Ноль в позиции ({i}, {j}) имеет штраф {penalty:.2f}")
            if penalty > best_penalty:
                best_penalty = penalty
                best_pos = (i, j)
    
    if best_pos:
        print(f"  Выбран лучший ноль в позиции {best_pos} со штрафом {best_penalty:.2f}")
    else:
        print("  Нули не найдены")
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

def tsp_branch_and_bound(matrix: list[list[float]]):
    n = len(matrix)
    orig = matrix_copy(matrix)
    
    print("ЗАПУСК МЕТОДА ВЕТВЕЙ И ГРАНИЦ ДЛЯ ЗАДАЧИ КОММИВОЯЖЁРА")
    print(f"Количество городов: {n}")
    
    reduced = matrix_copy(matrix)
    start_bound = reduce_matrix(reduced)
    print(f"\nНачальная нижняя граница для всего решения: {start_bound:.2f}")

    rows = list(range(n))
    cols = list(range(n))

    best_cost = INF
    best_path = None
    
    # Счётчик для отладки (ограничим глубину логов)
    recursion_depth = 0
    
    def rec_branch_and_bound(matrix: list[list[float]], rows: list[int], cols: list[int],
                  edges: list[tuple[int, int]], bound: float):
        nonlocal best_cost, best_path, recursion_depth
        
        recursion_depth += 1
        indent = "  " * recursion_depth
        
        print(f"\n{indent}--- Уровень рекурсии {recursion_depth} ---")
        print(f"{indent}Текущая нижняя граница: {bound:.2f}")
        print(f"{indent}Лучшая найденная стоимость на данный момент: {best_cost if best_cost != INF else 'бесконечность'}")
        
        if bound >= best_cost:
            print(f"{indent}Отсекаем ветку: текущая граница {bound:.2f} >= лучшей стоимости {best_cost:.2f}")
            recursion_depth -= 1
            return
        
        if len(matrix) == 1:
            u = rows[0]
            v = cols[0]
            final_edges = edges + [(u, v)]
            path = reconstruct_path(final_edges, n)
            cost = sum(orig[path[i]][path[(i + 1) % n]] for i in range(n))
            
            print(f"\n{indent}Найден полный маршрут! Путь: {path}, стоимость: {cost:.2f}")
            
            if cost < best_cost:
                best_cost = cost
                best_path = path
                print(f"{indent}Обновляем лучшее решение. Новая лучшая стоимость: {best_cost:.2f}")
            recursion_depth -= 1
            return
        
        pos, penalty = find_best_zero(matrix)
        if pos is None:
            print(f"{indent}Нет доступных нулей для ветвления, возвращаемся")
            recursion_depth -= 1
            return
        
        i, j = pos
        u = rows[i]
        v = cols[j]
        
        print(f"\n{indent}Рассматриваем ветвление по ребру из города {u} в город {v}")
        
        force_left = penalty >= INF / 2

        # ветка 1 - не включаем ребро (u, v)
        if not force_left:
            print(f"{indent}Ветка 1: НЕ включаем ребро ({u} -> {v})")
            right_matrix = matrix_copy(matrix)
            right_matrix[i][j] = INF
            right_bound = bound + reduce_matrix(right_matrix)
            print(f"{indent}После редукции новая нижняя граница: {right_bound:.2f}")
            
            rec_branch_and_bound(right_matrix, rows, cols, edges, right_bound)
        else:
            print(f"{indent}Ветка 1 пропущена (штраф слишком велик)")
        
        # ветка 2 - включаем ребро (u, v)
        if not creates_small_cycle(edges, u, v, n):
            print(f"{indent}Ветка 2: ВКЛЮЧАЕМ ребро ({u} -> {v})")
            left_matrix = matrix_copy(matrix)
            start, end = find_chain_endpoints(edges, u, v)
            print(f"{indent}Текущие концы цепи: начало = {start}, конец = {end}")
            
            left_matrix, left_rows, left_cols = remove_row_col(left_matrix, rows, cols, i, j)
            print(f"{indent}Удалили строку {i} и столбец {j} (города {u} и {v})")
            
            forbid_edge(left_matrix, left_rows, left_cols, end, start)
            left_bound = bound + reduce_matrix(left_matrix)
            print(f"{indent}После редукции новая нижняя граница: {left_bound:.2f}")
            
            rec_branch_and_bound(left_matrix, left_rows, left_cols, edges + [(u, v)], left_bound)
        else:
            print(f"{indent}Ветка 2 пропущена (добавление ребра создаст слишком короткий цикл)")
        
        recursion_depth -= 1
    
    rec_branch_and_bound(reduced, rows, cols, [], start_bound)
    
    print("\nРЕЗУЛЬТАТ РАБОТЫ АЛГОРИТМА")
    print(f"Оптимальный маршрут: {best_path}")
    print(f"Длина маршрута: {best_cost:.2f}")
    
    return best_path, best_cost

if __name__ == "__main__":
    n = int(input("Введите количество городов: "))
    print("Введите матрицу расстояний (-1 означает отсутствие ребра):")
    matrix = read_data(n)
    
    path, cost = tsp_branch_and_bound(matrix)
    print("\nФинальный вывод:")
    print(' '.join(map(str, path)))
    print(cost)