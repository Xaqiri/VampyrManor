class Fighter():
    def __init__(self, max_hp, max_mp, strength=0, defense=0):
        self.hp = max_hp
        self.mp = max_mp
        self.max_hp = max_hp
        self.max_mp = max_mp
        self.strength = strength
        self.defense = defense

    def attack(self, target):
        damage = self.strength - target.combat_component.defense
        target.combat_component.hp -= damage
        print('{0} hits {1} for {2} damage!'.format(self.parent.name, target.name, damage))
        if self.parent.name == 'player':
            self.parent.xp += damage
            print('You have gained {0} xp'.format(damage))
            print('You now have {0} xp'.format(self.parent.xp))
