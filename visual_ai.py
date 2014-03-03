import sys
import time
from tetris import Tetris

class DummyQueue(object):
    def put(self, item):
        pass

with open('trait_set.dat') as f:
    for line in f:
        if line[0] == '#':
            continue

        trait_set = line.split(',')
        if len(trait_set) != 4:
            print 'ERROR: Trait set must be a comma separated list of four elements'
            sys.exit(0)

        trait_set = [float(trait.strip()) for trait in trait_set]
        Tetris.main(time.time(), 0, DummyQueue(), [1.0899486313285176, -0.00048470297714053867, 2.05484698586114, -2.7296141753723413], True)
