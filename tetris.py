import copy
import random
import math
from block import Block
from fitness import calculate_fitness

class Tetris(object):
    width = 8
    height = 22

    def __init__(self, trait_sets):
        self.events = []
        self.init_controls()
        self.reset()
        self.trait_sets = trait_sets

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
        self.color_grid = []
        self.block_pool = []
        self.block = None
        self.position = (0, 0)
        self.gravity_timer = 0
        self.make_move_timer = 0

        for x in range(self.width):
            empty_column = []
            empty_color_column = []
            for y in range(self.height):
                empty_column.append('-')
                empty_color_column.append(None)

            self.grid.append(empty_column)
            self.color_grid.append(empty_color_column)


    def get_cell(self, x, y):
        return self.grid[x][y]

    def get_cell_color(self, x, y):
        return self.color_grid[x][y]

    def place_block(self, block, position):
        for x in range(4):
            for y in range(4):
                if block.get_cell(x, y) == 'x':
                    self.grid[x + position[0]][y + position[1]] = 'x'
                    self.color_grid[x + position[0]][y + position[1]] = block.color

    def _clear_row(self, y):
        for x in range(self.width):
            self.grid[x][y] = '-'
            self.color_grid[x][y] = None

    def _row_is_empty(self, row):
        return 'x' not in self.get_row(row)

    def _copy_row_to(self, row_from, row_to):
        for x in range(self.width):
            self.grid[x][row_to] = self.get_cell(x, row_from)
            self.color_grid[x][row_to] = self.get_cell_color(x, row_from)

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
                    self.color_grid[self.position[0] + x][self.position[1] + y] = None

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
                fitness_score = calculate_fitness(self.grid, self.trait_sets)

                if fitness_score > best_score:
                    best_score = fitness_score
                    best_x = self.position[0]
                    best_rotation = num_rotation

                self.move_block((self.position[0], 0))

                if self.move_right() == False:
                    break

        self.hide_current_block()

        self.position = position_backup
        self.block = block_backup
        self.grid = grid_backup

        return (best_x, best_rotation)

    @classmethod
    def main(self, seed, id, results, trait_sets, visual=False):
        random.seed(seed)
        
        if visual:
            import pygame
            pygame.init()

            TILE_SIZE = 25
             
            WHITE = (255, 255, 255)
            GREEN = (  0, 255,   0)
             
            size = [800, 600]
            screen = pygame.display.set_mode(size)
            pygame.display.set_caption('Tetris AI')
             
            clock = pygame.time.Clock()

        game = Tetris(trait_sets)
        game.start()

        def render(game):
            screen.fill(WHITE)

            x_offset = 0
            for y in range(game.height):
                pygame.draw.rect(screen, GREEN, [x_offset, y * TILE_SIZE, TILE_SIZE, TILE_SIZE])
                pygame.draw.rect(screen, GREEN, [(game.width) * TILE_SIZE + TILE_SIZE + x_offset, y * TILE_SIZE, TILE_SIZE, TILE_SIZE])

            for y in range(game.height):
                for x in range(game.width):
                    cell_color = game.get_cell_color(x, y)

                    if cell_color is None:
                        pygame.draw.rect(screen, WHITE, [x * TILE_SIZE + TILE_SIZE + x_offset, y * TILE_SIZE, TILE_SIZE, TILE_SIZE])
                    else:
                        pygame.draw.rect(screen, cell_color, [x * TILE_SIZE + TILE_SIZE + x_offset, y * TILE_SIZE, TILE_SIZE, TILE_SIZE])

            pygame.display.flip()

        num_updates = 0

        while True:
            if visual:
                clock.tick(10)

            if game.update():
                num_updates += 1
            else:
                break

            if visual:
                render(game)

        print '{} MOVES'.format(num_updates)
        results.put((id, num_updates))

        if visual:
            pygame.quit()

    # [3.2220703467626075, -1.1052026569788542, 1.8884685398230356, -4.420821661782874]: 1162
    # [3.0429925127860025, -0.6826343806600234, 1.8565413754198299, -4.620029833768513]: 1099   
    # Tetris.main(time.time(), 0, DummyQueue(), [1.0899486313285176, -0.00048470297714053867, 2.05484698586114, -2.7296141753723413], True)
