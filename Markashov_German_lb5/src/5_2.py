class Vertex:
    def __init__(self, id: int, parent, pchar: str, alpha: int = 5):
        self.id = id
        self.next = [None] * alpha
        self.parent = parent
        self.pchar = pchar
        self.sufflink = None
        self.dict_link = None
        self.go = [None] * alpha
        self.substring_data = [] #Храним список стартовых позиций l_i (в 1-индексации оригинального шаблона) и длины этих подстрок
        
    def __str__(self) -> str:
        return f"id: {self.id}"
    
    def __repr__(self):
        return self.__str__()
    
def num(c):
    return "ACGTN".index(c)

class Trie:
    def __init__(self, alpha: int = 5):
        self.alpha = alpha
        self.vertices = [Vertex(0, None, None, self.alpha)]
        self.root = self.vertices[0]
    
    def size(self) -> int:
        return len(self.vertices)
    
    def last(self) -> Vertex:
        return self.vertices[-1]
    
    def add(self, s: str, l_i: int):
        v = self.root
        for char in s:
            c_idx = num(char)
            if v.next[c_idx] is None:
                self.vertices.append(Vertex(self.size(), v, char, self.alpha))
                v.next[c_idx] = self.last()
            v = v.next[c_idx]
        v.substring_data.append((l_i, len(s)))
    
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
                v.dict_link = link
            elif link.substring_data:
                v.dict_link = link
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
    text = input()
    pattern = input()
    wildcard = input()
    
    t = Trie()
    
    k = 0 # Количество безмасочных подстрок (наш целевой порог совпадений)
    cur_part = []
    
    # Выделяем подстроки Q_i и находим их стартовые позиции l_i (1-индексация)
    for i, char in enumerate(pattern):
        if char == wildcard:
            if cur_part:
                l_i = i - len(cur_part) + 1
                t.add("".join(cur_part), l_i)
                k += 1
                cur_part = []
        else:
            cur_part.append(char)
    
    if cur_part:
        l_i = len(pattern) - len(cur_part) + 1
        t.add("".join(cur_part), l_i)
        k += 1
        
    # Используем размер len(text) + 2, чтобы спокойно работать в 1-индексации
    C = [0] * (len(text) + 2) # Создаем массив счетчиков C
    
    v = t.root
    for i, char in enumerate(text):
        v = t.go(v, char)
        
        tmp = v
        while tmp != t.root:
            if tmp.substring_data:
                for l_i, length in tmp.substring_data:
                    j = i - length + 2
                    start_pos = j - l_i + 1
                    if start_pos >= 1 and start_pos + len(pattern) - 1 <= len(text):
                        C[start_pos] += 1
            tmp = t.get_dict_link(tmp)
    
    results = []
    for i in range(1, len(text) + 1):
        if C[i] == k:
            results.append(str(i))
    
    if results:
        print("\n".join(results))
    