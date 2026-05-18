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
            print(f"Добавление шаблона #{pattern_id + 1}: '{s}' (длина {len(s)})")
        v = self.root
        for idx, char in enumerate(s):
            c_idx = num(char)
            if v.next[c_idx] is None:
                self.vertices.append(Vertex(self.size(), v, char, self.alpha))
                v.next[c_idx] = self.last()
                if self.verbose:
                    print(f"  Создан узел {self.last().id} для символа '{char}'")
            v = v.next[c_idx]
        v.pattern_ids.append(pattern_id)
        if self.verbose:
            print(f"  Узел {v.id} отмечен как терминальный для шаблона #{pattern_id + 1}")
    
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
                    print(f"    Суффиксная ссылка узла {v.id} -> {v.sufflink.id}")
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
    
    print(f"\nТекст: '{text}' (длина {len(text)})")
    print(f"Количество шаблонов: {n}\n")
    
    t = Trie(verbose=True)
    pattern_len = [0] * (n + 1)
    
    print("--- Построение бора ---")
    for i in range(1, n + 1):
        p = input(f"Шаблон #{i}: ")
        pattern_len[i-1] = len(p)
        t.add(p, i-1)
    
    print("\n--- Анализ бора ---")
    max_edges = 0
    max_vertex_id = -1
    for v in t.vertices:
        cur_edges = sum(1 for child in v.next if child is not None)
        if cur_edges > max_edges:
            max_edges = cur_edges
            max_vertex_id = v.id
    print(f"Максимальное количество исходящих дуг: {max_edges} (узел {max_vertex_id})")
    
    print("\n--- Поиск и удаление шаблонов ---")
    to_delete = [False] * len(text)
    v = t.root
    
    for i, char in enumerate(text):
        print(f"\nПозиция {i+1}, символ '{char}':")
        v = t.go(v, char)
        print(f"  Переход в узел {v.id}")
        
        tmp = v
        found_any = False
        while tmp != t.root:
            if tmp.pattern_ids:
                for p_id in tmp.pattern_ids:
                    length = pattern_len[p_id]
                    start_pos = i - length + 1
                    print(f"  Найден шаблон #{p_id + 1} (длина {length}) на позициях [{start_pos+1}..{i+1}]")
                    to_delete[start_pos:i+1] = [True] * length
                    found_any = True
            tmp = t.get_dict_link(tmp)
        
        if not found_any:
            print(f"  Совпадений не найдено")
    
    print("\n--- Результат ---")
    deleted_count = sum(to_delete)
    print(f"Удалено символов: {deleted_count}")
    print(f"Осталось символов: {len(text) - deleted_count}")
    
    remaining_text = "".join([text[i] for i in range(len(text)) if not to_delete[i]])
    print(f"Остаток строки поиска: {remaining_text}")
    
    if not remaining_text:
        print("Текст полностью удалён")