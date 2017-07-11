import sys
import os
import pygame as pyg
import pyRL.colors as colors
import pyRL.random_level_gen as rlg
import pyRL.fov as fov
import pyRL.panel as panel
from entity import *

# TODO
'''
Setup method to read in external files that contain  definitions for things like the map, enemies, and items
Make dungeon size unrelated to window size
Make dungeon stationary if it fits in the window, scroll otherwise
'''

pyg.init()
GAME_VERSION = '0.0.0'
pyg.display.set_caption('Vampyr Manor' + ', version: ' + GAME_VERSION)

font_size = 24
ui_font = pyg.font.SysFont('consolas', font_size)
fps_counter = 0

SCALE = 2
TILE_DIMENSION = int(8*SCALE)
WIN_WIDTH = 800*SCALE
WIN_HEIGHT = 480*SCALE
window_size = WIN_WIDTH, WIN_HEIGHT
SCREEN_CENTER = (WIN_WIDTH//2, WIN_HEIGHT//2)
screen = pyg.display.set_mode(window_size)
game_panel = panel.Panel(screen=screen, origin=(0, 0), width=WIN_WIDTH*.6, height=WIN_HEIGHT, fg_color=colors.Colors.PURPLE, bg_color=colors.Colors.BLACK, visible=True)
inventory_panel = panel.Panel(screen=screen, origin=(WIN_WIDTH*.6, 0), width=WIN_WIDTH*.2, height=WIN_HEIGHT*.40, fg_color=colors.Colors.PURPLE, bg_color=colors.Colors.DRK_GREEN, visible=True, name='Inventory')
char_stats_panel = panel.Panel(screen=screen, origin=(WIN_WIDTH*.8, 0), width=WIN_WIDTH*.2, height=WIN_HEIGHT*.40, fg_color=colors.Colors.PURPLE, bg_color=colors.Colors.DRK_PURPLE, visible=True, name='Stats')
party_panel = panel.Panel(screen=screen, origin=(WIN_WIDTH*.6, WIN_HEIGHT*.4), width=WIN_WIDTH*.4, height=WIN_HEIGHT*.4, fg_color=colors.Colors.PURPLE, bg_color=colors.Colors.DRK_BLUE, visible=True, name='Party')
message_panel = panel.Panel(screen=screen, origin=(WIN_WIDTH*.6, WIN_HEIGHT*.80), width=WIN_WIDTH*.4, height=WIN_HEIGHT*.2, fg_color=colors.Colors.PURPLE, bg_color=colors.Colors.DRK_YELLOW, visible=True, name='Message Log')
panels = [inventory_panel, message_panel, party_panel, char_stats_panel]
# Dungeon size is based on a scale of 2
# 75% of the width of the window / 16px/tile = 75 tiles
# 7/8 (87.5%) of the height of the window / 16px/tile = 49 tiles
dungeon_size = (60, 60)
dungeon = 0
player = Entity(x=1, y=1)
entities = [player]
player_took_turn = False
fov = fov.FOV(vision_range=5)
colors = colors.Colors()

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

def make_map():
    global dungeon, dungeon_size, fov, entities
    dungeon = 0
    fov.explored_tiles = []
    dungeon = rlg.RandomLevelGen(level_width=dungeon_size[0], level_height=dungeon_size[1], max_rooms=150, room_min_size=4, room_max_size=8)
    dungeon.make_level(entities)

    # Display entire level.  Will make this an option in pyRL in the
    # future
    for y in range(dungeon_size[1]):
        for x in range(dungeon_size[0]):
            fov.explored_tiles.append((x, y))


def main():
    done = False
    clock = pyg.time.Clock()
    make_map()
    fov.update(entities=entities, level=dungeon.level)
    while not done:
        input()
        update(clock)
        render()
        clock.tick(60)
    p.quit()

def input():
    global player, player_took_turn
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
            if e.key == pyg.K_r:
                make_map()
            player_took_turn = True

def update(clock):
    global screen_offset, player, fps_counter, fov, entities, dungeon, player_took_turn
    if player_took_turn:
        fov.update(entities=entities, level=dungeon.level)
        player_took_turn = False
    #screen_offset = [SCREEN_CENTER[0]-player.x*TILE_DIMENSION, SCREEN_CENTER[1]-player.y*TILE_DIMENSION]
    screen_offset = game_panel.origin
    fps_counter = clock.get_fps()

def render():
    global fov
    screen.fill(colors.BLACK)
    explored_wall = color_sprite(sprites['wall'], colors.RED)
    explored_floor = color_sprite(sprites['floor'], colors.DRK_RED)
    visible_wall = color_sprite(sprites['wall'], colors.GRAY)
    visible_floor = color_sprite(sprites['floor'], colors.DRK_GRAY)
    player_sprite = color_sprite(sprites['player'], colors.BLU_GRY)
    game_panel.render(ui_font)
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
            screen.blit(player_sprite, (TILE_DIMENSION*v[0]+screen_offset[0], TILE_DIMENSION*v[1]+screen_offset[1]))

    for p in panels:
        p.render(ui_font)
    render_fps(fps_counter)
    pyg.display.flip()

def move(x, y):
    global player
    if (dungeon.level[player.x + x][player.y + y] != 1):
        player.x = player.x + x
        player.y = player.y + y

def gen_goon(x, y):
    pass

def render_fps(fps_counter):
    pyg.draw.rect(screen, colors.BLACK, ((0, 0), (72, 24)))
    screen.blit(ui_font.render(str(('{:.2f}'.format(fps_counter))), 1, colors.GREEN), (0, 0))

main()
