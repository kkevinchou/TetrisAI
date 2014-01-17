'''

  0 1 2 3
0 - - - -
1 - - - -
2 - - - -
3 - - - -

'''

import copy
import random

BLOCK_CONFIGS = {
    'T': [['-', '-', '-', '-'], ['-', 'x', '-', '-'], ['-', 'x', 'x', '-'], ['-', 'x', '-', '-']],
    # 'O': [['-', '-', '-', '-'], ['-', 'x', 'x', '-'], ['-', 'x', 'x', '-'], ['-', '-', '-', '-']],
    # 'I': [['-', '-', '-', '-'], ['x', 'x', 'x', 'x'], ['-', '-', '-', '-'], ['-', '-', '-', '-']],
    # 'S': [['-', '-', '-', '-'], ['-', '-', 'x', 'x'], ['-', 'x', 'x', '-'], ['-', '-', '-', '-']],
    # 'Z': [['-', '-', '-', '-'], ['-', 'x', 'x', '-'], ['-', '-', 'x', 'x'], ['-', '-', '-', '-']],
    # 'L': [['-', '-', '-', '-'], ['-', 'x', 'x', 'x'], ['-', 'x', '-', '-'], ['-', '-', '-', '-']],
    # 'J': [['-', '-', '-', '-'], ['-', 'x', 'x', 'x'], ['-', '-', '-', 'x'], ['-', '-', '-', '-']],
    # 'T': [['-', '-', '-', '-'], ['-', 'x', 'x', 'x'], ['-', '-', 'x', '-'], ['-', '-', '-', '-']],
}

class Block(object):
    def __init__(self, block_type, config):
        self.block_type = block_type
        self.config = config
        self.num_rotations = 0

    @staticmethod
    def generate_pool():
        pool = [Block(block_type, copy.deepcopy(config)) for (block_type, config) in BLOCK_CONFIGS.iteritems()]
        random.shuffle(pool)
        return pool

    def _rotate_ccw(self, num_times):
        for i in range(num_times):
            new_config = []
            for i in range(4):
                new_config.append(['-', '-', '-', '-'])

            new_config[1][2] = self.config[1][0]
            new_config[1][1] = self.config[2][0]
            new_config[1][0] = self.config[3][0]
            new_config[2][2] = self.config[1][1]
            new_config[2][1] = self.config[2][1]
            new_config[2][0] = self.config[3][1]
            new_config[3][2] = self.config[1][2]
            new_config[3][1] = self.config[2][2]
            new_config[3][0] = self.config[3][2]

            self.config = new_config
            self.num_rotations += 1
            self.num_rotations %= 4

    def rotate_ccw(self):
        if self.block_type in ('L', 'J', 'T'):
            self._rotate_ccw(1)
        elif self.block_type in ('S', 'Z'):
            if self.num_rotations == 0:
                self._rotate_ccw(1)
            else:
                self._rotate_ccw(3)
        elif self.block_type == 'I':
            if self.num_rotations == 0:
                self._rotate_ccw(1)
                self.config[0][1] = '-'
                self.config[2][3] = 'x'
            else:
                self._rotate_ccw(3)
                self.config[0][1] = 'x'
                self.config[2][3] = '-'

    def get_cell(self, x, y):
        return self.config[x][y]

    def __str__(self):
        return '\n'.join(' '.join(row) for row in self.config)
