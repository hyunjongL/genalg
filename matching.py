
sequences = ["abce", "1234e"]
target = "abcde"

def print_matrices(M):
    for m in M:
        print_matrix(m)

def print_matrix(m):
    for l in m:
        for j in l:
            print(j, end='\t')
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

def initialize_matrices(mats, gap):
    for m in mats:
        initialize_matrix(m, gap)

def initialize_matrix(mat, gap):
    lenseq = len(mat)
    lentar = len(mat[0])
    cnt = 0
    for i in range(lenseq):
        mat[i][0] = cnt * gap
        cnt -= 1
    cnt = 0
    for j in range(lentar):
        mat[0][j] = cnt * gap
        cnt -= 1

# TODO: Implement dynamic Iterations

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


def iterate_mats(seq, tar, mat, inc, gap):
    if not check_args(seq, tar, mat):
        exit(-1)
    for i in range(len(seq)):
        iterate_mat(seq[i], tar, mat[i], inc, gap)


def iterate_mat(seq, tar, mat, inc, gap):
    for i in range(1, len(mat)):
        for j in range(1, len(mat[0])):
            if seq[j-1] == tar[i-1]:
                mat[i][j] = max_around(mat, i, j) + inc
            else:
                mat[i][j] = max_around(mat, i, j) - gap
    return


if __name__ == '__main__':
    gap = 1
    inc = 1
    M = gen_matrix(sequences, target)
    initialize_matrices(M, gap)
    print_matrices(M)
    iterate_mats(sequences, target, M, inc, gap)
    print_matrices(M)
