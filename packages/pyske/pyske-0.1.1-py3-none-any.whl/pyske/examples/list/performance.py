from pyske.core.list.slist import SList
from pyske.core.list.plist import PList
from pyske.core.support.parallel import *
from operator import *
from gc import *

iterations = 10


def test(f, input, name):
    times = SList()
    print(f'Test: {name}')
    for i in range(0, iterations):
        print(f'  Iteration: {i}', end='\r')
        collect()
        t = wtime()
        output = f(input)
        t = wtime() - t
        times.append(t)
    print(30 * ' ', end='\r')
    print(f'  Min time:\t{times.reduce(min)}')
    print(f'  Max time:\t{times.reduce(max)}')
    print(f'  Avg time:\t{times.reduce(add) / times.length()} ')
    return output


input = SList(range(1, 4_000_000))

t1 = test(lambda l: l.map2(l, add), input, "map2")

assert t1