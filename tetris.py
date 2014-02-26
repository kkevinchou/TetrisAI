import copy
import random
import math
from block import Block
from fitness import calculate_fitness

class Tetris(object):
    width = 8
    height = 22

    def __init__(self, read_grid=False):
        self.events = []
        self.init_controls()
        self.reset()

        if read_grid:
            with open('grid.dat') as f:
                y = 0
                for line in f:
                    if len(line) < self.width:
                        break

                    x = 0
                    for cell in line:
                        if cell == 'x':
                            self.grid[x][y] = 'x'
                        x += 1
                    y += 1

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
        self.make_move_timer = 0

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

        if self.can_place(self.block, self.position):
            self.place_block(self.block, self.position)
            return True

        return False

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

    def flash(self):
        while self.move_down():
            pass

    def rotate(self):
        self.hide_current_block()
        self.block.rotate_cw()
        self.place_block(self.block, self.position)

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

    def update(self):
        self.make_move()
        self.settle()
        if not self.start():
            return False

        return True

    def make_move(self):
        x_movement, num_rotations = self.find_next_move()

        if x_movement < 0:
            move_function = self.move_left
        else:
            move_function = self.move_right

        for i in range(num_rotations):
            self.rotate()
            
        for i in range(int(math.fabs(x_movement))):
            move_function()

        self.flash()

    def find_next_move(self):
        grid_backup = copy.deepcopy(self.grid)
        block_backup = self.block.copy()
        position_backup = self.position

        # TODO find an actual good min here
        best_score = -999
        best_x = 0
        best_rotation = 0

        for num_rotation in range(4):
            self.move_block((0, 0))

            if num_rotation > 0:
                self.rotate()

            while self.move_left():
                pass

            for x in range(self.width):
                self.flash()
                fitness_score = calculate_fitness(self.grid, [4, -4, 3.5, -10])
                # print (self.position[0], num_rotation, fitness_score)

                if fitness_score > best_score:
                    best_score = fitness_score
                    best_x = self.position[0]
                    best_rotation = num_rotation

                self.move_block((self.position[0], 0))

                if self.move_right() == False:
                    break

        self.position = position_backup
        self.block = block_backup
        self.grid = grid_backup

        # print (best_x, best_rotation, best_score)
        return (best_x, best_rotation)

    @classmethod
    def main(self):
        import random
        import pygame
        import sys
        from math import pi
         
        pygame.init()

        TILE_SIZE = 25
         
        BLACK = (  0,   0,   0)
        WHITE = (255, 255, 255)
        BLUE =  (  0,   0, 255)
        GREEN = (  0, 255,   0)
        RED =   (255,   0,   0)
         
        size = [800, 600]
        screen = pygame.display.set_mode(size)
        pygame.display.set_caption('Tetris AI')
         
        done = False
        clock = pygame.time.Clock()

        game = Tetris()
        game.start()

        def get_event_type(key):
            if key == pygame.K_w:
                return 'FLASH'
            elif key == pygame.K_s:
                return 'DOWN'
            elif key == pygame.K_a:
                return 'LEFT'
            elif key == pygame.K_d:
                return 'RIGHT'
            elif key == pygame.K_ESCAPE:
                return 'EXIT'
            elif key == pygame.K_j:
                return 'ROTATE'

            return None

        def render(game):
            screen.fill(WHITE)

            x_offset = 0
            for y in range(game.height):
                pygame.draw.rect(screen, GREEN, [x_offset, y * TILE_SIZE, TILE_SIZE, TILE_SIZE])
                pygame.draw.rect(screen, GREEN, [(game.width) * TILE_SIZE + TILE_SIZE + x_offset, y * TILE_SIZE, TILE_SIZE, TILE_SIZE])

            for y in range(game.height):
                for x in range(game.width):
                    if game.get_cell(x, y) == '-':
                        pygame.draw.rect(screen, WHITE, [x * TILE_SIZE + TILE_SIZE + x_offset, y * TILE_SIZE, TILE_SIZE, TILE_SIZE])
                    elif game.get_cell(x, y) == 'x':
                        pygame.draw.rect(screen, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), [x * TILE_SIZE + TILE_SIZE + x_offset, y * TILE_SIZE, TILE_SIZE, TILE_SIZE])

            pygame.display.flip()

        num_updates = 0
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                elif event.type == pygame.KEYDOWN:
                    event_type = get_event_type(event.key)
                    if event_type is not None:
                        game.event(event_type)

            if game.update():
                num_updates += 1
            else:
                break

            render(game)

        print '{} UPDATES'.format(num_updates)

        pygame.quit()

if __name__ == '__main__':
    Tetris.main()
