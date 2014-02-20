import copy
import random

BLOCK_CONFIGS = {
    'I': [['-', '-', '-', '-'], ['x', 'x', 'x', 'x'], ['-', '-', '-', '-'], ['-', '-', '-', '-']],
    # 'J': [['-', '-', 'x', '-'], ['x', 'x', 'x', '-'], ['-', '-', '-', '-'], ['-', '-', '-', '-']],
    # 'L': [['-', '-', '-', '-'], ['x', 'x', 'x', '-'], ['-', '-', 'x', '-'], ['-', '-', '-', '-']],
    # 'O': [['x', 'x', '-', '-'], ['x', 'x', '-', '-'], ['-', '-', '-', '-'], ['-', '-', '-', '-']],
    # 'S': [['-', '-', 'x', '-'], ['-', 'x', 'x', '-'], ['-', 'x', '-', '-'], ['-', '-', '-', '-']],
    # 'Z': [['-', 'x', '-', '-'], ['-', 'x', 'x', '-'], ['-', '-', 'x', '-'], ['-', '-', '-', '-']],
    # 'T': [['-', 'x', '-', '-'], ['-', 'x', 'x', '-'], ['-', 'x', '-', '-'], ['-', '-', '-', '-']],
}

class Block(object):
    def __init__(self, block_type, config):
        self.block_type = block_type
        self.config = config

    @staticmethod
    def generate_pool():
        pool = [Block(block_type, copy.deepcopy(config)) for (block_type, config) in BLOCK_CONFIGS.iteritems()]
        random.shuffle(pool)
        return pool

    def rotate_cw(self):
        for i in range(4):
            new_config = []
            for i in range(4):
                new_config.append(['-', '-', '-', '-'])

        if self.block_type == 'I':
            new_config[3][0] = self.config[0][0]
            new_config[3][1] = self.config[1][0]
            new_config[3][2] = self.config[2][0]
            new_config[3][3] = self.config[3][0]
            new_config[2][0] = self.config[0][1]
            new_config[2][1] = self.config[1][1]
            new_config[2][2] = self.config[2][1]
            new_config[2][3] = self.config[3][1]
            new_config[1][0] = self.config[0][2]
            new_config[1][1] = self.config[1][2]
            new_config[1][2] = self.config[2][2]
            new_config[1][3] = self.config[3][2]
            new_config[0][0] = self.config[0][3]
            new_config[0][1] = self.config[1][3]
            new_config[0][2] = self.config[2][3]
            new_config[0][3] = self.config[3][3]
        elif self.block_type == 'O':
            return
        else:
            new_config[2][0] = self.config[0][0]
            new_config[2][1] = self.config[1][0]
            new_config[2][2] = self.config[2][0]
            new_config[1][0] = self.config[0][1]
            new_config[1][1] = self.config[1][1]
            new_config[1][2] = self.config[2][1]
            new_config[0][0] = self.config[0][2]
            new_config[0][1] = self.config[1][2]
            new_config[0][2] = self.config[2][2]

        self.config = new_config

    def get_cell(self, x, y):
        return self.config[x][y]

    def copy(self):
        return Block(self.block_type, copy.deepcopy(self.config))

    def __str__(self):
        return '\n'.join(' '.join(row) for row in self.config)
