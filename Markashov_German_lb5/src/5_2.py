class Vertex:
    def __init__(self, id: int, parent, pchar: str, alpha: int = 5):
        self.id = id
        self.next = [None] * alpha
        self.parent = parent
        self.pchar = pchar
        self.sufflink = None
        self.dict_link = None
        self.go = [None] * alpha
        self.substring_data = []  # (стартовая позиция l_i, длина)
        
    def __str__(self) -> str:
        return f"id: {self.id}"
    
    def __repr__(self):
        return self.__str__()
    
def num(c):
    return "ACGTN".index(c)

class Trie:
    def __init__(self, alpha: int = 5, verbose: bool = False):
        self.alpha = alpha
        self.verbose = verbose
        self.vertices = [Vertex(0, None, None, self.alpha)]
        self.root = self.vertices[0]
    
    def size(self) -> int:
        return len(self.vertices)
    
    def last(self) -> Vertex:
        return self.vertices[-1]
    
    def add(self, s: str, l_i: int):
        if self.verbose:
            print(f"Добавление подстроки '{s}' (начало в шаблоне: {l_i})")
        v = self.root
        for char in s:
            c_idx = num(char)
            if v.next[c_idx] is None:
                self.vertices.append(Vertex(self.size(), v, char, self.alpha))
                v.next[c_idx] = self.last()
                if self.verbose:
                    print(f"  Создан узел {self.last().id} для символа '{char}'")
            v = v.next[c_idx]
        v.substring_data.append((l_i, len(s)))
        if self.verbose:
            print(f"  Узел {v.id} хранит данные: ({l_i}, {len(s)})")
    
    def get_link(self, v: Vertex) -> Vertex:
        if v.sufflink is None:
            if v == self.root or v.parent == self.root:
                v.sufflink = self.root
                if self.verbose and v != self.root:
                    print(f"  Суффиксная ссылка узла {v.id} -> корень")
            else:
                if self.verbose:
                    print(f"  Вычисление суффиксной ссылки для узла {v.id}")
                v.sufflink = self.go(self.get_link(v.parent), v.pchar)
                if self.verbose:
                    print(f"    Суффиксная ссылка узла {v.id} -> узел {v.sufflink.id}")
        return v.sufflink
    
    def get_dict_link(self, v: Vertex) -> Vertex:
        if v.dict_link is None:
            link = self.get_link(v)
            if link == self.root:
                v.dict_link = link
            elif link.substring_data:
                v.dict_link = link
                if self.verbose:
                    print(f"    Сжатая ссылка узла {v.id} -> узел {link.id} (имеет данные)")
            else:
                v.dict_link = self.get_dict_link(link)
        return v.dict_link
    
    def go(self, v: Vertex, char: str) -> Vertex:
        c_idx = num(char)
        if v.go[c_idx] is None:
            if v.next[c_idx] is not None:
                v.go[c_idx] = v.next[c_idx]
            elif v == self.root:
                v.go[c_idx] = self.root
            else:
                v.go[c_idx] = self.go(self.get_link(v), char)
        return v.go[c_idx]

if __name__ == "__main__":
    text = input("Текст: ")
    pattern = input("Шаблон: ")
    wildcard = input("Wildcard символ: ")
    
    print(f"\nТекст: '{text}'")
    print(f"Шаблон: '{pattern}'")
    print(f"Wildcard: '{wildcard}'\n")
    
    t = Trie(verbose=True)
    
    k = 0
    cur_part = []
    
    print("--- Разбор шаблона на подстроки ---")
    for i, char in enumerate(pattern):
        if char == wildcard:
            if cur_part:
                l_i = i - len(cur_part) + 1
                print(f"Найдена подстрока '{''.join(cur_part)}' (позиции {l_i}-{i} в шаблоне, 1-индексация)")
                t.add("".join(cur_part), l_i)
                k += 1
                cur_part = []
        else:
            cur_part.append(char)
    
    if cur_part:
        l_i = len(pattern) - len(cur_part) + 1
        print(f"Найдена подстрока '{''.join(cur_part)}' (позиции {l_i}-{len(pattern)} в шаблоне)")
        t.add("".join(cur_part), l_i)
        k += 1
    
    print(f"\nВсего подстрок (k) = {k}")
    
    C = [0] * (len(text) + 2)
    
    print("\n--- Проход по тексту ---")
    v = t.root
    for i, char in enumerate(text):
        print(f"\nПозиция {i+1} в тексте, символ '{char}':")
        v = t.go(v, char)
        print(f"  Переход в узел {v.id}")
        
        tmp = v
        while tmp != t.root:
            if tmp.substring_data:
                for l_i, length in tmp.substring_data:
                    j = i - length + 2
                    start_pos = j - l_i + 1
                    if start_pos >= 1 and start_pos + len(pattern) - 1 <= len(text):
                        C[start_pos] += 1
                        print(f"  Найдена подстрока длиной {length} в тексте на позициях [{j}..{i+1}]")
                        print(f"    Это соответствует {l_i}-й позиции в шаблоне")
                        print(f"    Гипотетическое начало шаблона: позиция {start_pos}, счетчик -> {C[start_pos]}")
            tmp = t.get_dict_link(tmp)
            if tmp != t.root and tmp.substring_data:
                print(f"  Переход по сжатой ссылке к узлу {tmp.id}")
    
    print("\n--- Результат ---")
    results = []
    for i in range(1, len(text) + 1):
        if C[i] == k:
            results.append(str(i))
            print(f"Позиция {i}: все {k} подстрок совпали")
        elif C[i] > 0:
            print(f"Позиция {i}: совпало {C[i]} из {k} подстрок")
    
    if results:
        print(f"\nНайденные стартовые позиции:")
        print("\n".join(results))
    else:
        print("Совпадений не найдено")