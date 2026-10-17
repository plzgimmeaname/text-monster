#player class for defining movement, attack, inventory, etc.
from item import Item

class Player:

    def __init__(self, name):
        self.name = name 
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
        if self.does_have(object):
            self.inventory[object] -= 1
            return True
        return False


class Main_Character:
    def __init__(self, name):
        self.name = name 
        self.hp = 10 
        self.max = 10 
        self.atk = 1 
        self.dodge = 0.01
        self.speed = 1 
        self.x = 0 
        self.y = 0 
        self.inventory = {}
        self.hand_equip = None
        self.armor_equip = None 
        self.accessory_equip = None 

    def move(self, direction:int):
        if direction == 1: 
            self.y -= 1 
            return "You move upward"
        elif direction == 2:
            self.x += 1
            return "You move leftward"
        elif direction == 3:
            self.y -= 1 
            return "You move downward"
        else:
            self.x -= 1 
            return "You move rightward"

    def pickup(self, item:Item):
        if item.name in self.inventory.keys():
            self.inventory[item.name] += 1 
        else:
            self.inventory[item.name] = 1 

        return f"You pick up a {item.name}"

    def apply_status_effects(self, item:Item):
        effects = item.get_stat_effects()

        for effect in effects:
            stat = effect[0]
            amount = effect[0]

            if stat == "hp":
                self.hp + amount 
            elif stat == "max":
                self.max + amount 
            elif stat == "speed":
                self.speed + amount 
            elif stat == "dodge":
                self.dodge + amount 
            elif stat == "attack":
                self.atk + amount 

        return "You equip the item and gain its stats. Check your status for more info."

    def remove_status_effects(self, item:Item):
        effects = item.get_stat_effects()

        for effect in effects:
            stat = effect[0]
            amount = effect[0]

            if stat == "hp":
                self.hp - amount 
            elif stat == "max":
                self.max - amount 
            elif stat == "speed":
                self.speed - amount 
            elif stat == "dodge":
                self.dodge - amount 
            elif stat == "attack":
                self.atk - amount 

        return "You unequip the item and lose its stats. Check your status for more info."

    def check_status(self):
        status = f"{self.name} | HP: {self.hp}/{self.max} | ATK: {self.atk} | DODGE: {self.dodge} | SPEED: {self.speed}"

    def equip(self, item:Item):
        equip_type = item.equip
        if equip_type == 1:
            if self.hand_equip == None:
                self.hand_equip = item 
                self.apply_status_effects(self.hand_equip)
                self.inventory[item] -= 1 
            else:
                self.inventory[self.hand_equip.name] += 1 
                self.remove_status_effects(self.hand_equip)
                self.hand_equip = None 
        elif equip_type == 2: 
            if self.armor_equip == None:
                self.armor_equip = item 
                self.apply_status_effects(self.armor_equip)
                self.inventory[item] -= 1 
            else:
                self.inventory[self.armor_equip.name] += 1 
                self.remove_status_effects(self.armor_equip)
                self.armor_equip = None 
        elif equip_type == 3:
            if self.accessory_equip == None:
                self.armor_equip = item 
                self.apply_status_effects(self.accessory_equip)
                self.inventory[item] -= 1 
            else:
                self.inventory[self.accessory_equip.name] += 1 
                self.remove_status_effects(self.accessory_equip)
                self.accessory_equip = None 
                

