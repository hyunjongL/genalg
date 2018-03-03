import time
import matching2

def test(length, number):
    t = 0
    corpus = list()
    for i in range(number):
        corpus.append("abcdefghijklmnopqrstuvwxyz"[:length - 1] + str(i)[0])
    print("Number of Seqs: " + str(len(corpus)))
    print("Length of a Seq: " + str(len(corpus[0])))
    handler = matching2.seqmap(corpus, '')
    for i in range(10):
        start_time = time.time()
        handler.append(str(i)[0])
        delta = time.time() - start_time
        print("--- %s seconds ---" % (delta))
        t += delta
    print(t / 10.0)

test(10, 100)
test(20, 100)
test(10, 1000)
test(20, 1000)
test(10, 10000)
test(20, 10000)
