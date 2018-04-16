import time
import json


def match(a, b):
    # a = QQ, b = QA
    if a[1] == b[1]:
        if a[0] == b[0]:
            # Both
            return 1
        # Intent
        return 0.7
    if a[0] == b[0]:
        # Form
        return 0.3
    # None
    return -0.5


class seqmap:
    def __init__(self, corpus, init):
        self.corpus = corpus
        self.corpusnum = len(corpus)
        self.current_input = list()
        self.current_length = 1
        self.mat = list(0 for i in range(self.corpusnum))

    def append(self, addseq):
        self.current_input.append(addseq)
        for corp_num in range(self.corpusnum):
            self.mat[corp_num] += int(match(addseq, self.corpus[corp_num][0][self.current_length-1]) * self.current_length)
            if self.mat[corp_num] < 0:
                self.mat[corp_num] = 0
        self.current_length += 1

    def print(self):
        print(self.mat)
        max_point = 0
        maxs = list()
        aggregate_max = {}
        aggregate_max_point = 0
        for i in range(self.corpusnum):
            if max_point < self.mat[i]:
                max_point = self.mat[i]
            if self.corpus[i][1] in aggregate_max:
                aggregate_max[self.corpus[i][1]] += self.mat[i]
            else:
                aggregate_max[self.corpus[i][1]] = self.mat[i]

        for i in range(self.corpusnum):
            if max_point == self.mat[i]:
                print('best:', max_point, self.corpus[i][1], 'corpus number', i)

        aggregate_max_point = aggregate_max[max(aggregate_max, key=lambda k: aggregate_max[k])]
        for i in aggregate_max:
            if aggregate_max_point * 0.8 < aggregate_max[i]:
                maxs.append(i)
        if len(maxs) == 1:
            print('\naggregate max:', maxs[0], aggregate_max[maxs[0]])
        else:
            print('\nduplicate maxs')
            for i in maxs:
                print(i, aggregate_max[i])

    def _max(self):
        json_form = {
          'corpus_max_num': 0,
          'corpus_max': [],
          'average_max_num': 0,
          'average_max': []
        }
        return_set = []
        max_point = 0
        maxs = list()
        aggregate_max = {}
        count = {}
        aggregate_max_point = 0
        for i in range(self.corpusnum):
            if max_point < self.mat[i]:
                max_point = self.mat[i]
            if self.corpus[i][1] in aggregate_max:
                aggregate_max[self.corpus[i][1]] += self.mat[i]
                count[self.corpus[i][1]] += 1
            else:
                aggregate_max[self.corpus[i][1]] = self.mat[i]
                count[self.corpus[i][1]] = 1
        for i in range(self.corpusnum):
            if max_point == self.mat[i]:
                json_form['corpus_max'].append(i)
        json_form['corpus_max_num'] = len(json_form['corpus_max'])

        for key in aggregate_max:
            aggregate_max[key] = aggregate_max[key] / count[key]
        aggregate_max_point = aggregate_max[max(aggregate_max, key=lambda k: aggregate_max[k])]

        for i in aggregate_max:
            if aggregate_max_point * 0.9 < aggregate_max[i]:
                maxs.append(i)
        if len(maxs) == 1:
            json_form['aggregate_max'].append(maxs[0])
        else:
            for i in maxs:
                json_form['aggregate_max'].append(i)
        json_form['aggregate_max_num'] = len(json_form['aggregate_max'])
        return json.dumps(json_form)


if __name__ == "__main__":

    # load Corpus
    corpus = [
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
        for cat in handler.current_input:
            curr += cat + ' '
        s = input("SEQ: " + curr)
        if s == '.':
            exit(0)
        handler.append(s)
        handler.print()
