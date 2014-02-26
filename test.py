import random
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
 
done = False
clock = pygame.time.Clock()

game = Tetris(True)
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
    render(game)
    raw_input()
    if game.update(1000):
        num_updates += 1
    else:
        break
    render(game)
print '{} UPDATES'.format(num_updates)

pygame.quit()
