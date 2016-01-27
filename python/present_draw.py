
from random import shuffle
from collections import Counter

n = 20

shuffled = lambda ls: shuffle(ls) or ls
own_gift = lambda n: [i for i, j in enumerate(
    shuffled(list(range(n)))) if i == j]

# print own_gift(20)

#shuffled = lambda ls: shuffle(ls) or ls
for i, j in enumerate(shuffled(list(range(30)))):
    print '%s %s' % (i, j)
