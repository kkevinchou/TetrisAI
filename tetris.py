import copy
import random
from block import Block

class Tetris(object):
    width = 10
    height = 22

    def __init__(self):
        self.reset()

    def _get_cell(self, col, row):
        return self.grid[row][col]

    def _get_collision_y(self, col):
        for row in range(self.height):
            if self._get_cell(col, row) == 'x':
                return row - 1

        return self.height - 1

    def _place_block(self, block, position):
        for row in range(4):
            for col in range(4):
                if block.get_cell(col, row) == 'x':
                    self.grid[row + position[0]][col + position[1]] = block.get_cell(col, row)

    def _clear_row(self, row):
        for col in range(self.width):
            self.grid[row][col] = '-'

    def _row_is_empty(self, row):
        for col in range(self.width):
            if self.grid[row][col] == 'x':
                return False

        return True

    def _copy_row_to(self, row_from, row_to):
        for col in range(self.width):
            self.grid[row_to][col] = self._get_cell(col, row_from)

    def _cut_row_to(self, row_from, row_to):
        for col in range(self.width):
            self.grid[row_to][col] = self._get_cell(col, row_from)

        for col in range(self.width):
            self.grid[row_from][col] = '-'

    def reset(self):
        self.grid = []
        self.block_pool = []
        self.block = None
        self.position = (0, 3)

        for row in range(self.height):
            empty_row = []
            for col in range(self.width):
                empty_row.append('-')
            self.grid.append(empty_row)

    def start(self):
        self.generate_block()

    def generate_block(self):
        if len(self.block_pool) == 0:
            self.block_pool = Block.generate_pool()

        self.block = self.block_pool.pop()

    def flash(self):
        collision_y = 99 # TODO: actually find a good initial value here

        for row in range(4):
            for col in range(4):
                if self.block.get_cell(col, row) == 'x':
                    collision_y = min(self._get_collision_y(col + self.position[1]) - col, collision_y)

        self._place_block(self.block, (collision_y, self.position[1]))

    def print_grid(self):
        print ['=' for col in self.grid[0]]
        for row in self.grid:
            print row
        print ['=' for col in self.grid[0]]

    def settle(self):
        for row in range(self.height - 1, -1, -1):
            filled_row = True
            
            for col in range(self.width):
                if self._get_cell(col, row) == '-':
                    filled_row = False
                    break

            if filled_row:
                self._clear_row(row)

        non_empty_rows = []
        for row in range(self.height - 1, -1, -1):
            if not self._row_is_empty(row):
                non_empty_rows.append(row)

        next_empty_row = None
        for row in range(self.height - 1, -1, -1):
            if self._row_is_empty(row):
                next_empty_row = row
                break

        if next_empty_row is None:
            raise Exception('next_empty_row is None')

        for non_empty_row in non_empty_rows:
            self._cut_row_to(non_empty_row, next_empty_row)
            next_empty_row -= 1

