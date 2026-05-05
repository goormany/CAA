def lev_dist_prefixes(s1: str, s2: str, mode="префиксов"):
    n, m = len(s1), len(s2)
    prev = list(range(m + 1))
    curr = [0] * (m + 1)
    
    dists = [prev[m]]
    
    print(f"\nРасчет для {mode}")
    print(f"Сравниваем '{s1}' и '{s2}'")
    print(f"Начальное состояние (пустой префикс s1): {prev}")
    
    for i in range(1, n + 1):
        curr[0] = i
        for j in range(1, m + 1):
            if s1[i-1] == s2[j-1]:
                curr[j] = prev[j-1]
            else:
                curr[j] = min(prev[j], curr[j-1], prev[j-1]) + 1
        
        dists.append(curr[m])
        print(f"Шаг {i}: подстрока '{s1[:i]}' -> расстояние до s2 = {curr[m]} | Весь ряд: {curr}")
        
        prev[:] = curr[:]
    
    return dists

def main():
    s1 = input("Введите строку s1 (оригинал): ")
    s2 = input("Введите строку s2 (цель): ")
    n = len(s1)

    # Считаем префиксы
    prefix_dists = lev_dist_prefixes(s1, s2, mode="префиксов")
    min_pref = min(prefix_dists)
    best_prefixes = [s1[:i] for i, d in enumerate(prefix_dists) if d == min_pref]
    
    # Считаем суффиксы (используем реверс)
    s1_rev = s1[::-1]
    s2_rev = s2[::-1]
    suffix_dists_rev = lev_dist_prefixes(s1_rev, s2_rev, mode="суффиксов")
    
    # Разворачиваем результаты обратно
    suffix_dists = [0] * (n + 1)
    for k in range(n + 1):
        suffix_dists[n - k] = suffix_dists_rev[k]

    print("\nИТОГОВЫЙ АНАЛИЗ:")
    print(f"Расстояния для всех префиксов: {prefix_dists}")
    print(f"Минимальное расстояние префикса = {min_pref}")
    print(f"Лучшие префиксы: {best_prefixes}")
    
    print(f"\nРасстояния для всех суффиксов: {suffix_dists}")
    min_suff = min(suffix_dists)
    best_suffixes = [s1[i:] for i, d in enumerate(suffix_dists) if d == min_suff]
    print(f"Минимальное расстояние суффикса = {min_suff}")
    print(f"Лучшие суффиксы: {best_suffixes}")

if __name__ == "__main__":
    main()