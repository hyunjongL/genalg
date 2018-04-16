import time
import json

debug = False

# match_points = (FULL, INTENT, FORM, NO_MATCH)
match_points = (1, 0.7, 0.5, -1)

# incentifies when Q&A categories match
category_incentive = 2


def match(a, b, beforeA=None, beforeB=None):
    weight = 1
    # Function to calculate reward for two labels.
    # a = QQ, b = QA
    if beforeA is not None and beforeB is not None:
        if len(beforeA) > 2 and len(beforeB) > 2:
            weight = category_incentive
    if a[1] == b[1]:
        if a[0] == b[0]:
            # Both
            return match_points[0]
        # Intent matches
        return match_points[1]
    if a[0] == b[0]:
        # Form matches
        return match_points[2]
    # None
    return match_points[3]


class seqmap:
    def __init__(self, corpus, init):
        self.corpus = corpus            # Save the corpus as object
        self.corpusnum = len(corpus)    # Number of corpus
        self.mat = list([list(0 for j in range(len(i[0]) + 1))] for i in corpus)
                                        # array to calculate
        dummy = {'max': 0,              # Dummy for saving max values
                 'length': 0,
                 'type': ' ',
                 'at': [0]}
        self.maxs = list(dummy for i in corpus) # Save max values
        self.seq = []                   # Current input sequence
        self.append(init)

    def append(self, addseq):
        for row in self.maxs:
            row['max'] = int(row['max'] * 0.8)
        if addseq == '':
            return

        self.seq.append(addseq)

        for j in range(self.corpusnum):
            # for each corpus,
            self.mat[j].append([0])

            for k in range(len(self.corpus[j][0])):
                # Update Arrays
                # Get the highest neighbor and add according to the
                # matching reward.

                # newval = previous top score
                newval = max(self.mat[j][-2][k],
                             int(self.mat[j][-2][k+1] * 0.7))

                # previous score is updated with the match
                if k != 0 and len(self.seq) > 1:
                    newval += int(match(self.corpus[j][0][k], addseq, self.corpus[j][0][k-1], self.seq[-2]) * len(self.seq))
                else:
                    newval += int(match(self.corpus[j][0][k], addseq) * len(self.seq))
                self.mat[j][-1].append(max(newval, 0))

                # Max value cache
                if newval > self.maxs[j]['max']:
                    self.maxs[j] = {'max': newval,
                                    'length': len(self.seq),
                                    'type': self.corpus[j][1],
                                    'at': [k + 1]}
                elif newval == self.maxs[j]['max']:
                    self.maxs[j]['at'].append(k + 1)

    def print(self):
        if debug is True:
            # Printing the whole array
            for i in range(self.corpusnum):
                print("", end='\t\t')
                for j in self.corpus[i][0]:
                    print(j, end='\t')
                print("")
                for k in range(len(self.seq)+1):
                    if k == 0:
                        print("", end='\t')
                    else:
                        print(self.seq[k-1], end='\t')
                    for j in range(len(self.corpus[i][0])+1):
                        print(self.mat[i][k][j], end='\t')
                    print('')
                print('')
        print('\n--Summary--\n')
        rank = {}
        for row in self.maxs:
            if row['type'] in rank:
                rank[row['type']] += row['max']
            else:
                rank[row['type']] = row['max']
        print(' -Aggregate-')
        for r in rank:
            print(r, rank[r])
        print(' -Max-')
        temp = 0
        for m in self.maxs:
            if temp < m['max']:
                temp = m['max']
        for i in range(len(self.maxs)):
            if temp == self.maxs[i]['max']:
                print_str = 'With points {}, Corpus {} of type {} have matches at {}'
                print(print_str.format(self.maxs[i]['max'],
                                       i + 1,
                                       self.maxs[i]['type'],
                                       self.maxs[i]['at']))

    def _max(self):
        json_form = {
          'corpus_max_num': 0,
          'corpus_max': [],
          'average_max_num': 0,
          'average_max': []
        }
        rank = {}
        count = {}
        for row in self.maxs:
            if row['type'] in rank:
                rank[row['type']] += row['max']
                count[row['type']] += 1
            else:
                rank[row['type']] = row['max']
                count[row['type']] = 1
        for r in rank:
            rank[r] = rank[r] / count[r]
        average_max = rank[max(rank, key=lambda k: rank[k])]
        for r in rank:
            if rank[r] == average_max:
                json_form['average_max'].append(r)
        temp = 0
        for m in self.maxs:
            if temp < m['max']:
                temp = m['max']
        for i in range(len(self.maxs)):
            if temp == self.maxs[i]['max']:
                json_form['corpus_max'].append(i + 1)
        json_form['corpus_max_num'] = len(json_form['corpus_max'])
        json_form['average_max_num'] = len(json_form['average_max'])
        return json.dumps(json_form)

