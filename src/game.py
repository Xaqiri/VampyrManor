import pygame as pyg
import sys
import os

pyg.init()
GAME_VERSION = '0.0.0'
pyg.display.set_caption(' Vampyr Manor' + ', version: ' + GAME_VERSION)

''' Colors '''
TRANS = (255, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)

SCALE = 4
TILE_DIMENSION = int(8*SCALE)
window_size = window_width, window_height = 1200, 700
SCREEN_CENTER = (window_width//2, window_height//2)
screen = pyg.display.set_mode(window_size)
font_size = 8
fonts = ['palatino', 'consolas', 'courier', 'terminal']
sprites = dict(wall=pyg.image.load(os.path.join('..', 'assets', 'sprites',
                                              'wall.png')).convert(),
               floor=pyg.image.load(os.path.join('..', 'assets', 'sprites',
                                               'floor.png')).convert(),
               player=pyg.image.load(os.path.join('..', 'assets', 'sprites',
                                                'player.png')).convert())

# Goes through each sprite and sets a certain color to be transparent and scales it to the appropriate dimensions
for i in sprites:
    sprites[i].set_colorkey(TRANS)
    sprites[i] = pyg.transform.scale(sprites[i], (TILE_DIMENSION, TILE_DIMENSION))

dungeon = [[0]*10 for y in range(10)]

done = False
clock = pyg.time.Clock()

while not done:
    for e in pyg.event.get():
        if e.type == pyg.QUIT:
            sys.exit()
        if e.type == pyg.KEYDOWN:
            if e.key == pyg.K_ESCAPE:
                sys.exit()
    screen.fill(GRAY)
    for y in range(10):
        for x in range(10):
            if (x == 0 or x == 9) or (y == 0 or y == 9):
                screen.blit(sprites['wall'], (32*x, 32*y))
            elif (x == 4 and y == 4):
                screen.blit(sprites['player'], (32*x, 32*y))
            else:
                screen.blit(sprites['floor'], (32*x, 32*y))

    pyg.display.flip()
    clock.tick(60)

p.quit()
