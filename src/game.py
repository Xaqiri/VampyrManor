import sys
import os
import pygame as pyg
import pyRL.colors as colors
import pyRL.random_level_gen as rlg
import pyRL.fov as fov

from entity import *

pyg.init()
GAME_VERSION = '0.0.0'
pyg.display.set_caption('Vampyr Manor' + ', version: ' + GAME_VERSION)

font_size = 16
ui_font = pyg.font.SysFont('consolas', font_size)
fps_counter = 0

SCALE = 4
TILE_DIMENSION = int(8*SCALE)
window_size = window_width, window_height = 1600, 900
SCREEN_CENTER = (window_width//2, window_height//2)
screen = pyg.display.set_mode(window_size)
dungeon_size = (32, 32)
player = Entity(x=1, y=1)
entities = [player]
fov = fov.FOV()
colors = colors.Colors()
dungeon = rlg.RandomLevelGen(level_width=dungeon_size[0], level_height=dungeon_size[1], max_rooms=100, room_min_size=4, room_max_size=6)
dungeon.make_level(entities)
sprites = dict(wall=pyg.image.load(os.path.join('..', 'assets', 'sprites',
                                              'wall.png')).convert(),
               floor=pyg.image.load(os.path.join('..', 'assets', 'sprites',
                                               'floor.png')).convert(),
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
        update(clock)
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

def update(clock):
    global screen_offset, player, fps_counter, fov, entities, dungeon
    fov.update(entities=entities, level=dungeon.level)
    screen_offset = [SCREEN_CENTER[0]-player.x*TILE_DIMENSION, SCREEN_CENTER[1]-player.y*TILE_DIMENSION]
    fps_counter = clock.get_fps()

def render():
    global fov
    screen.fill(colors.DRK_GRAY)
    explored_wall = color_sprite(sprites['wall'], colors.DRK_BLUE)
    explored_floor = color_sprite(sprites['floor'], colors.BLUE)
    visible_wall = color_sprite(sprites['wall'], colors.DRK_YELLOW)
    visible_floor = color_sprite(sprites['floor'], colors.YELLOW)
    for ex in fov.explored_tiles:
        if dungeon.level[ex[0]][ex[1]] == 1:
            screen.blit(explored_wall, (TILE_DIMENSION*ex[0]+screen_offset[0], TILE_DIMENSION*ex[1]+screen_offset[1]))
        else:
            screen.blit(explored_floor, (TILE_DIMENSION*ex[0]+screen_offset[0], TILE_DIMENSION*ex[1]+screen_offset[1]))
    for v in fov.visible_tiles:
        if dungeon.level[v[0]][v[1]] == 1:
            screen.blit(visible_wall, (TILE_DIMENSION*v[0]+screen_offset[0], TILE_DIMENSION*v[1]+screen_offset[1]))
        else:
            screen.blit(visible_floor, (TILE_DIMENSION*v[0]+screen_offset[0], TILE_DIMENSION*v[1]+screen_offset[1]))
        if (v == (player.x, player.y)):
            screen.blit(sprites['player'], (TILE_DIMENSION*v[0]+screen_offset[0], TILE_DIMENSION*v[1]+screen_offset[1]))

    screen.blit(ui_font.render(str(('{:.2f}'.format(fps_counter))), 1, colors.GREEN), (0, 0))
    pyg.display.flip()

def move(x, y):
    global player, screen_offset
    if (dungeon.level[player.x + x][player.y + y] != 1):
        player.x = player.x + x
        player.y = player.y + y

def gen_goon(x, y):
    pass
main()
