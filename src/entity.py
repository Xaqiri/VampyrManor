import pygame as pyg

class Entity():
    def __init__(self, x, y, sprite=0):
        self.x = x
        self.y = y
        self.sprite = sprite
        self.combat_component = 0
        if self.combat_component:
            self.combat_component.parent = self
