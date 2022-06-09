import itertools
import json


def __all_words():
    with open('boggle_dict.txt') as f:
        return f.read().splitlines()

DIRECTIONS = {
    (-1, -1),
    (-1, 0),
    (-1, 1),
    (0, 1),
    (1, 1),
    (1, 0),
    (1, -1),
    (0, -1)
}


def is_valid_path(board, path, words):
    if False in [in_board(board, i, j) for i, j in path]:
        return False
    elif not ''.join([board[i][j] for i, j in path]) in words:
        return False
    path_ = path.copy()
    path_.pop()
    for ind, coords in enumerate(path_):
        if not (abs(path[ind + 1][0] - coords[0]), abs(path[ind + 1][1] - coords[1])) in DIRECTIONS:
            return False
    return True


def in_board(board, i, j):
    return 0 <= i < len(board) and 0 <= j < len(board[0])


def find_length_n_paths_core(board, words, i, j, path_so_far, word_so_far, n=None, m=None ):
    if not in_board(board, i, j) or (i, j) in path_so_far:
        return
    word = word_so_far + board[i][j]
    if len(words) == 0:
        return
    path_so_far.append((i, j))
    if n and n == len(path_so_far):
        if word in words:
            yield path_so_far
        path_so_far.pop()
        return
    elif m and len(path_so_far) == m:
        if word in words:
            yield path_so_far
        path_so_far.pop()
        return
    words = [w for w in words if w.startswith(word)]
    for di, dj in DIRECTIONS:
        yield from find_length_n_paths_core(board, words, i+di, j+dj, path_so_far, word, n, m)
    path_so_far.pop()


def find_length_n_paths(n, board, words):
    if n == 0:
        return []
    res = []
    for i, row in enumerate(board):
        for j, _ in enumerate(row):
            gen = find_length_n_paths_core(
                board, words, i, j, [], '', n)
            res.extend(path.copy() for path in gen)
    return res


def find_length_n_words(n, board, words):
    res = []
    if n == 0:
        return res
    words_in_length = [word for word in words if len(word) == n]
    for i, row in enumerate(board):
        for j, _ in enumerate(row):
            gen = find_length_n_paths_core(
                board, words_in_length, i, j, [], '', 0, n)
        res.extend(path.copy() for path in gen)
    return res


def max_score_paths(board, words):
    res = {}
    n = max([len(word) for word in words])
    while n > 0:
        n_paths = find_length_n_paths(n, board, words)
        if not n_paths:
            n -= 1
            continue
        for path in n_paths:
            word = ''.join([board[i][j] for i, j in path])
            if word not in res:
                res[word] = path
        n -= 1
    return [path for path in res.values()]


if __name__ == '__main__':
    words = __all_words()

    board1 = [
        ['A', 'E', 'K', 'E'],
        ['S', 'C', 'EE', 'S'],
        ['A', 'D', 'E', 'E']
    ]
    board2 = [
        ['A', 'K', 'C', 'E', 'K', 'Q', 'D', 'R'],
        ['S', 'F', 'U', 'S', 'A', 'BA', 'C', 'E'],
        ['A', 'Q', 'E', 'E', 'A', 'B', 'C', 'E'],
        ['A', 'B', 'CR', 'C', 'KEC', 'Q', 'D', 'R'],
        ['S', 'F', 'C', 'S', 'K', 'Q', 'D', 'R'],
        ['A', 'D', 'E', 'E', 'K', 'QU', 'D', 'R']
    ]
    words1 = ["SEED", "SEE", "SEEK"]
    words2 = ['ABAB', 'ABAC', 'QUD', 'QUK']
    print(find_length_n_paths(3, board1, words))
    print(find_length_n_paths(4, board1, words))
    print(find_length_n_paths(6, board1, words))
    print(find_length_n_words(3, board1, words))
    print(max_score_paths(board2, words))
    path1 = [(1, 3), (2, 3), (2, 2)]
    path2 = [(0, 0), (1, 0), (2, 0), (3, 0)]
    path3 = [(0, 0), (1, 0), (2, 0), (3, 0)]
    path4 = [(0, 0), (2, 0), (2, 1), (3, 1)]
    path5 = [(1, 0), (2, 0), (2, 1), (3, 1)]
    # print(path1, is_valid_path(board, path1, words), ''.join([board[i][j] for i, j in path1]))
    # print(path2, is_valid_path(board, path2, words))
    # print(path3, is_valid_path(board, path3, words))
    # print(path4, is_valid_path(board, path4, words))
    # print(path5, is_valid_path(board, path5, words))

    print(max_score_paths(board2, words2))
    for combo in max_score_paths(board2, words):
        print(combo)