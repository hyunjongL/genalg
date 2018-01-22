import random


def check_pass(L, max):
    sum = 0
    for x in L:
        sum += x[0]
    sum = sum/len(L)
    if L[-1][0] >= max and sum >= max-1:
        for x in L:
            if x[0] < max - 1:
                return False
        return True
    return False


def get_random_set(n, m):
    result = list()
    for i in range(n):
        new = list()
        for i in range(m):
            if random.random() > 0.5:
                new.append(True)
            else:
                new.append(False)
        result.append((evaluate(new), new))
    result.sort()
    return result


def evaluate(gene):
    val = 0
    for x in gene:
        if x:
            val += 1
    return val


def mutate(L, N):
    # Get best N genes reproduce.
    new_list = list()
    for i in range(N):
        x = -1
        new_list.append(L[x])
        x -= 1
    for i in range(len(L) - N):
        sex1 = random.randint(0, N-1)
        sex2 = random.randint(0, N-1)
        new = list()
        for i in range(len(L[0][1])):
            t = random.random()
            if t > 0.6:
                new.append(new_list[sex1][1][i])
            elif t > 0.2:
                new.append(new_list[sex2][1][i])
            elif t > 0.1:
                new.append(True)
            else:
                new.append(False)
        new_list.append((evaluate(new), new))
    new_list.sort()
    return new_list


def run_main():
    L = get_random_set(20, 20)
    while(not check_pass(L, 19)):
        L = mutate(L, 5)
    print(L)


if __name__ == "__main__":
    run_main()
