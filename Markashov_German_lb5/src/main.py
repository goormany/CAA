class Vertex:
    def __init__(self, id: int, parent, pchar: str, alpha=5):
        self.id = id
        self.next = [None] * alpha # список переходов внутри бора
        self.parent = parent
        self.pchar = pchar
        self.sufflink = None # Обычная суффиксная ссылка
        self.dict_link = None # Сжатая суффиксная ссылка (к ближайшему терминалу)
        self.go = [None] * alpha # список переходов в автомате
        self.pattern_ids = [] # Список ID шаблонов, заканчивающихся здесь
    
    def __str__(self) -> str:
        return f"id: {self.id}"
    
    def __repr__(self):
        return self.__str__()

def num(c):
    return "ACGTN".index(c)

class Trie:
    def __init__(self, alpha=5):
        self.alpha = alpha
        self.vertices = [Vertex(0, None, None, alpha)]
        self.root = self.vertices[0]
        
    
    def size(self):
        return len(self.vertices)
    
    def last(self):
        return self.vertices[-1]
    
    def add(self, s: str, pattern_id: int):
        v = self.root
        for char in s:
            c_idx = num(char)
            if v.next[c_idx] is None:
                self.vertices.append(Vertex(self.size(), v, char, self.alpha))
                v.next[c_idx] = self.last()
            v = v.next[c_idx]
        v.pattern_ids.append(pattern_id)
    
    def get_link(self, v: Vertex) -> Vertex:
        if v.sufflink is None:
            if v == self.root or v.parent == self.root:
                v.sufflink = self.root
            else:
                v.sufflink = self.go(self.get_link(v.parent), v.pchar)
        return v.sufflink
    
    def get_dict_link(self, v: Vertex) -> Vertex:
        if v.dict_link is None:
            link = self.get_link(v)
            if link == self.root:
                v.dict_link = self.root
            elif link.pattern_ids:
                v.dict_link = link
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
    text = input()
    n = int(input())
    
    t = Trie()
    pattern_len = [0] * (n + 1)
    
    for i in range(1, n + 1):
        p = input()
        pattern_len[i-1] = len(p)
        t.add(p, i-1)
    
    max_edges = 0
    for v in t.vertices:
        cur_edges = sum(1 for child in v.next if child is not None)
        if cur_edges > max_edges:
            max_edges = cur_edges
    print("Максимальное кол-во исходящих дуг:", max_edges)
    
    
    to_delete = [False] * len(text)
    v = t.root
    for i, char in enumerate(text):
        v = t.go(v, char)
        
        tmp = v
        while tmp != t.root:
            if tmp.pattern_ids:
                for p_id in tmp.pattern_ids:
                    length = pattern_len[p_id]
                    start_pos = i - length + 1
                    to_delete[start_pos:i+1] = [True] * length
            tmp = t.get_dict_link(tmp)
    
    remaining_text = "".join([text[i] for i in range(len(text)) if not to_delete[i]])
    print(f"Остаток строки поиска: {remaining_text}")
    