#player class for defining movement, attack, inventory, etc.
import random
from item import Item

class Player:

    def __init__(self, name):
        self.name = name 
        self.hp = 20
        self.max = 20
        self.atk = 2
        self.dodge = 0.05
        self.speed = 2
        self.level = 1
        self.xp = 0
        self.weapon = None
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

    def weapon_bonus(self):
        if self.weapon is None:
            return 0
        bonus = 0
        for effect in self.weapon.get_stat_effects():
            if effect[0] == "attack":
                bonus += effect[1]
        return bonus

    def equip_weapon(self, item:Item):
        if item.equip != 1:
            return False
        current = self.weapon_bonus()
        new = 0
        for effect in item.get_stat_effects():
            if effect[0] == "attack":
                new += effect[1]
        if self.weapon is None or new > current:
            self.weapon = item
            print(f"You equip the {item.name} (+{new} attack).")
            return True
        print(f"The {item.name} is no better than your {self.weapon.name}, so you leave it behind.")
        return False

    def gain_xp(self, amount:int):
        self.xp += amount
        messages = []
        while self.xp >= self.level * 10:
            self.xp -= self.level * 10
            self.level += 1
            self.max += 3
            self.atk += 1
            self.hp = self.max
            messages.append(f"You reach level {self.level}! Your health is restored.")
        return messages

    def attack(self):
        rand_increase = random.randint(1,3)
        rand_increase += self.weapon_bonus()
        if self.does_have("Sword"):
            rand_increase += 3
        return self.atk + rand_increase

    def dodged(self):
        probabilty = random.randint(1, 100)
        return probabilty < self.dodge * 100

    def take_damage(self, damage:int):
        self.hp = max(self.hp - damage, 0)
        return f"You took {damage} points of damage."

    def heal(self, health:int):
        self.hp = min(self.hp + health, self.max)

    def is_alive(self):
        return self.hp > 0

    def check_status(self):
        print()
        weapon = self.weapon.name if self.weapon is not None else "None"
        print(f"{self.name} | LVL: {self.level} ({self.xp}/{self.level * 10} XP) | HP: {self.hp}/{self.max} | ATK: {self.atk} | DODGE: {self.dodge} | SPEED: {self.speed} | WEAPON: {weapon}")
        print()

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
            return "You move rightward"
        elif direction == 3:
            self.y += 1 
            return "You move downward"
        else:
            self.x -= 1 
            return "You move leftward"

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
            amount = effect[1]

            if stat == "hp":
                self.hp = min(self.hp + amount, self.max)
            elif stat == "max":
                self.max += amount 
            elif stat == "speed":
                self.speed += amount 
            elif stat == "dodge":
                self.dodge += amount 
            elif stat == "attack":
                self.atk += amount 

        return "You equip the item and gain its stats. Check your status for more info."

    def remove_status_effects(self, item:Item):
        effects = item.get_stat_effects()

        for effect in effects:
            stat = effect[0]
            amount = effect[1]

            if stat == "hp":
                self.hp = max(self.hp - amount, 1)
            elif stat == "max":
                self.max -= amount 
                self.hp = min(self.hp, self.max)
            elif stat == "speed":
                self.speed -= amount 
            elif stat == "dodge":
                self.dodge -= amount 
            elif stat == "attack":
                self.atk -= amount 

        return "You unequip the item and lose its stats. Check your status for more info."

    def check_status(self):
        status = f"{self.name} | HP: {self.hp}/{self.max} | ATK: {self.atk} | DODGE: {self.dodge} | SPEED: {self.speed}"
        return status 

    def equip(self, item:Item):
        slots = {1: "hand_equip", 2: "armor_equip", 3: "accessory_equip"}
        slot = slots.get(item.equip)
        if slot is None:
            return "You cannot equip that."
        if self.inventory.get(item.name, 0) < 1:
            return f"You do not have a {item.name}."
        current = getattr(self, slot)
        if current is not None:
            self.inventory[current.name] = self.inventory.get(current.name, 0) + 1 
            self.remove_status_effects(current)
        setattr(self, slot, item)
        self.apply_status_effects(item)
        self.inventory[item.name] -= 1 
        return f"You equip the {item.name}."
