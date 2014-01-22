import copy
import random
from block import Block

class Tetris(object):
    width = 10
    height = 22

    def __init__(self):
        self.reset()

    def get_cell(self, x, y):
        return self.grid[x][y]

    def _get_collision_y(self, x):
        for y in range(self.height):
            if self.get_cell(x, y) == 'x':
                return y - 1

        return self.height - 1

    def place_block(self, block, position):
        for x in range(4):
            for y in range(4):
                if block.get_cell(x, y) == 'x':
                    self.grid[x + position[0]][y + position[1]] = 'x'

    def _clear_row(self, y):
        for x in range(self.width):
            self.grid[x][y] = '-'

    def _row_is_empty(self, row):
        return 'x' not in self.get_row(row)

    def _copy_row_to(self, row_from, row_to):
        for x in range(self.width):
            self.grid[x][row_to] = self.get_cell(x, row_from)

    def _cut_row_to(self, row_from, row_to):
        self._copy_row_to(row_from, row_to)
        self._clear_row(row_from)

    def reset(self):
        self.grid = []
        self.block_pool = []
        self.block = None
        self.position = (0, 0)

        for x in range(self.width):
            empty_column = []
            for y in range(self.height):
                empty_column.append('-')
            self.grid.append(empty_column)

    def start(self):
        self.block = self.generate_block()
        self.place_block(self.block, self.position)

    def can_place(self, block, position):
        for x in range(4):
            for y in range(4):
                x_pos = position[0] + x
                y_pos = position[1] + y

                if block.get_cell(x, y) == 'x':
                    if (x_pos >= self.width or y_pos >= self.height) or (x_pos < 0) or (self.get_cell(x_pos, y_pos) == 'x'):
                        return False

        return True

    def hide_current_block(self):
        for x in range(4):
            for y in range(4):
                if self.block.get_cell(x, y) == 'x':
                    self.grid[self.position[0] + x][self.position[1] + y] = '-'

    def move_down(self):
        new_position = (self.position[0], self.position[1] + 1)
        self.move_block(new_position)

    def move_up(self):
        new_position = (self.position[0], self.position[1] - 1)
        self.move_block(new_position)

    def move_left(self):
        new_position = (self.position[0] - 1, self.position[1])
        self.move_block(new_position)

    def move_right(self):
        new_position = (self.position[0] + 1, self.position[1])
        self.move_block(new_position)

    def move_block(self, new_position):
        self.hide_current_block()
        if self.can_place(self.block, new_position):
            self.place_block(self.block, new_position)
            self.position = new_position
        else:
            self.place_block(self.block, self.position)

    def generate_block(self):
        if len(self.block_pool) == 0:
            self.block_pool = Block.generate_pool()

        return self.block_pool.pop()

    def flash(self, position):
        actual_block = self.block
        collision_y = 99 # TODO: actually find a good initial value here

        for x in range(4):
            for y in range(4):
                if self.block.get_cell(x, y) == 'x':
                    collision_y = min(self._get_collision_y(x + position[0]) - y, collision_y)

        self.place_block(actual_block, (position[0], collision_y))

    def print_grid(self):
        border_str = ' '.join(['=' for x in range(self.width)])
        print border_str
        for y in range(self.height):
            row_str = []
            for x in range(self.width):
                row_str.append(self.grid[x][y])
            print ' '.join(row_str)
        print border_str

    def get_row(self, y):
        return [self.grid[x][y] for x in range(self.width)]

    def iter_row(self):
        for y in range(self.height - 1, -1, -1):
            yield y, [self.grid[x][y] for x in range(self.width)]

    def settle(self):
        for row_index, row in self.iter_row():
            filled_row = '-' not in row
            if filled_row:
                self._clear_row(row_index)

        non_empty_rows = []
        for row_index, row in self.iter_row():
            if not self._row_is_empty(row_index):
                non_empty_rows.append(row_index)

        next_empty_row = None
        for row_index, row in self.iter_row():
            if self._row_is_empty(row_index):
                next_empty_row = row_index
                break

        if next_empty_row is None:
            raise Exception('next_empty_row is None')

        for non_empty_row in non_empty_rows:
            self._cut_row_to(non_empty_row, next_empty_row)
            next_empty_row -= 1

