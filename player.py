#player class for defining movement, attack, inventory, etc.

class Player:

    def __init__(self):
        self.inventory = {}

    def move(self, direction):
        print(f'You moved in {direction}.\n')
        return direction

    def pickup(self, object):
        self.inventory.get(object, 0) += 1
        print(f'You now have {self.inventory[object]} {object}(s)')

    def attack(self, object):
        if object == 'sword':
            self.inventory[object] -= 1
        else:
            return False

    # add inventory display functions