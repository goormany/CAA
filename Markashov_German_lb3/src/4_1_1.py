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
    return dp[n][m]
        


def main():
    cost_replace, cost_insert, cost_delete = list(map(int, input().split(" ")))
    s1 = input()
    s2 = input()
    
    dist = lev_dist(s1, s2, cost_replace, cost_insert, cost_delete)
    print(dist)

if __name__ == "__main__":
    main()