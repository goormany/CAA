def lev_dist(s1: str, s2: str, cost_replace: int, cost_insert: int, cost_delete: int) -> int:
    n, m = len(s1), len(s2)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    
    # Заполнение базовых случаев (первый столбец и строка)
    for i in range(n + 1):
        dp[i][0] = i * cost_delete
    for j in range(m + 1):
        dp[0][j] = j * cost_insert
        
    print(f"\n[Конфигурация] Замена: {cost_replace}, Вставка: {cost_insert}, Удаление: {cost_delete}")
    print(f"[Старт] Сравниваем '{s1}' -> '{s2}'\n")

    for i in range(1, n + 1):
        print(f"Обработка символа '{s1[i-1]}':")
        for j in range(1, m + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
                print(f"  - '{s1[i-1]}' == '{s2[j-1]}': Совпадение (0)")
            else:
                # Считаем стоимость каждого варианта
                val_del = dp[i-1][j] + cost_delete
                val_ins = dp[i][j-1] + cost_insert
                val_rep = dp[i-1][j-1] + cost_replace
                
                res = min(val_del, val_ins, val_rep)
                dp[i][j] = res
                
                # Показываем, что было выбрано
                op = "Замена" if res == val_rep else ("Удаление" if res == val_del else "Вставка")
                print(f"  - '{s1[i-1]}' != '{s2[j-1]}': Выбрано {op} ({res})")
        
        print_matrix(dp, s1, s2)
        print()

    return dp[n][m]

def print_matrix(matrix, s1, s2):
    header = "  " + "  ".join(list(s2))
    print("    " + header)
    for i, row in enumerate(matrix):
        char = s1[i-1] if i > 0 else " "
        print(f"{char} {row}")

def main():
    c_replace, c_insert, c_delete = list(map(int, input("Введите через пробел стоимости (Замена Вставка Удаление): ").split(" ")))

    s1 = input("Введите строку s1: ")
    s2 = input("Введите строку s2: ")
    
    final_cost = lev_dist(s1, s2, c_replace, c_insert, c_delete)
    print(f"\nИТОГОВАЯ СТОИМОСТЬ ТРАНСФОРМАЦИИ: {final_cost}")

if __name__ == "__main__":
    main()