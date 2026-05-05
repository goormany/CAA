def lev_dist(s1: str, s2: str) -> int:
    n, m = len(s1), len(s2)
    # Создаем матрицу
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    
    # Инициализация границ
    for i in range(n + 1):
        dp[i][0] = i
    for j in range(m + 1):
        dp[0][j] = j
        
    print(f"Сравниваем '{s1}' и '{s2}'")
    print(f"Начальная матрица (базовые правки):")
    print_matrix(dp, s1, s2)

    for i in range(1, n + 1):
        print(f"\nОбработка символа '{s1[i-1]}' (строка {i})")
        for j in range(1, m + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
                print(f"  Символы '{s1[i-1]}' == '{s2[j-1]}' совпали. Копируем диагональ: {dp[i][j]}")
            else:
                res = min(
                    dp[i-1][j] + 1,    # удаление
                    dp[i][j-1] + 1,    # вставка
                    dp[i-1][j-1] + 1   # замена
                )
                dp[i][j] = res
                print(f"  Символы '{s1[i-1]}' != '{s2[j-1]}'. Минимум из соседей + 1: {dp[i][j]}")
        
        print_matrix(dp, s1, s2)
        
    return dp[n][m]

def print_matrix(matrix, s1, s2):
    header = "  " + "  ".join(list(s2))
    print("    " + header)
    for i, row in enumerate(matrix):
        char = s1[i-1] if i > 0 else " "
        print(f"{char} {row}")

def main():
    s1 = input("Введите первую строку: ")
    s2 = input("Введите вторую строку: ")
    
    final_dist = lev_dist(s1, s2)
    print(f"\nИтоговое расстояние Левенштейна: {final_dist}")

if __name__ == "__main__":
    main()