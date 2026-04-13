from littl import *

def test_matrix_copy():
    original = [[1, 2, 3], [4, 5, 6]]
    copied = matrix_copy(original)
    
    assert copied == original
    assert copied is not original
    assert copied[0] is not original[0]


def test_reduce_matrix():
    matrix = [
        [INF, 1, 3],
        [3, INF, 1],
        [1, 2, INF]
    ]
    bound = reduce_matrix(matrix)
    
    assert bound == 3
    zeros = sum(row.count(0) for row in matrix)
    assert zeros >= 3


def test_remove_row_col():
    matrix = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ]
    rows = [0, 1, 2]
    cols = [0, 1, 2]
    
    new_matrix, new_rows, new_cols = remove_row_col(matrix, rows, cols, 0, 1)
    
    assert new_matrix == [[4, 6], [7, 9]]
    assert new_rows == [1, 2]
    assert new_cols == [0, 2]


def test_forbid_edge():
    matrix = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ]
    rows = [0, 1, 2]
    cols = [0, 1, 2]
    
    forbid_edge(matrix, rows, cols, from_city=1, to_city=2)
    
    assert matrix[1][2] == INF


def test_estimate_zero():
    matrix = [
        [INF, 0, 2],
        [2, INF, 0],
        [0, 1, INF]
    ]
    penalty = estimate_zero(matrix, 3, 0, 1)
    assert penalty == 3
    
    penalty = estimate_zero(matrix, 3, 1, 2)
    assert penalty == 4


def test_find_best_zero():
    matrix = [
        [INF, 0, 2],
        [2, INF, 0],
        [0, 1, INF]
    ]
    pos, penalty = find_best_zero(matrix)
    
    assert pos == (1, 2)
    assert penalty == 4


def test_reconstruct_path():
    edges = [(0, 1), (1, 2), (2, 0)]
    path = reconstruct_path(edges, 3)
    
    assert path == [0, 1, 2]


def test_find_chain_endpoints():
    edges = [(0, 1), (2, 3)]
    start, end = find_chain_endpoints(edges, u=1, v=2)
    
    assert start == 0
    assert end == 3


def test_creates_small_cycle():
    edges = [(0, 1), (1, 2), (3, 4)]
    
    assert creates_small_cycle(edges, u=2, v=0, total_n=5) == True
    
    assert creates_small_cycle(edges, u=2, v=3, total_n=5) == False
    
    edges_full = [(0, 1), (1, 2)]
    assert creates_small_cycle(edges_full, u=2, v=0, total_n=3) == False


def test_tsp_3x3():
    matrix = [
        [INF, 1, 3],
        [3, INF, 1],
        [1, 2, INF]
    ]
    path, cost = tsp_branch_and_bound(matrix)
    
    assert path == [0, 1, 2]
    assert cost == 3


def test_tsp_4x4():
    matrix = [
        [INF, 10, 15, 20],
        [10, INF, 35, 25],
        [15, 35, INF, 30],
        [20, 25, 30, INF]
    ]
    path, cost = tsp_branch_and_bound(matrix)
    
    assert path == [0, 2, 3, 1]
    assert cost == 80


def test_tsp_with_minus_one():
    matrix = [
        [INF, 41, 40, 48, 40, 42],
        [48, INF, 41, 29, 42, 46],
        [22, 22, INF, 23, 24, 19],
        [15, 17, 11, INF, 10, 14],
        [47, 43, 18, 42, INF, 52],
        [34, 39, 30, 39, 32, INF]
    ]
    path, cost = tsp_branch_and_bound(matrix)
    
    assert path[0] == 0
    assert len(path) == 6
    assert cost > 0