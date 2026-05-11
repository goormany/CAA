def get_prefix_func(s: str) -> list[int]:
    n = len(s)
    pi = [0] * n
    
    for i in range(1, n):
        j = pi[i-1]
        
        while j > 0 and s[i] != s[j]:
            j = pi[j-1]
            
        if s[j] == s[i]:
            j += 1
            
        pi[i] = j
    return pi

def kmp(text: str, pattern: str) -> list[int]:
    nt = len(text)
    np = len(pattern)
    if np == 0: return []
    
    pi = get_prefix_func(pattern)
    res = []
    j = 0
    
    for i in range(nt):
        while j > 0 and text[i] != pattern[j]:
            j = pi[j-1]
        
        if text[i] == pattern[j]:
            j += 1
        
        if j == np:
            res.append(i - np + 1)
            j = pi[j-1]
            
    return res

if __name__ == "__main__":
    A = input()
    B = input()
    
    if len(B) != len(A):
        print(-1)
    else: 
        result = kmp(A*2, B)
        if result:
            print(result[0])
        else:
            print(-1)