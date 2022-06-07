import itertools

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


def find_length_n_paths_core(n, board, words, i, j, path_so_far, word_so_far):
    if not in_board(board, i, j) or (i, j) in path_so_far:
        return
    word = word_so_far + board[i][j]
    if len(words) == 0:
        return
    path_so_far.append((i, j))
    if n == len(path_so_far):
        if word in words:
            yield path_so_far
        path_so_far.pop()
        return
    words = [w for w in words if w.startswith(word)]
    for di, dj in DIRECTIONS:
        yield from find_length_n_paths_core(n, board, words, i+di, j+dj, path_so_far, word)
    path_so_far.pop()


def find_length_n_paths(n, board, words):
    if n == 0:
        return []
    res = []
    for i, row in enumerate(board):
        for j, _ in enumerate(row):
            gen = find_length_n_paths_core(
                n, board, words, i, j, [], '')
            res.extend(path.copy() for path in gen)
    return res


def find_length_n_words(n, board, words):
    res = []
    for word in words:
        if len(word) == n:
            res.extend([find_length_n_paths(i, board, [word]) for i in range(n)])
    return res


def max_score_paths(board, words):
    res = {}
    n = len(board) * len(board[0])
    while n > 0:
        n_paths = find_length_n_paths(n, board, words)
        for ind, word in enumerate([''.join([board[i][j] for i, j in path]) for path in n_path]):
            if word not in res:
                res[word] = [n_paths[ind]]
            elif len(res[word]) == len(n_paths[ind]):
                res[word].append([n_paths[ind]])
    options = []

    def combinations(keys):
        if len(keys) == 1:
            return [path for path in res[keys[0]]]
        for word in keys:
            options.append([word].extend(combo) for combo in combinations(keys[1:]))
    if len(keys):
        combinations(res.keys())
    return options




if __name__ == '__main__':
    board = [
        ['A', 'B', 'C', 'E'],
        ['S', 'F', 'C', 'S'],
        ['A', 'D', 'E', 'E']
    ]
    words = ["ABCCED", "SEE", "ABCB"]
    print(find_length_n_paths(3, board, words))
    print(find_length_n_paths(4, board, words))
    print(find_length_n_paths(6, board, words))
    #print(find_length_n_words(3, board, words))
    #print(max_score_paths(board, words))
    path1 = [(1, 3), (2, 3), (2, 2)]
    path2 = [(0, 0), (1, 0), (2, 0), (3, 0)]
    path3 = [(0, 0), (1, 0), (2, 0), (3, 0)]
    path4 = [(0, 0), (2, 0), (2, 1), (3, 1)]
    path5 = [(1, 0), (2, 0), (2, 1), (3, 1)]
    print(path1, is_valid_path(board, path1, words), ''.join([board[i][j] for i, j in path1]))
    print(path2, is_valid_path(board, path2, words))
    print(path3, is_valid_path(board, path3, words))
    print(path4, is_valid_path(board, path4, words))
    print(path5, is_valid_path(board, path5, words))
