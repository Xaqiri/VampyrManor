import math
import sys
import os
import random
import pygame as pyg
import pyRL.colors as colors
import pyRL.random_level_gen as rlg
import pyRL.fov
import pyRL.panel as panel
from entity import *
import monsters
import sprite 

# TODO
'''
Setup method to read in external files that contain definitions for things like the map, enemies, and items
Add options for starting the game explored/unexplored
Add autoexplore
Add enemy movement
Add combat
Add items
BUG - Enemies can spawn on player. Fix in pyRL.RandomLevelGen.make_level
BUG - Messages don't scroll properly, cutting off the bottom message
'''

pyg.init()
GAME_VERSION = '0.0.0'
pyg.display.set_caption('Vampyr Manor' + ', version: ' + GAME_VERSION)
pyg.key.set_repeat(300, 50)

FONT_SIZE = 32
ui_font = pyg.font.SysFont('consolas', FONT_SIZE)

SCALE = 2
TILE_DIMENSION = int(8*SCALE)
WIN_WIDTH = 1200
WIN_HEIGHT = 600
WIN_SIZE = WIN_WIDTH, WIN_HEIGHT
GAME_PANEL_SIZE = WIN_WIDTH*.75, WIN_HEIGHT
GAME_PANEL_CENTER = (GAME_PANEL_SIZE[0]//2, GAME_PANEL_SIZE[1]//2)
DUNGEON_SIZE = (200, 200)
NUM_X_TILES = int(GAME_PANEL_SIZE[0]/TILE_DIMENSION)
NUM_Y_TILES = int(GAME_PANEL_SIZE[1]/TILE_DIMENSION)
MAX_ENEMIES_PER_ROOM = 4
UI_PANEL_SIZE = WIN_WIDTH*.25, WIN_HEIGHT
FOV_MODE = 'unexplored'
TEXT_SPACING = ui_font.get_linesize()

screen = pyg.display.set_mode(WIN_SIZE)
colors = colors.Colors()
messages = []
message_render_offset = 0

""" PANELS """
game_panel = panel.Panel(screen=screen, origin=(0, 0), size=GAME_PANEL_SIZE, fg_color=colors.PURPLE, bg_color=colors.BLACK, visible=True)
ui_panel = panel.Panel(screen=screen, origin=(GAME_PANEL_SIZE[0], 0), size=UI_PANEL_SIZE, fg_color=colors.PURPLE, bg_color=colors.BLACK, visible=True)
inventory_panel = panel.Panel(screen=screen, origin=ui_panel.origin, size=(ui_panel.size[0]*.5, ui_panel.size[1]*.35), fg_color=colors.PURPLE, bg_color=colors.DRK_GREEN, visible=True, name='Inventory')
char_stats_panel = panel.Panel(screen=screen, origin=(ui_panel.origin[0]+inventory_panel.size[0], 0), size=(ui_panel.size[0]*.5, ui_panel.size[1]*.35), fg_color=colors.PURPLE, bg_color=colors.DRK_PURPLE, visible=True, name='Stats')
party_panel = panel.Panel(screen=screen, origin=(ui_panel.origin[0], ui_panel.origin[1]+inventory_panel.size[1]), size=(ui_panel.size[0], ui_panel.size[1]*.35), fg_color=colors.PURPLE, bg_color=colors.DRK_BLUE, visible=True, name='Party')
message_panel = panel.Panel(screen=screen, origin=(ui_panel.origin[0], party_panel.origin[1]+party_panel.size[1]), size=(ui_panel.size[0], ui_panel.size[1]*.3), fg_color=colors.PURPLE, bg_color=colors.DRKR_GRAY, visible=True, name='Message Log')
panels = [game_panel, ui_panel, inventory_panel, char_stats_panel, party_panel, message_panel]
MAX_MESSAGES = math.floor(message_panel.size[1] / TEXT_SPACING)

def main():
    sprites = sprite.load_sprites(colors, TILE_DIMENSION)

    player_took_turn = False
    player = monsters.generate_player(1, 1, sprites['player_sprite'])
    entities = [player]
    fov = pyRL.fov.FOV(vision_range=8, level_width=DUNGEON_SIZE[0], level_height=DUNGEON_SIZE[1], fov_mode=FOV_MODE)
    dungeon = make_map(fov, DUNGEON_SIZE, entities, MAX_ENEMIES_PER_ROOM, sprites)

    fov.update(entities=dungeon.entities, level=dungeon.level)
    screen_offset = (0, 0)
    done = False
    clock = pyg.time.Clock()
    fps_counter = 0

    while not done:
        player_took_turn, dungeon = input(dungeon, player, player_took_turn, fov, DUNGEON_SIZE, sprites)
        fps_counter, player_took_turn = update(clock, player_took_turn, fps_counter, fov, dungeon)
        render(fov, dungeon, player, fps_counter, sprites)
        clock.tick(60)
    pyg.quit()

def spawn_enemies(dungeon, sprites):
    for i in range(1, len(dungeon.entities)):
        chance = random.randrange(10)
        if chance < 8:
            enemy = monsters.generate_rat(dungeon.entities[i][0], dungeon.entities[i][1], sprites['rat_sprite'])
        else:
            enemy = monsters.generate_bat(dungeon.entities[i][0], dungeon.entities[i][1], sprites['bat_sprite'])
        dungeon.entities[i] = enemy

def make_map(fov, DUNGEON_SIZE, entities, MAX_ENEMIES_PER_ROOM, sprites):
    global messages, message_render_offset
    dungeon = 0
    fov.clear()
    messages = []
    message_render_offset = 0
    message('Welcome to Vampyr Manor', colors.BLUE)
    dungeon = rlg.RandomLevelGen(level_width=DUNGEON_SIZE[0], level_height=DUNGEON_SIZE[1], max_rooms=600, room_min_size=4, room_max_size=12, entities=entities)
    dungeon.make_level(MAX_ENEMIES_PER_ROOM=MAX_ENEMIES_PER_ROOM)
    spawn_enemies(dungeon, sprites)
    return dungeon

def input(dungeon, player, player_took_turn, fov, DUNGEON_SIZE, sprites):
    global message_render_offset
    pyg.event.pump()
    ends_turn = True
    for e in pyg.event.get():
        if e.type == pyg.QUIT:
            sys.exit()
        if e.type == pyg.KEYDOWN:
            if e.key == pyg.K_ESCAPE:
                sys.exit()
            if e.key == pyg.K_UP:
                message_render_offset += TEXT_SPACING if message_render_offset / TEXT_SPACING < 0 else 0
                ends_turn = False
            if e.key == pyg.K_DOWN:
                message_render_offset -= TEXT_SPACING if len(messages)*TEXT_SPACING+message_render_offset > MAX_MESSAGES*TEXT_SPACING else 0
                ends_turn = False
            if e.key == pyg.K_KP1 or e.key == pyg.K_z:
                move(dungeon, player, sprites, -1, 1)
            if e.key == pyg.K_KP2 or e.key == pyg.K_x:
                move(dungeon, player, sprites, 0, 1)
            if e.key == pyg.K_KP3 or e.key == pyg.K_c:
                move(dungeon, player, sprites, 1, 1)
            if e.key == pyg.K_KP4 or e.key == pyg.K_a:
                move(dungeon, player, sprites, -1, 0)
            if (e.key == pyg.K_KP5 or e.key == pyg.K_s):
                message('You idle for a moment', colors.WHITE)    
            if e.key == pyg.K_KP6 or e.key == pyg.K_d:
                move(dungeon, player, sprites, 1, 0)
            if e.key == pyg.K_KP7 or e.key == pyg.K_q:
                move(dungeon, player, sprites, -1, -1)
            if e.key == pyg.K_KP8 or e.key == pyg.K_w:
                move(dungeon, player, sprites, 0, -1)
            if e.key == pyg.K_KP9 or e.key == pyg.K_e:
                move(dungeon, player, sprites, 1, -1)
            if e.key == pyg.K_v:
                message('You now have {0} xp'.format(player.xp), colors.DRK_GREEN)
            if e.key == pyg.K_l:
                p = dungeon.entities[0]
                dungeon = make_map(fov, DUNGEON_SIZE, [p], MAX_ENEMIES_PER_ROOM, sprites)
            player_took_turn = True if ends_turn else False
    return player_took_turn, dungeon

def update(clock, player_took_turn, fps_counter, fov, dungeon):
    global screen_offset
    if player_took_turn:
        fov.update(entities=dungeon.entities, level=dungeon.level)
        player_took_turn = False
    if NUM_X_TILES < dungeon.size[0] or NUM_Y_TILES < dungeon.size[1]:
        screen_offset = [GAME_PANEL_CENTER[0]-dungeon.entities[0].x*TILE_DIMENSION, GAME_PANEL_CENTER[1]-dungeon.entities[0].y*TILE_DIMENSION]
    else:
        screen_offset = game_panel.origin
    return clock.get_fps(), player_took_turn

def render(fov, dungeon, player, fps_counter, sprites):
    global screen_offset, message_render_offset
    screen.fill(colors.BLACK)
    for p in panels:
        p.render(ui_font)
    for i in range(len(messages)):
        if message_panel.origin[1]+message_render_offset+(i*TEXT_SPACING)+TEXT_SPACING > message_panel.origin[1]:
            screen.blit(ui_font.render(messages[i][0], 1, messages[i][1]), (message_panel.origin[0]+2, message_panel.origin[1]+message_render_offset+(i*TEXT_SPACING)+TEXT_SPACING))
    # Draw explored tiles
    y_min_range = player.y-NUM_Y_TILES//2 if player.y-NUM_Y_TILES//2 > 0 else 0
    y_max_range = player.y+NUM_Y_TILES//2 if player.y+NUM_Y_TILES//2 < dungeon.level_height else dungeon.level_height
    x_min_range = player.x-NUM_X_TILES//2 if player.x-NUM_X_TILES//2 > 0 else 0
    x_max_range = player.x+NUM_X_TILES//2 if player.x+NUM_X_TILES//2 < dungeon.level_width else dungeon.level_width
    for y in range(y_min_range, y_max_range):
        for x in range(x_min_range, x_max_range):
            if fov.explored_tiles[x][y] == 1:
                if dungeon.level[x][y] == 1:
                    screen.blit(sprites['explored_wall'], (TILE_DIMENSION*x+screen_offset[0], TILE_DIMENSION*y+screen_offset[1]))
                else:
                    screen.blit(sprites['explored_floor'], (TILE_DIMENSION*x+screen_offset[0], TILE_DIMENSION*y+screen_offset[1]))
    for v in fov.visible_tiles:
        # Only render tiles that are actually on screen
        if tile_in_bounds(v):
            if dungeon.level[v[0]][v[1]] == 1:
                screen.blit(sprites['visible_wall'], (TILE_DIMENSION*v[0]+screen_offset[0], TILE_DIMENSION*v[1]+screen_offset[1]))
            else:
                screen.blit(sprites['visible_floor'], (TILE_DIMENSION*v[0]+screen_offset[0], TILE_DIMENSION*v[1]+screen_offset[1]))
    for e in dungeon.entities:
        if e is not player and (e.x, e.y) in fov.visible_tiles:
            screen.blit(e.sprite, (TILE_DIMENSION*e.x+screen_offset[0], TILE_DIMENSION*e.y+screen_offset[1]))
    screen.blit(sprites['player_sprite'], (TILE_DIMENSION*player.x+screen_offset[0], TILE_DIMENSION*player.y+screen_offset[1]))
    render_fps(fps_counter)
    pyg.display.flip()

def tile_in_bounds(tile):
    ''' Check to see if tile will fit in the display area '''
    global screen_offset
    if TILE_DIMENSION*tile[0]+screen_offset[0]+TILE_DIMENSION < GAME_PANEL_SIZE[0] and TILE_DIMENSION*tile[1]+screen_offset[1] < GAME_PANEL_SIZE[1]:
        return True
    return False

def move(dungeon, player, sprites, x, y):
    dx = player.x + x
    dy = player.y + y
    can_move = True
    if (dungeon.level[dx][dy] != 1):
        for e in dungeon.entities:
            if (e.x, e.y) == (dx, dy) and e.blocks:
                player.combat_component.attack(e, message)
                if e.combat_component.hp <= 0:
                    message('{0} has died!'.format(e.name), colors.RED)
                    monsters.entity_death(e, sprites['dead_sprite'])
                can_move = False
                break
        if can_move:
            player.x = dx
            player.y = dy
    else:
        message('The wall feels solid', colors.GRAY)

def render_fps(fps_counter):
    pyg.draw.rect(screen, colors.BLACK, ((0, 0), (72, 24)))
    screen.blit(ui_font.render(str(('{:.2f}'.format(fps_counter))), 1, colors.GREEN), (0, 0))

def message(message, color):
    global message_render_offset
    # Number of characters that will fit in the panel
    wrap = calc_wrap(message_panel.size[0])
    start_indices = [0]
    if len(message) > wrap:
        # Going from 0 -> len(message), if i jumps by wrap it will give start indices of each message part
        # e.g. if wrap == 21, start_indices == [0, 21, 42]
        for i in range(wrap, len(message), wrap):
            start_indices.append(i)
        # The length of start_indices indicates how many times the 
        # message needs to be split
        for i in range(len(start_indices)):
            if i != (len(start_indices) - 1):
                messages.append((message[start_indices[i]:start_indices[i+1]], color))
            else:
                messages.append((message[start_indices[i]:], color))
    else:
        messages.append((message, color))
    # Scrolls the message panel show it only shows the most recent messages
    if len(messages) > MAX_MESSAGES:
        message_render_offset -= TEXT_SPACING * len(start_indices)
    print(message_render_offset, len(messages))

def calc_wrap(width):
    '''
    Produces the maximum number of characters a panel can display
    '''
    global FONT_SIZE
    # 1.68 is a ratio gotten from testing with 24pt font and 300px width
    # Through manual testing 21 characters would fit in the panel
    # 24/(300/21) = 1.68, (300/24)*1.68 = 21
    return math.floor((width/FONT_SIZE)*1.68)-1

main()
