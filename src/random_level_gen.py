import random

import colors
import rect

class RandomLevelGen():
    def __init__(self, room_min_size=1, room_max_size=5, max_rooms=20, level_width=0, level_height=0, level_font=None, tile_size=16, sprites=None):
        ''' Generates a random level
            Takes parameters:
                room_min_size
                room_max_size
                max_rooms
                level_width
                level_height '''
        self.room_min_size = room_min_size
        self.room_max_size = room_max_size
        self.max_rooms = max_rooms
        self.level_width = level_width
        self.level_height = level_height
        self.explored_wall = colors.Colors.BLUE#colors.Colors.DRK_BLUE
        self.visible_wall = colors.Colors.GRAY
        self.explored_floor = colors.Colors.BLU_GRY
        self.visible_floor = colors.Colors.WHITE
        self.level_font = level_font
        self.tile_size = tile_size
        self.sprites = sprites
        self.level = [[1]*level_height for x in range(level_width)]
        self.rooms = []

    def create_room(self, room):
        for x in range(room.x1, room.x2):
            for y in range(room.y1, room.y2):
                self.level[x][y] = 0

    def create_h_tunnel(self, x1, x2, y):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.level[x][y] = 0

    def create_v_tunnel(self, y1, y2, x):
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.level[x][y] = 0

    def make_level(self, entities=None, items=None):
        #self.rooms = []
        num_rooms = 0
        for r in range(self.max_rooms):
            w = random.randint(self.room_min_size, self.room_max_size)
            h = random.randint(self.room_min_size, self.room_max_size)
            x = random.randint(1, self.level_width - w - 1)
            y = random.randint(1, self.level_height - h - 1)
            new_room = rect.Rect(x, y, w, h)
            failed = False
            for other_room in self.rooms:
                if new_room.intersect(other_room):
                    failed = True
                    break
            if not failed:
                self.create_room(new_room)
                (new_x, new_y) = new_room.center()
                if num_rooms == 0:
                    try:
                        entities[0].x = new_x
                        entities[0].y = new_y
                    except:
                        print('No entities')
                        pass
                    try:
                        items[0].x = new_x + 1
                        items[0].y = new_y + 1
                    except:
                        print('No items')
                        pass
                else:
                    (prev_x, prev_y) = self.rooms[num_rooms-1].center()
                    if random.randint(0, 2) == 1:
                        self.create_h_tunnel(prev_x, new_x, prev_y)
                        self.create_v_tunnel(prev_y, new_y, new_x)
                    else:
                        self.create_v_tunnel(prev_y, new_y, prev_x)
                        self.create_h_tunnel(prev_x, new_x, new_y)
                self.rooms.append(new_room)
                num_rooms += 1
        #stairs = Tile(pos=(new_x, new_y), ascii_tile='>', font=self.level_font, tile_size=self.tile_size, walkable=True, visible_color=pyRL.colors.Colors.WHITE, explored_color=pyRL.colors.Colors.WHITE, sprites=None)
        return [entities[0].x, entities[0].y]
