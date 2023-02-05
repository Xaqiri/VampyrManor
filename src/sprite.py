import os
import pygame as pyg

sprite_path = os.path.join('..', 'assets', 'sprites')


def load_sprites(colors, size):
    ''' Load sprites
        @colors = list of colors
        @size = size in pixels of the sprite's sides
    '''
    sprite_list = dict(
            wall = load_sprite('wall2.png', colors.TRANS, size),
            wall2 = load_sprite('wall2.png', colors.TRANS, size),
            floor = load_sprite('wall2.png', colors.TRANS, size),
            dead = load_sprite('dead.png', colors.TRANS, size),
            player = load_sprite('player.png', colors.TRANS, size),
            b = load_sprite('b.png', colors.TRANS, size),
            r = load_sprite('r.png', colors.TRANS, size)
    )
    tile_colors = dict(
        unexplored_tile = color_sprite(sprite_list['wall2'], colors.BLACK, colors.DRK_RED, colors.TRANS),
        explored_wall = color_sprite(sprite_list['wall2'], colors.BLACK, colors.DRK_RED, colors.TRANS),
        explored_floor = color_sprite(sprite_list['floor'], colors.BLACK, colors.DRKR_RED, colors.TRANS),
        visible_wall = color_sprite(sprite_list['wall'], colors.BLACK, colors.GRAY, colors.TRANS),
        visible_floor = color_sprite(sprite_list['floor'], colors.BLACK, colors.DRK_GRAY, colors.TRANS),
        player_sprite = color_sprite(sprite_list['player'], colors.BLACK, colors.BLU_GRY, colors.TRANS),
        bat_sprite = color_sprite(sprite_list['b'], colors.BLACK, colors.GRAY, colors.TRANS),
        rat_sprite = color_sprite(sprite_list['r'], colors.BLACK, colors.BROWN, colors.TRANS),
        dead_sprite = color_sprite(sprite_list['dead'], colors.BLACK, colors.RED, colors.TRANS)
    )
    return tile_colors

def load_sprite(name, color, size):
    sprite = pyg.image.load(os.path.join(sprite_path, name)).convert()
    sprite.set_colorkey(color)
    sprite = pyg.transform.scale(sprite, (size, size))
    return sprite

def color_sprite(sprite, old_color, new_color, no_color):
    new_sprite = sprite.copy()
    new_sprite = pyg.PixelArray(new_sprite)
    new_sprite.replace(old_color, new_color)
    new_sprite =  pyg.PixelArray.make_surface(new_sprite)
    new_sprite.set_colorkey(no_color)
    return new_sprite