

class reaction:
    def __init__(self, a, b, name=''):
        self.apple = a
        self.banana = b
        self.name = name

    def __str__(self):
        return self.name


if __name__ == "__main__":
    a_list = list()
    for i in range(10):
        r = reaction(0, 1, str(i))
        a_list.append(r)
    for r in a_list:
        print(r)
