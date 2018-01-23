
sequences = ["abcefg", "1c234e"]
target = "abcde"


def print_matrices(M):
    for m in range(len(M)):
        print(' ', end='\t\t')
        for s in sequences[m]:
            print(s, end='\t')
        print('')
        print_matrix(M[m])


def print_matrix(m):
    for l in range(len(m)):
        if l > 0:
            print(target[l-1], end='\t')
        else:
            print('', end='\t')
        for j in range(len(m[l])):
            print(m[l][j], end='\t')
        print('')
    print('')


def gen_matrix(seqs, tar):
    total_num = len(seqs)
    L = list()
    for k in range(total_num):
        block = list()
        for i in range(len(tar)+1):
            templist = list()
            for j in range(len(seqs[k])+1):
                templist.append(0)
            block.append(templist)
        L.append(block)
    return L


def initialize_matrices(mats, gap, bestalign):
    for m in mats:
        initialize_matrix(m, gap, bestalign)


def initialize_matrix(mat, gap, bestalign):
    lenseq = len(mat)
    lentar = len(mat[0])
    cnt = 0
    for i in range(lenseq):
        if bestalign:
            mat[i][0] = 0
        else:
            mat[i][0] = cnt * gap
        cnt -= 1
    cnt = 0
    for j in range(lentar):
        if bestalign:
            mat[0][j] = 0
        else:
            mat[0][j] = cnt * gap
        cnt -= 1


def max_around(mat, i, j):
    return max(mat[i-1][j-1], mat[i-1][j], mat[i][j-1])


def check_args(seq, tar, mat):
    if len(seq) != len(mat):
        print(1)
        return False
    for i in range(len(seq)):
        if len(seq[i]) != len(mat[i][0]) - 1:
            print(2)
            return False
        if len(tar) != len(mat[i]) - 1:
            print(3)
            return False
    return True


def iterate_mats(seq, tar, mat, inc, gap, bestalign):
    if not check_args(seq, tar, mat):
        exit(-1)
    max = list()
    for i in range(len(seq)):
        max.append(iterate_mat(seq[i], tar, mat[i], inc, gap, bestalign))
    return max


def iterate_mat(seq, tar, mat, inc, gap, bestalign):
    max_ = 0
    for i in range(1, len(mat)):
        for j in range(1, len(mat[0])):
            if seq[j-1] == tar[i-1]:
                if bestalign:
                    mat[i][j] = max(max_around(mat, i, j) + i - 1, 0)
                else:
                    mat[i][j] = max_around(mat, i, j) + inc
            else:
                if bestalign:
                    mat[i][j] = max(max_around(mat, i, j) - gap, 0)
                else:
                    mat[i][j] = max_around(mat, i, j) - gap
            if mat[i][j] > max_:
                max_ = mat[i][j]
    return max_

def get_path_mat(seq, tar, gap, inc, bestalign):
    M = gen_matrix(seq, tar)
    initialize_matrices(M, gap, bestalign)
    m = iterate_mats(seq, tar, M, inc, gap, bestalign)
    return M, m


if __name__ == '__main__':
    gap = 1
    inc = 2
    M = get_path_mat(sequences, target, gap, inc, True)
    print_matrices(M[0])
    print(M[1])
