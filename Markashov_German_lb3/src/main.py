def lev_dist_prefixes(s1: str, s2: str):
    n, m = len(s1), len(s2)
    prev = list(range(m + 1))
    curr = [0] * (m + 1)
    
    dists = [prev[m]]  # расстояние от пустого префикса до s2
    
    for i in range(1, n + 1):
        curr[0] = i
        for j in range(1, m + 1):
            if s1[i-1] == s2[j-1]:
                curr[j] = prev[j-1]
            else:
                curr[j] = min(prev[j], curr[j-1], prev[j-1]) + 1
        dists.append(curr[m])
        prev, curr = curr, prev
    
    return dists

def main():
    s1 = input()
    s2 = input()
    n = len(s1)

    prefix_dists = lev_dist_prefixes(s1, s2)
    min_pref = min(prefix_dists)
    best_prefixes = [s1[:i] for i, d in enumerate(prefix_dists) if d == min_pref]
    
    s1_rev = s1[::-1]
    s2_rev = s2[::-1]
    suffix_dists_rev = lev_dist_prefixes(s1_rev, s2_rev)
    suffix_dists = [0] * (n + 1)
    for k in range(n + 1):
        suffix_dists[n - k] = suffix_dists_rev[k]

    min_suff = min(suffix_dists)
    best_suffixes = [s1[i:] for i, d in enumerate(suffix_dists) if d == min_suff]
    
    print(f"Префиксы: мин. расстояние = {min_pref}")
    print("Префиксы:", best_prefixes)
    print(f"Суффиксы: мин. расстояние = {min_suff}")
    print("Суффиксы:", best_suffixes)

if __name__ == "__main__":
    main()