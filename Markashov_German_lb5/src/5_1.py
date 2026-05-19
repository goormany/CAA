class Vertex:
    def __init__(self, id: int, parent, pchar: str, alpha=5):
        self.id = id
        self.next = [None] * alpha
        self.parent = parent
        self.pchar = pchar
        self.sufflink = None
        self.dict_link = None
        self.go = [None] * alpha
        self.pattern_ids = []
    
    def __str__(self) -> str:
        return f"id: {self.id}"
    
    def __repr__(self):
        return self.__str__()

def num(c):
    return "ACGTN".index(c)

class Trie:
    def __init__(self, alpha=5, verbose=False):
        self.alpha = alpha
        self.verbose = verbose
        self.vertices = [Vertex(0, None, None, alpha)]
        self.root = self.vertices[0]
        if self.verbose:
            print(f"Создан корневой узел {self.root.id}")
    
    def size(self):
        return len(self.vertices)
    
    def last(self):
        return self.vertices[-1]
    
    def add(self, s: str, pattern_id: int):
        if self.verbose:
            print(f"Добавление шаблона #{pattern_id + 1}: '{s}'")
        v = self.root
        for idx, char in enumerate(s):
            c_idx = num(char)
            if v.next[c_idx] is None:
                self.vertices.append(Vertex(self.size(), v, char, self.alpha))
                v.next[c_idx] = self.last()
                if self.verbose:
                    print(f"  Создан узел {self.last().id} (символ '{char}', родитель {v.id})")
            v = v.next[c_idx]
        v.pattern_ids.append(pattern_id)
        if self.verbose:
            print(f"  Узел {v.id} помечен как терминальный для шаблона #{pattern_id + 1}")
    
    def get_link(self, v: Vertex) -> Vertex:
        if v.sufflink is None:
            if v == self.root or v.parent == self.root:
                v.sufflink = self.root
                if self.verbose and v != self.root:
                    print(f"  Суффиксная ссылка узла {v.id} ('{v.pchar}') -> корень")
            else:
                if self.verbose:
                    print(f"  Вычисление суффиксной ссылки для узла {v.id} ('{v.pchar}')")
                v.sufflink = self.go(self.get_link(v.parent), v.pchar)
                if self.verbose:
                    print(f"    Суффиксная ссылка узла {v.id} -> узел {v.sufflink.id}")
        return v.sufflink
    
    def get_dict_link(self, v: Vertex) -> Vertex:
        if v.dict_link is None:
            link = self.get_link(v)
            if link == self.root:
                v.dict_link = self.root
            elif link.pattern_ids:
                v.dict_link = link
                if self.verbose:
                    print(f"    Сжатая ссылка узла {v.id} -> терминальный узел {link.id}")
            else:
                v.dict_link = self.get_dict_link(link)
        return v.dict_link
                
    def go(self, v: Vertex, c: str) -> Vertex:
        c_idx = num(c)
        if v.go[c_idx] is None:
            if v.next[c_idx] is not None:
                v.go[c_idx] = v.next[c_idx]
            elif v == self.root:
                v.go[c_idx] = self.root
            else:
                v.go[c_idx] = self.go(self.get_link(v), c)
        return v.go[c_idx]

if __name__ == "__main__":
    text = input("Введите текст: ")
    n = int(input("Введите количество шаблонов: "))
    
    print(f"\nТекст: '{text}'")
    print(f"Шаблонов: {n}\n")
    
    t = Trie(verbose=True)
    pattern_len = [0] * (n + 1)
    
    print("--- Построение бора ---")
    for i in range(1, n + 1):
        p = input(f"Шаблон #{i}: ")
        pattern_len[i-1] = len(p)
        t.add(p, i-1)
    
    print("\n--- Поиск вхождений ---")
    results = []
    v = t.root
    
    for i, char in enumerate(text):
        print(f"\nПозиция {i+1}, символ '{char}':")
        v = t.go(v, char)
        print(f"  Переход в узел {v.id}")
        
        tmp = v
        while tmp != t.root:
            if tmp.pattern_ids:
                for p_id in tmp.pattern_ids:
                    start_pos = i - pattern_len[p_id] + 2
                    results.append((start_pos, p_id + 1))
                    print(f"  Найдено совпадение: шаблон #{p_id + 1} (длина {pattern_len[p_id]}) заканчивается в узле {tmp.id}, начальная позиция {start_pos}")
            tmp = t.get_dict_link(tmp)
            if tmp != t.root and tmp.pattern_ids:
                print(f"  Проверка по сжатой ссылке: узел {tmp.id}")
    
    print(f"\n--- Результат ---")
    results.sort()
    output = [f"{pos} {p_id}" for pos, p_id in results]
    print("\n".join(output) if output else "Совпадений не найдено")