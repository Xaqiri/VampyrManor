import pygame as pyg

class Entity():
    def __init__(self, x, y, sprite=0):
        self.x = x
        self.y = y
        self.sprite = sprite
