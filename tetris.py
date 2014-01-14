class Tetris(object):
    width = 10
    height = 22

    def __init__(self):
        self.grid = []

        for y in range(self.height):
            empty_row = []
            for x in range(self.width):
                empty_row.append('-')
            self.grid.append(empty_row)

    def _get_cell(self, y, x):
        return self.grid[y][x]

    def _get_collision_y(self, x):
        for y in range(self.height, 0, -1):
            if _get_cell(y, x) == '-':
                return y

    def _place_block(self, block, position):
        for y in range(3):
            for x in range(3):
                self.grid[y + position[0]][x + position[1]] = block.get_cell(y, x)

    def _clear_row(self, y):
        for x in range(self.width):
            self.grid[y][x] = '-'

    def _row_is_empty(self, y):
        for x in range(self.width):
            if self.grid[y][x] == 'x'
                return False

        return True

    def _copy_row_to(self, row_start, row_end):
        for x in range(width):
            self.grid[row_end][x] = self._get_cell(row_start, x)

    def flash(self, position, block):
        collision_y = 99 # TODO: actually find a good initial value here

        for y in range(3):
            for x in range(3):
                if block.get_cell(y, x) == 'x':
                    collision_y = min(self._get_collision_y(y + position[0]), collision_y)

        self._place_block((collision_y, position[1]), block)

    def settle(self):
        for y in range(self.height, 0, -1):
            filled_row = True
            
            for x in range(self.width):
                if self._get_cell(y, x) == '-':
                    filled_row = False
                    break

            if filled_row:
                self._clear_row(y)

        top = self.height - 1
        for y in range(self.height, 0, -1):
            if self._row_is_empty(y):