'''
Request	Questi	Answer	Compli	Rebuke	Banter	Opinion	Apolo	Thank	Confirm
0       1	    2	    3	    4      	5	    6	    7	    8	    9

Disclo  Edifi   Advise  Confirm Questi  Ackn    Interp  Reflec
1       2       3       4       5       6       7       8

'''



if __name__ == "__main__":
    # load Corpus
    corpus = [
        #  1     2     3     4     5     6     7     8     9     10    11    12
        (['QQ', 'DD', 'QQ', 'QQ', 'QQ', 'DD', 'AA', 'KK', 'QQ', 'DD', 'AA', 'QQ'], 'A'), # 1 Hyunwoo
        (['QQ', 'DD', 'QQ', 'QQ', 'QQ', 'QQ', 'AA', 'DD', 'QQ', 'DD', 'AA', 'KK'], 'A'), # 2 Jean
        (['QQ', 'DD', 'QQ', 'DD', 'QQ', 'CC', 'AA', 'DD', 'QQ', 'DD', 'AA', 'QQ'], 'A'), # 3 Eunyeong
        (['QQ', 'DD', 'QQ', 'DD', 'QQ', 'KK', 'AA', 'KK', 'QQ', 'DD', 'AA', 'KK'], 'A'), # 4 Seoyoung
        (['QQ', 'DD', 'QQ', 'DD', 'QQ', 'CD', 'AA', 'KK', 'QQ', 'QQ', 'AA', 'KK'], 'B'), # 5 SC
        (['QQ', 'DD', 'QQ', 'DD', 'QQ', 'DD', 'AA', 'KK', 'QQ', 'DD', 'AA', 'KK'], 'B'), # 6 Paul
        (['QQ', 'DD', 'QQ', 'DD', 'QQ', 'KK', 'AA', 'KK', 'QQ', 'DD', 'AA', 'KK'], 'B'), # 7 Jiyoun
        (['QQ', 'DD', 'QQ', 'AA', 'QQ', 'DD', 'AA', 'KK', 'QQ', 'DD', 'AA', 'KK'], 'B')  # 8 KJ
    ]
    corpus2 = [
        (['DD', 'QQ', 'DD', 'KK', 'DD', 'QQ'], 'A'), # 1 Hyunwoo
        (['DD', 'QQ', 'QQ', 'DD', 'DD', 'KK'], 'A'), # 2 Jean
        (['DD', 'DD', 'CC', 'DD', 'DD', 'QQ'], 'A'), # 3 Eunyeong
        (['DD', 'DD', 'KK', 'KK', 'DD', 'KK'], 'A'), # 4 Seoyoung
        (['DD', 'DD', 'CD', 'KK', 'QQ', 'KK'], 'B'), # 5 SC
        (['DD', 'DD', 'DD', 'KK', 'DD', 'KK'], 'B'), # 6 Paul
        (['DD', 'DD', 'KK', 'KK', 'DD', 'KK'], 'B'), # 7 Jiyoun
        (['DD', 'AA', 'DD', 'KK', 'DD', 'KK'], 'B')  # 8 KJ
    ]  # Only the human response

    handler = seqmap(corpus, '')
    handler.print()
    while(True):
        curr = ''
        for cat in handler.seq:
            curr += cat + ' '
        s = input("SEQ: " + curr)
        if s == '.':
            exit(0)
        if s == '*':
            # Enter '*' to enable debug mode.
            # Debug mode shows the full 2-dim arrays
            # where we calculate the points
            debug = not debug
            continue
        handler.append([s])
        handler.print()
