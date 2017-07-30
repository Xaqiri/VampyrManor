import random
import entity
import components.fighter

def generate_player(x, y, sprite):
    combat_component = components.fighter.Fighter(max_hp=10, max_mp=10, strength=1, defense=1)
    player = entity.Entity(x, y, 'player', sprite, combat_component)
    return player

def generate_bat(x, y, sprite):
    combat_component = components.fighter.Fighter(max_hp=3, max_mp=1, strength=2, defense=0)
    bat = entity.Entity(x, y, 'bat', sprite, combat_component)
    return bat

def generate_rat(x, y, sprite):
    combat_component = components.fighter.Fighter(max_hp=1, max_mp=1, strength=1, defense=0)
    rat = entity.Entity(x, y, 'rat', sprite, combat_component)
    return rat

def entity_death(entity, sprite):
    entity.combat_component = None
    entity.name = 'dead ' + entity.name
    entity.sprite = sprite
    entity.blocks = False
