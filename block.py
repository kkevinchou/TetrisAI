'''
  0 1 2
0 - - -
1 - - -
2 - - -

'''

class Block(object):
    def __init__(self, config):
        self.config = config

    # Rotates counter-clockwise
    def rotate(self):
        new_config = []
        for i in range(3):
            new_config.append(['-', '-', '-'])

        new_config[2][0] = self.config[0][0]
        new_config[1][0] = self.config[0][1]
        new_config[0][0] = self.config[0][2]
        new_config[2][1] = self.config[1][0]
        new_config[1][1] = self.config[1][1]
        new_config[0][1] = self.config[1][2]
        new_config[2][2] = self.config[2][0]
        new_config[1][2] = self.config[2][1]
        new_config[0][2] = self.config[2][2]

        self.config = new_config

    def get_cell(self, y, x):
        return self.config(y, x)

    def __str__(self):
        return '\n'.join(' '.join(row) for row in self.config)
