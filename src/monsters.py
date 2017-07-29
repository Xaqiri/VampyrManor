import random
import entity
import components.fighter

def generate_rat(sprite, dungeon):
    x = random.randrange(0, dungeon.level_width)
    y = random.randrange(0, dungeon.level_height)
    while dungeon.level[x][y] == 1:
        x = random.randrange(0, dungeon.level_width)
        y = random.randrange(0, dungeon.level_height)
    combat_component = components.fighter.Fighter(1, 1)
    rat = entity.Entity(x, y, sprite, combat_component)
    return rat
