import copy
import random
from block import Block

class Tetris(object):
    width = 10
    height = 22

    def __init__(self):
        self.events = []
        self.init_controls()
        self.reset()

    def init_controls(self):
        self.event_to_action = {
            'FLASH': self.flash,
            'UP': self.move_up,
            'DOWN': self.move_down,
            'LEFT': self.move_left,
            'RIGHT': self.move_right,
            'ROTATE': self.rotate,
        }

    def reset(self):
        self.grid = []
        self.block_pool = []
        self.block = None
        self.position = (0, 0)
        self.gravity_timer = 0

        for x in range(self.width):
            empty_column = []
            for y in range(self.height):
                empty_column.append('-')
            self.grid.append(empty_column)

    def get_cell(self, x, y):
        return self.grid[x][y]

    def _get_collision_y(selfself, x):
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
        if row_from == row_to:
            return
        self._copy_row_to(row_from, row_to)
        self._clear_row(row_from)

    def start(self):
        self.position = (0, 0)
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
        return self.move_block(new_position)

    def move_up(self):
        new_position = (self.position[0], self.position[1] - 1)
        return self.move_block(new_position)

    def move_left(self):
        new_position = (self.position[0] - 1, self.position[1])
        return self.move_block(new_position)

    def move_right(self):
        new_position = (self.position[0] + 1, self.position[1])
        return self.move_block(new_position)

    def move_block(self, new_position):
        self.hide_current_block()
        if self.can_place(self.block, new_position):
            self.place_block(self.block, new_position)
            self.position = new_position
            return True
        else:
            self.place_block(self.block, self.position)
            return False

    def generate_block(self):
        if len(self.block_pool) == 0:
            self.block_pool = Block.generate_pool()

        return self.block_pool.pop()

    def flash(self, settle=True):
        while self.move_down():
            pass

        if settle:
            self.settle()
            self.start()
            self.gravity_timer = 0

    def rotate(self):
        self.hide_current_block()
        self.block.rotate_cw()
        self.place_block(self.block, jdbjjself.position)

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

        next_fill_row = self.height-1

        for non_empty_row in non_empty_rows:
            self._cut_row_to(non_empty_row, next_fill_row)
            next_fill_row -= 1

    def event(self, event_type):
        self.events.append(event_type)

    def update(self, delta):
        self.gravity_timer += delta

        for event in list(self.events):
            self.events.remove(event)
            if event == 'EXIT':
                return False
            elif event in self.event_to_action:
                self.event_to_action[event]()

        if self.gravity_timer >= 1000:
            self.gravity_timer -= 1000
            moved = self.move_down()

            if not moved:
                self.settle()
                self.start()

        return True

    def find_next_move(self):
        grid_backup = copyopy.deepcopy(self.grid)
        block_backup = self.block.copy()
        position_backup = position

        # TODO find an actual good min here
        best_score = -999
        best_x = 0
        best_rotation = 0

        for num_rotation in range(4):
            self.position = (0, 0)

            for rotation in num_rotation:
                self.block.rotate_cw()

            while self.move_left():
                pass

            for x in range(self.width):
                if self.move_right() == False:
                    break

                self.flash(settle=False)

                # calculate score
                # if better than best score, replace





