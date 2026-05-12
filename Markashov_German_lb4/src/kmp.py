def get_prefix_func(s: str) -> list[int]:
    n = len(s)
    pi = [0] * n
    
    print(f"Запускаем префикс-функцию для шаблона: {s}")
    print("Всегда pi[0] = 0")
    
    for i in range(1, n):
        print(f"\nИтерация для индекса i = {i}")
        print(f"Рассматриваем подстроку: \"{s[:i+1]}\"")
        
        j = pi[i-1]
        print(f"Берем значение pi от прошлого элемента: j = pi[{i-1}] = {j}")
        
        while j > 0 and s[i] != s[j]:
            print(f"  Откат: s[{i}]('{s[i]}') != s[{j}]('{s[j]}'), новый j = pi[{j-1}] = {pi[j-1]}")
            j = pi[j-1]
            
        if s[j] == s[i]:
            j += 1
            print(f"  СОВПАДЕНИЕ: s[{i}] == s[{j-1}], увеличиваем j на 1: j = {j}")
        else:
            print(f"  НЕТ СОВПАДЕНИЯ: s[{i}] != s[{j}], j остается {j}")
            
        pi[i] = j
        print(f"  Результат: pi[{i}] = {j}")
        print(f"  Текущий массив pi: {pi[:i+1]}")
    
    print(f"\nИтоговая префикс-функция: {pi}\n" + "="*40)
    return pi

def kmp(text: str, pattern: str) -> list[int]:
    nt = len(text)
    np = len(pattern)
    if np == 0: return []
    
    pi = get_prefix_func(pattern)
    print(f"\nЗапускаем алгоритм КМП")
    print(f"Текст: {text}\nШаблон: {pattern}")
    
    
    res = []
    j = 0
    
    for i in range(nt):
        print(f"\nШаг i={i} (символ текста '{text[i]}')")
        
        while j > 0 and text[i] != pattern[j]:
            print(f"  Элементы не совпали: text[{i}] != pattern[{j}], откат j = pi[{j-1}] = {pi[j-1]}")
            j = pi[j-1]
        
        if text[i] == pattern[j]:
            print(f"  Элементы совпали: text[{i}] == pattern[{j}], j = {j+1}")
            j += 1
        
            if j == np:
                print(f"НАЙДЕНО ВХОЖДЕНИЕ по индексу {i - np + 1}")
                res.append(i - np + 1)
                print(f"  Откатываем j для поиска перекрытий: j = pi[{j-1}] = {pi[j-1]}")
                j = pi[j-1]
        else:
            print(f"  j = 0 и совпадений нет, просто идем к следующему i")
            
    return res

if __name__ == "__main__":
    pattern = input()
    text = input()
    
    result = kmp(text, pattern)
    
    print("\nФИНАЛЬНЫЙ ОТВЕТ:")
    if result:
        print(",".join(map(str, result)))
    else:
        print(-1)