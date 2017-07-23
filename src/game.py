import sys
import os
import pygame as pyg
import pyRL.colors as colors
import pyRL.random_level_gen as rlg
import pyRL.fov
import pyRL.panel as panel
from entity import *

# TODO
'''
Setup method to read in external files that contain  definitions for things like the map, enemies, and items
'''

pyg.init()
GAME_VERSION = '0.0.0'
pyg.display.set_caption('Vampyr Manor' + ', version: ' + GAME_VERSION)

font_size = 24
ui_font = pyg.font.SysFont('consolas', font_size)

SCALE = 2
TILE_DIMENSION = int(8*SCALE)
WIN_WIDTH = 1600
WIN_HEIGHT = 960
WIN_SIZE = WIN_WIDTH, WIN_HEIGHT
GAME_PANEL_SIZE = WIN_WIDTH*.75, WIN_HEIGHT
GAME_PANEL_CENTER = (GAME_PANEL_SIZE[0]//2, GAME_PANEL_SIZE[1]//2)
DUNGEON_SIZE = (200, 200)
NUM_X_TILES = int(GAME_PANEL_SIZE[0]/TILE_DIMENSION)
NUM_Y_TILES = int(GAME_PANEL_SIZE[1]/TILE_DIMENSION)
UI_PANEL_SIZE = WIN_WIDTH*.25, WIN_HEIGHT
FOV_MODE = 'unexplored'
screen = pyg.display.set_mode(WIN_SIZE)
colors = colors.Colors()

""" PANELS """
game_panel = panel.Panel(screen=screen, origin=(0, 0), size=GAME_PANEL_SIZE, fg_color=colors.PURPLE, bg_color=colors.BLACK, visible=True)
ui_panel = panel.Panel(screen=screen, origin=(GAME_PANEL_SIZE[0], 0), size=UI_PANEL_SIZE, fg_color=colors.PURPLE, bg_color=colors.BLACK, visible=True)
inventory_panel = panel.Panel(screen=screen, origin=ui_panel.origin, size=(ui_panel.size[0]*.5, ui_panel.size[1]*.35), fg_color=colors.PURPLE, bg_color=colors.DRK_GREEN, visible=True, name='Inventory')
char_stats_panel = panel.Panel(screen=screen, origin=(ui_panel.origin[0]+inventory_panel.size[0], 0), size=(ui_panel.size[0]*.5, ui_panel.size[1]*.35), fg_color=colors.PURPLE, bg_color=colors.DRK_PURPLE, visible=True, name='Stats')
party_panel = panel.Panel(screen=screen, origin=(ui_panel.origin[0], ui_panel.origin[1]+inventory_panel.size[1]), size=(ui_panel.size[0], ui_panel.size[1]*.35), fg_color=colors.PURPLE, bg_color=colors.DRK_BLUE, visible=True, name='Party')
message_panel = panel.Panel(screen=screen, origin=(ui_panel.origin[0], party_panel.origin[1]+party_panel.size[1]), size=(ui_panel.size[0], ui_panel.size[1]*.3), fg_color=colors.PURPLE, bg_color=colors.DRK_YELLOW, visible=True, name='Message Log')
panels = [game_panel, ui_panel, inventory_panel, char_stats_panel, party_panel, message_panel]

sprites = dict(wall=pyg.image.load(os.path.join('..', 'assets', 'sprites',
                                              'wall2.png')).convert(),
               wall2=pyg.image.load(os.path.join('..', 'assets', 'sprites',
                                                     'wall2.png')).convert(),
               floor=pyg.image.load(os.path.join('..', 'assets', 'sprites',
                                               'wall2.png')).convert(),
               player=pyg.image.load(os.path.join('..', 'assets', 'sprites',
                                                'player.png')).convert(),
               goon=pyg.image.load(os.path.join('..', 'assets', 'sprites',
                                                 'goon.png')).convert())

# Goes through each sprite and sets a certain color to be transparent and scales it to the appropriate dimensions
for i in sprites:
    sprites[i].set_colorkey(colors.TRANS)
    sprites[i] = pyg.transform.scale(sprites[i], (TILE_DIMENSION, TILE_DIMENSION))

def main():
    tile_colors = dict(
        unexplored_tile = color_sprite(sprites['wall2'], colors.DRKR_GRAY),
        explored_wall = color_sprite(sprites['wall2'], colors.RED),
        explored_floor = color_sprite(sprites['floor'], colors.DRK_RED),
        visible_wall = color_sprite(sprites['wall'], colors.GRAY),
        visible_floor = color_sprite(sprites['floor'], colors.DRK_GRAY),
        player_sprite = color_sprite(sprites['player'], colors.BLU_GRY)
    )
    player_took_turn = False

    player = Entity(x=1, y=1)
    entities = [player]

    fov = pyRL.fov.FOV(vision_range=10, level_width=DUNGEON_SIZE[0], level_height=DUNGEON_SIZE[1], fov_mode=FOV_MODE)
    dungeon = make_map(fov, DUNGEON_SIZE, entities)

    fov.update(entities=entities, level=dungeon.level)
    screen_offset = (0, 0)
    mode = 'nonscroll'
    done = False
    clock = pyg.time.Clock()
    fps_counter = 0
    while not done:
        player_took_turn, dungeon = input(dungeon, player, player_took_turn, fov, DUNGEON_SIZE, entities)
        fps_counter, player_took_turn, mode = update(clock, player_took_turn, fps_counter, fov, entities, dungeon)
        render(fov, dungeon, player, fps_counter, tile_colors)
        clock.tick(60)
    p.quit()

def color_sprite(sprite, color):
    new_sprite = sprite.copy()
    new_sprite = pyg.PixelArray(new_sprite)
    new_sprite.replace(colors.BLACK, color)
    new_sprite =  pyg.PixelArray.make_surface(new_sprite)
    new_sprite.set_colorkey(colors.TRANS)
    return new_sprite

def make_map(fov, DUNGEON_SIZE, entities):
    dungeon = 0
    fov.clear()
    dungeon = rlg.RandomLevelGen(level_width=DUNGEON_SIZE[0], level_height=DUNGEON_SIZE[1], max_rooms=600, room_min_size=4, room_max_size=12)
    dungeon.make_level(entities)
    return dungeon

def input(dungeon, player, player_took_turn, fov, DUNGEON_SIZE, entities):
    pyg.event.pump()
    for e in pyg.event.get():
        if e.type == pyg.QUIT:
            sys.exit()
        if e.type == pyg.KEYDOWN:
            if e.key == pyg.K_ESCAPE:
                sys.exit()
            if e.key == pyg.K_UP:
                move(dungeon, player, 0, -1)
            if e.key == pyg.K_DOWN:
                move(dungeon, player, 0, 1)
            if e.key == pyg.K_LEFT:
                move(dungeon, player, -1, 0)
            if e.key == pyg.K_RIGHT:
                move(dungeon, player, 1, 0)
            if e.key == pyg.K_r:
                dungeon = make_map(fov, DUNGEON_SIZE, entities)
            player_took_turn = True
    return player_took_turn, dungeon

def update(clock, player_took_turn, fps_counter, fov, entities, dungeon):
    global screen_offset
    if NUM_X_TILES < dungeon.size[0] or NUM_Y_TILES < dungeon.size[1]:
        mode = 'scroll'
    else:
        mode = 'nonscroll'
    if player_took_turn:
        fov.update(entities=entities, level=dungeon.level)
        player_took_turn = False
    if mode == 'scroll':
        screen_offset = [GAME_PANEL_CENTER[0]-entities[0].x*TILE_DIMENSION, GAME_PANEL_CENTER[1]-entities[0].y*TILE_DIMENSION]
    elif mode == 'nonscroll':
        screen_offset = game_panel.origin
    return clock.get_fps(), player_took_turn, mode

def render(fov, dungeon, player, fps_counter, tile_colors):
    global screen_offset
    screen.fill(colors.BLACK)
    for p in panels:
        p.render(ui_font)

    # Draw explored tiles
    y_min_range = player.y-NUM_Y_TILES//2 if player.y-NUM_Y_TILES//2 > 0 else 0
    y_max_range = min(player.y+NUM_Y_TILES//2, dungeon.level_height) if NUM_Y_TILES < dungeon.level_height else dungeon.level_height
    x_min_range = player.x-NUM_X_TILES//2 if player.x-NUM_X_TILES//2 > 0 else 0
    x_max_range = min(player.x+NUM_X_TILES//2, dungeon.level_width) if NUM_X_TILES < dungeon.level_width else dungeon.level_width
    for y in range(y_min_range, y_max_range):
        for x in range(x_min_range, x_max_range):
            if fov.explored_tiles[x][y] == 1:
                if dungeon.level[x][y] == 1:
                    screen.blit(tile_colors['explored_wall'], (TILE_DIMENSION*x+screen_offset[0], TILE_DIMENSION*y+screen_offset[1]))
                else:
                    screen.blit(tile_colors['explored_floor'], (TILE_DIMENSION*x+screen_offset[0], TILE_DIMENSION*y+screen_offset[1]))
            else:
                screen.blit(tile_colors['unexplored_tile'], (TILE_DIMENSION*x+screen_offset[0], TILE_DIMENSION*y+screen_offset[1]))
    for v in fov.visible_tiles:
        if tile_in_bounds(v):
            if dungeon.level[v[0]][v[1]] == 1:
                screen.blit(tile_colors['visible_wall'], (TILE_DIMENSION*v[0]+screen_offset[0], TILE_DIMENSION*v[1]+screen_offset[1]))
            else:
                screen.blit(tile_colors['visible_floor'], (TILE_DIMENSION*v[0]+screen_offset[0], TILE_DIMENSION*v[1]+screen_offset[1]))
            if (v == (player.x, player.y)):
                screen.blit(tile_colors['player_sprite'], (TILE_DIMENSION*v[0]+screen_offset[0], TILE_DIMENSION*v[1]+screen_offset[1]))

    render_fps(fps_counter)
    pyg.display.flip()

def tile_in_bounds(tile):
    global screen_offset
    if TILE_DIMENSION*tile[0]+screen_offset[0]+TILE_DIMENSION < GAME_PANEL_SIZE[0] and TILE_DIMENSION*tile[1]+screen_offset[1] < GAME_PANEL_SIZE[1]:
        return True
    return False

def move(dungeon, player, x, y):
    if (dungeon.level[player.x + x][player.y + y] != 1):
        player.x = player.x + x
        player.y = player.y + y

def gen_goon(x, y):
    pass

def render_fps(fps_counter):
    pyg.draw.rect(screen, colors.BLACK, ((0, 0), (72, 24)))
    screen.blit(ui_font.render(str(('{:.2f}'.format(fps_counter))), 1, colors.GREEN), (0, 0))

main()
