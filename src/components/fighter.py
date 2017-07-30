import pyRL.colors as colors

class Fighter():
    def __init__(self, max_hp, max_mp, strength=0, defense=0):
        self.hp = max_hp
        self.mp = max_mp
        self.max_hp = max_hp
        self.max_mp = max_mp
        self.strength = strength
        self.defense = defense

    def attack(self, target, message):
        damage = self.strength - target.combat_component.defense
        target.combat_component.hp -= damage
        message('{0} hits {1} for {2} damage!'.format(self.parent.name, target.name, damage), colors.Colors.WHITE)
        if self.parent.name == 'player':
            self.parent.xp += damage
            message('You have gained {0} xp'.format(damage), colors.Colors.GREEN)
