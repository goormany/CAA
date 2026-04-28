def lev_dist(s1: str, s2: str, cost_replace: int, cost_insert: int, cost_delete: int) -> int:
    n, m = len(s1), len(s2)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    
    for i in range(n + 1):
        dp[i][0] = i * cost_delete
    for j in range(m + 1):
        dp[0][j] = j * cost_insert
        
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = min(
                    dp[i-1][j] + cost_delete,
                    dp[i][j-1] + cost_insert,
                    dp[i-1][j-1] + cost_replace
                )

    i, j = n, m
    ops = []

    while i > 0 or j > 0:
        if i > 0 and j > 0 and s1[i - 1] == s2[j - 1]:
            ops.append('M')
            i -= 1
            j -= 1
        elif i > 0 and j > 0 and dp[i][j] == dp[i - 1][j - 1] + cost_replace:
            ops.append('R')
            i -= 1
            j -= 1
        elif i > 0 and dp[i][j] == dp[i - 1][j] + cost_delete:
            ops.append('D')
            i -= 1
        elif j > 0 and dp[i][j] == dp[i][j - 1] + cost_insert:
            ops.append('I')
            j -= 1

    ops.reverse()
    return ops
        


def main():
    cost_replace, cost_insert, cost_delete = list(map(int, input().split(" ")))
    s1 = input()
    s2 = input()
    
    path = lev_dist(s1, s2, cost_replace, cost_insert, cost_delete)
    print("".join(path))
    print(s1)
    print(s2)

if __name__ == "__main__":
    main()