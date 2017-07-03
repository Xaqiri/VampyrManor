import pygame as pyg
import colors
from entity import *
import sys
import os

pyg.init()
GAME_VERSION = '0.0.0'
pyg.display.set_caption('Vampyr Manor' + ', version: ' + GAME_VERSION)

SCALE = 4
TILE_DIMENSION = int(8*SCALE)
window_size = window_width, window_height = 1200, 700
SCREEN_CENTER = (window_width//2, window_height//2)
screen_offset = [SCREEN_CENTER[0]-TILE_DIMENSION, SCREEN_CENTER[1]-TILE_DIMENSION]
screen = pyg.display.set_mode(window_size)
dungeon_size = (20, 20)
dungeon = [[0]*dungeon_size[1] for x in range(dungeon_size[0])]
for y in range(dungeon_size[1]):
    for x in range(dungeon_size[0]):
        if (x == 0 or x == dungeon_size[0]-1) or (y == 0 or y == dungeon_size[1]-1):
            dungeon[x][y] = 1
player = Entity(x=1, y=1)
sprites = dict(wall=pyg.image.load(os.path.join('..', 'assets', 'sprites',
                                              'wall.png')).convert(),
               floor=pyg.image.load(os.path.join('..', 'assets', 'sprites',
                                               'floor3.png')).convert(),
               player=pyg.image.load(os.path.join('..', 'assets', 'sprites',
                                                'player.png')).convert(),
               goon=pyg.image.load(os.path.join('..', 'assets', 'sprites',
                                                 'goon.png')).convert())

# Goes through each sprite and sets a certain color to be transparent and scales it to the appropriate dimensions
for i in sprites:
    sprites[i].set_colorkey(colors.TRANS)
    sprites[i] = pyg.transform.scale(sprites[i], (TILE_DIMENSION, TILE_DIMENSION))

def color_sprite(sprite, color):
    new_sprite = sprite.copy()
    new_sprite = pyg.PixelArray(new_sprite)
    new_sprite.replace(colors.BLACK, color)
    new_sprite =  pyg.PixelArray.make_surface(new_sprite)
    new_sprite.set_colorkey(colors.TRANS)
    return new_sprite

def main():
    done = False
    clock = pyg.time.Clock()
    while not done:
        input()
        render()
        clock.tick(60)
    p.quit()

def input():
    global player
    pyg.event.pump()
    for e in pyg.event.get():
        if e.type == pyg.QUIT:
            sys.exit()
        if e.type == pyg.KEYDOWN:
            if e.key == pyg.K_ESCAPE:
                sys.exit()
            if e.key == pyg.K_UP:
                move(0, -1)
            if e.key == pyg.K_DOWN:
                move(0, 1)
            if e.key == pyg.K_LEFT:
                move(-1, 0)
            if e.key == pyg.K_RIGHT:
                move(1, 0)

def render():
    screen.fill(colors.GRAY)
    for y in range(dungeon_size[1]):
        for x in range(dungeon_size[0]):
            if dungeon[x][y] == 1:
                screen.blit(sprites['wall'], (32*x+screen_offset[0], 32*y+screen_offset[1]))
            elif (x == player.x and y == player.y):
                screen.blit(sprites['player'], (32*x+screen_offset[0], 32*y+screen_offset[1]))
            else:
                screen.blit(sprites['floor'], (32*x+screen_offset[0], 32*y+screen_offset[1]))

    pyg.display.flip()

def move(x, y):
    global player, screen_offset
    if (dungeon[player.x + x][player.y + y] != 1):
        player.x = player.x + x
        player.y = player.y + y
        screen_offset = [SCREEN_CENTER[0]-player.x*TILE_DIMENSION, SCREEN_CENTER[1]-player.y*TILE_DIMENSION]

def gen_goon(x, y):
    pass
main()
