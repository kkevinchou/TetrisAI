import pygame
import sys
from math import pi
from tetris import Tetris
 
pygame.init()
 
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE =  (  0,   0, 255)
GREEN = (  0, 255,   0)
RED =   (255,   0,   0)
 
size = [400, 300]
# screen = pygame.display.set_mode(size)
# pygame.display.set_caption('Tetris AI')
 
done = False
clock = pygame.time.Clock()

game = Tetris()
block = game.generate_block()
block.rotate_ccw()
block.rotate_ccw()
game.flash((-1, 0), block)
game.flash((2, 0), block)
game.flash((5, 0), block)
block.rotate_ccw()
game.flash((7, 0), block)
game.settle()
game.print_grid()
sys.exit()
 
while not done:
    clock.tick(1)

    game.generate_block()
    game.flash()
    game.print_grid()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print 'meow'
            done = True

    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        done = True

    screen.fill(WHITE)
    pygame.draw.rect(screen, BLACK, [150, 10, 50, 20])
    pygame.display.flip()
 
pygame.quit()