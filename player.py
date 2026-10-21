# Names: Sreekar Karra, Zayan Sikder, John Steele
# Period: 2
# Date Last Edited: 10/20/26

#Configure imports 
import random
from item import Item

# Class for the player 
class Player:
    #Constructor: Sets name and the base stats / fresh start 
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

    # Change x, y coordinates with player notifiction. 
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
    
    # Adds item to inventory, max limit checked in main loop 
    def pickup(self, object):
        try:
            self.inventory[object] += 1
        except KeyError:
            self.inventory[object] = 1
        print(f'You now have {self.inventory[object]} {object}(s)')

    # Applies the weapon's bonus to attack power of player
    def weapon_bonus(self):
        if self.weapon is None:
            return 0
        bonus = 0
        for effect in self.weapon.get_stat_effects():
            if effect[0] == "attack":
                bonus += effect[1]
        return bonus

    #Checks if one weapon is better than other, equips/keeps the best one 
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

    #Gain expierence plus level up check to see if you level up and gain power 
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

    #A gives attack damage plus random increase, in stage 1 the basic sword item allows for instant kills 
    def attack(self):
        rand_increase = random.randint(1,3)
        rand_increase += self.weapon_bonus()
        if self.does_have("Sword"):
            rand_increase += 3
        return self.atk + rand_increase

    # Checks if player dodge sthe attack 
    def dodged(self):
        probabilty = random.randint(1, 100)
        return probabilty < self.dodge * 100

    #Player takes damage function
    def take_damage(self, damage:int):
        self.hp = max(self.hp - damage, 0)
        return f"You took {damage} points of damage."

    #When player heals with stone or potion, make sure they cannot heal past max 
    def heal(self, health:int):
        self.hp = min(self.hp + health, self.max)

    #Checks if player died 
    def is_alive(self):
        return self.hp > 0

    #Shows user the check stats of the character 
    def check_status(self):
        print()
        weapon = self.weapon.name if self.weapon is not None else "None"
        print(f"{self.name} | LVL: {self.level} ({self.xp}/{self.level * 10} XP) | HP: {self.hp}/{self.max} | ATK: {self.atk} | DODGE: {self.dodge} | SPEED: {self.speed} | WEAPON: {weapon}")
        print()

    #Checks if player has certain object in inventory 
    def does_have(self, object:str):
        if self.inventory.get(object, 0) >= 1:
            return True 
        else:
            return False 

    #Renders inventory for user 
    def display_inventory(self):
        print()
        print("|--- Inventory Menu ---|")
        for key in self.inventory.keys():
            print(str(key) + " x" + str(self.inventory[key]))
        print("|----------------------|")
        print()

    #Gets rid of an item
    def discard(self, object):
        if self.does_have(object):
            self.inventory[object] -= 1
            return True
        return False

