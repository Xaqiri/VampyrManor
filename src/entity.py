import pygame as pyg

class Entity():
    def __init__(self, x, y, name, sprite=0, combat_component=None, ai_component=None):
        self.x = x
        self.y = y
        self.sprite = sprite
        self.blocks = True
        self.name = name
        self.xp = 0
        self.combat_component = combat_component
        if self.combat_component:
            self.combat_component.parent = self
        self.ai_component = ai_component
        if self.ai_component:
            self.ai_component.parent = self
