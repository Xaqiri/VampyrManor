import random
import entity
import components.fighter

def generate_rat(x, y, sprite, dungeon):
    combat_component = components.fighter.Fighter(1, 1)
    rat = entity.Entity(x, y, sprite, combat_component)
    return rat
