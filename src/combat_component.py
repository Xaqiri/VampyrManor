import pygame as pyg

class CombatComponent():
    def __init__(self):
        self.max_hp = 10
        self.current_hp = 10
        self.damage = 1
        self.parent = 0
