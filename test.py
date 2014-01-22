import pygame
import sys
from math import pi
from tetris import Tetris
 
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
# pygame.key.set_repeat()
 
done = False
clock = pygame.time.Clock()

game = Tetris()
game.start()
# block = game.generate_block()
# block.rotate_ccw()
# block.rotate_ccw()
# game.flash((-1, 0), block)
# game.flash((2, 0), block)
# game.flash((5, 0), block)
# block.rotate_ccw()
# game.flash((7, 0), block)
# game.settle()
# game.print_grid()
# sys.exit()

def handle_keyup(game, key):
    if key == pygame.K_w:
        game.move_up()
    elif key == pygame.K_s:
        game.move_down()
    elif key == pygame.K_a:
        game.move_left()
    elif key == pygame.K_d:
        game.move_right()
    elif key == pygame.K_ESCAPE:
        return False

    return True
 
while not done:
    clock.tick(60)

    # game.generate_block()
    # game.flash()
    # game.print_grid()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYUP:
            if not handle_keyup(game, event.key):
                done = True

    screen.fill(WHITE)

    x_offset = 0

    for y in range(game.height):
        pygame.draw.rect(screen, GREEN, [x_offset, y * TILE_SIZE, TILE_SIZE, TILE_SIZE])
        pygame.draw.rect(screen, GREEN, [(game.width + 1) * TILE_SIZE + x_offset, y * TILE_SIZE, TILE_SIZE, TILE_SIZE])

    for y in range(game.height):
        for x in range(game.width):
            if game.get_cell(x, y) == '-':
                pygame.draw.rect(screen, WHITE, [x * TILE_SIZE + TILE_SIZE + x_offset, y * TILE_SIZE, TILE_SIZE, TILE_SIZE])
            elif game.get_cell(x, y) == 'x':
                pygame.draw.rect(screen, BLACK, [x * TILE_SIZE + TILE_SIZE + x_offset, y * TILE_SIZE, TILE_SIZE, TILE_SIZE])

    pygame.display.flip()
 
pygame.quit()