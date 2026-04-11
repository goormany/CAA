from tsp_2approx import INF, create_mst, build_adjacency, dfs_preorder, path_len

def test_create_mst():
    matrix = [
        [INF, 2, 3],
        [2, INF, 4],
        [3, 4, INF]
    ]
    parent, parent_weight = create_mst(matrix, start_vertex_idx=0)
    
    assert parent[0] == -1
    assert parent_weight[0] == 0
    assert sum(1 for p in parent if p != -1) == 2

def test_build_adjacency():
    parent = [-1, 0, 0]
    parent_weight = [0, 5, 3]
    adj = build_adjacency(parent, parent_weight)
    
    neighbors_0 = [v for v, _ in adj[0]]
    assert 1 in neighbors_0
    assert 2 in neighbors_0
    
    neighbors_1 = [v for v, _ in adj[1]]
    assert 0 in neighbors_1

def test_dfs_preorder():
    adj = [
        [(1, 5), (2, 3)],
        [(0, 5)],
        [(0, 3)]
    ]
    path = dfs_preorder(adj, start=0)
    
    assert path[0] == 0
    assert len(path) == 3

def test_path_len():
    matrix = [
        [0, 1, 2],
        [1, 0, 3],
        [2, 3, 0]
    ]
    path = [0, 1, 2, 0]
    length = path_len(path, matrix)
    
    assert length == 6.0