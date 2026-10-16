#player class for defining movement, attack, inventory, etc.

class Player:

    def __init__(self):
        self.inventory = {}
        self.x = 0 
        self.y = 0 

    def move(self, direction):
        print(f'You move {direction}.\n')
        if direction == "rightward":
            self.x += 1 
        elif direction == "leftward":
            if self.x == 0:
                pass
            else:
                self.x -= 1 
        elif direction == "downward":
            self.y +=  1
        elif direction == "upward": 
            if self.y == 0:
                pass
            else:
                self.y -= 1 
        
    def pickup(self, object):
        try:
            self.inventory[object] += 1
        except KeyError:
            self.inventory[object] = 1
        print(f'You now have {self.inventory[object]} {object}(s)')

    def does_have(self, object:str):
        if self.inventory.get(object, 0) >= 1:
            return True 
        else:
            return False 

    def display_inventory(self):
        print()
        print("|--- Inventory Menu ---|")
        for key in self.inventory.keys():
            print(str(key) + " x" + str(self.inventory[key]))
        print("|----------------------|")
        print()

    def discard(self, object):
        if object == 'Sword':
            self.inventory[object] -= 1
        else:
            return False