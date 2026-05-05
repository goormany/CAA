def lev_dist(s1: str, s2: str, cost_replace: int, cost_insert: int, cost_delete: int) -> list:
    n, m = len(s1), len(s2)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    
    # Заполнение таблицы
    for i in range(n + 1):
        dp[i][0] = i * cost_delete
    for j in range(m + 1):
        dp[0][j] = j * cost_insert
        
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = min(
                    dp[i-1][j] + cost_delete,
                    dp[i][j-1] + cost_insert,
                    dp[i-1][j-1] + cost_replace
                )

    print("\nРезультирующая матрица стоимостей")
    print_matrix(dp, s1, s2)

    # Восстановление пути (Backtracking)
    print("\nВосстановление пути (обратный ход)")
    i, j = n, m
    ops = []

    while i > 0 or j > 0:
        current_val = dp[i][j]
        # Проверяем совпадение
        if i > 0 and j > 0 and s1[i - 1] == s2[j - 1]:
            print(f"[{i}][{j}] Символы '{s1[i-1]}' совпали -> Идем по диагонали (M)")
            ops.append('M')
            i -= 1
            j -= 1
        # Проверяем замену
        elif i > 0 and j > 0 and current_val == dp[i - 1][j - 1] + cost_replace:
            print(f"[{i}][{j}] Выгодна замена '{s1[i-1]}' на '{s2[j-1]}' -> По диагонали (R)")
            ops.append('R')
            i -= 1
            j -= 1
        # Проверяем удаление
        elif i > 0 and current_val == dp[i - 1][j] + cost_delete:
            print(f"[{i}][{j}] Выгодно удалить '{s1[i-1]}' -> Идем вверх (D)")
            ops.append('D')
            i -= 1
        # Проверяем вставку
        elif j > 0 and current_val == dp[i][j - 1] + cost_insert:
            print(f"[{i}][{j}] Выгодно вставить '{s2[j-1]}' -> Идем влево (I)")
            ops.append('I')
            j -= 1

    ops.reverse()
    return ops

def print_matrix(matrix, s1, s2):
    header = "  " + "  ".join(list(s2))
    print("    " + header)
    for i, row in enumerate(matrix):
        char = s1[i-1] if i > 0 else " "
        print(f"{char} {row}")

def main():
    c_rep, c_ins, c_del = list(map(int, input("Введите веса (замена вставка удаление) через пробел (например: 1 1 1): ").split(" ")))

    s1 = input("Введите строку s1: ")
    s2 = input("Введите строку s2: ")
    
    path = lev_dist(s1, s2, c_rep, c_ins, c_del)
    

    print(f"\nИТОГОВАЯ ПОСЛЕДОВАТЕЛЬНОСТЬ: {''.join(path)}")
    print(f"Оригинал: {s1}")
    print(f"Цель: {s2}")

if __name__ == "__main__":
    main()