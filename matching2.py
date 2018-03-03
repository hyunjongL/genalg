import time


class seqmap:
    def __init__(self, corpus, init):
        self.corpus = corpus
        self.corpusnum = len(corpus)
        self.mat = list()
        for i in corpus:
            temp = list()
            for j in i:
                temp.append(0)
            temp.append(0)
            self.mat.append([temp])
        self.maxs = list()
        for i in range(self.corpusnum):
            self.maxs.append([0, 0, 0, '0'])
        self.seq = ''
        self.append(init)

    def append(self, addseq):
        for i in self.maxs:
            i[0] = int(i[0] * 0.8)
        if addseq == '':
            return
        for i in range(len(addseq)):
            self.seq += addseq[i]
            for j in range(self.corpusnum):
                self.mat[j].append([0])
                for k in range(len(self.corpus[j])):
                    newval = max(int(self.mat[j][-1][-1] * 0.7),
                                 self.mat[j][-2][k],
                                 int(self.mat[j][-2][k+1] * 0.7))
                    if self.corpus[j][k] == addseq[i]:
                        newval += len(self.seq)
                    else:
                        newval = int(newval - len(self.seq) * 0.9 - 1)
                    self.mat[j][-1].append(max(newval, 0))
                    if newval > self.maxs[j][0]:
                        try:
                            self.maxs[j] = [newval, k + 1, len(self.seq), self.corpus[j][k + 1]]
                        except:
                            self.maxs[j] = [newval, k + 1, len(self.seq), 'END']


    def print(self):
        for i in range(self.corpusnum):
            print("", end='\t\t')
            for j in self.corpus[i]:
                print(j, end='\t')
            print("")
            for k in range(len(self.seq)+1):
                if k == 0:
                    print("", end='\t')
                else:
                    print(self.seq[k-1], end='\t')
                for j in range(len(self.corpus[i])+1):
                    print(self.mat[i][k][j], end='\t')
                print('')
            print('')
            print(self.maxs[i], end='')
            try:
                print("\tSuggested: "
                      + self.corpus[i][self.maxs[i][1]]
                      + " by point "
                      + str(self.maxs[i][0]))
            except:
                print("\t Suggested: End of Conversation")
        points = {'.': 0}
        for i in range(self.corpusnum):
            try:
                if self.corpus[i][self.maxs[i][1]] in points:
                    points[self.corpus[i][self.maxs[i][1]]] += self.maxs[i][0]
                else:
                    points[self.corpus[i][self.maxs[i][1]]] = self.maxs[i][0]
            except:
                points['.'] += self.maxs[i][0]
        #print(points)
        #print(self.maxs)
        for k in self.maxs:
            print(k)
            print('points: ' + str(k[0]) + ', Category Num: ' + k[3])
        print(max(points, key=lambda key: points[key]))


'''
Request	Questi	Answer	Compli	Rebuke	Banter	Opinion	Apolo	Thank	Confirm
0       1	    2	    3	    4      	5	    6	    7	    8	    9

Disclo  Edifi   Advise  Confirm Questi  Ackn    Interp  Reflec
1       2       3       4       5       6       7       8

'''

if __name__ == "__main__":

    # load Corpus
    corpus = ["abcde", "abfck", "bcdef"]
    '''
    corpus = ["1354545253515252",
              "518181111112",
              "52212",
              "551225",
              '5131412125285']
    '''
    handler = seqmap(corpus, '')
    handler.print()
    while(True):
        s = input("SEQ: " + handler.seq)
        if s == '.':
            exit(0)
        handler.append(s)
        handler.print()
