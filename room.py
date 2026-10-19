import random
from monster import Monster
from item import WEAPONS

class Room:
    def __init__(self, name, type, object=None, floor:int = 0, sequel:bool = False, final:bool = False):
        self.name = name
        self.explored = False 
        self.type = type 
        self.floor = floor 
        self.sequel = sequel 
        self.final = final 
        self.contents = self.random_contents() 
        if self.type == "Monster":
            self.monster = self.random_monster()
        elif self.type == "Object": 
            self.obj = self.random_obj()
            self.location = self.random_location()
        elif self.type == "Boss":
            self.boss_name = self.random_boss_name()
            if self.sequel:
                self.monster = self.sequel_boss()
            else:
                self.monster = Monster(self.boss_name, 20, 2, 0.05, 2)

    def random_contents(self):
        if self.sequel:
            names = list(WEAPONS.keys())
            top = min(self.floor + 2, len(names))
            items = names[:top] + ["Magic Stone", "Health Potion", "Health Potion", "Health Potion"]
            return random.choice(items)
        items = ["Sword", "Sword", "Sword", "Health Potion", "Magic Stone", "Health Potion", "Sword"]
        return random.choice(items)

    def random_monster_name(self):
        p_names = ["Orge", "Troll", "Evil Fairy", "Young Dragon", "Giant Spider"]
        return random.choice(p_names)

    def random_monster(self):
        stats = {
            "Orge": (8, 2, 0.05, 1),
            "Troll": (10, 3, 0.05, 1),
            "Evil Fairy": (5, 2, 0.3, 3),
            "Young Dragon": (12, 3, 0.1, 2),
            "Giant Spider": (6, 2, 0.15, 3),
        }
        name = self.random_monster_name()
        hp, attack, dodge_chance, speed = stats[name]
        if self.sequel:
            scale = 1 + 0.25 * self.floor
            hp = int(hp * scale)
            attack = int(attack * scale)
            dodge_chance = min(dodge_chance + 0.02 * self.floor, 0.5)
            speed = speed + self.floor // 2
        return Monster(name, hp, attack, dodge_chance, speed)

    def random_location(self):
        p_locations = ["in the corner of the room", "in the center of the room", "just behind the door", "set upon an old stone bench"]
        return random.choice(p_locations) 

    def random_obj(self):
        p_obj = ["a crate", "a desk", "a chest", "a coffer"]
        return random.choice(p_obj)

    def random_boss_name(self):
        if self.sequel:
            p_sequel_boss = ["Smolder", "Azopolxferz", "Crimson", "The Hollow King", "Zayan, Master of the Labyrinth"]
            if self.final:
                return p_sequel_boss[-1]
            return p_sequel_boss[min(self.floor, len(p_sequel_boss) - 2)]
        p_boss = ["Smolder", "Azopolxferz", "Crimson"]
        return random.choice(p_boss)

    def sequel_boss(self):
        scale = self.floor
        return Monster(self.boss_name, 20 + 12 * scale, 2 + scale, 0.05 + 0.02 * scale, 2 + scale // 2)

    def explore(self):
        self.explored = True

    def get_item(self):
        if self.type == "Object": 
            return self.contents
        else:
            return 0 

    def enter(self):
        if self.explored == True:
            print("You are now in an already explored/defeated/pillaged room...")
            return "Empty" 
        print("You enter " + self.name + "...")
        if self.type == "Empty": 
            print("The room is empty; you are safe, for now...")
        elif self.type == "Monster": 
            print("Watch out! A " + str(self.monster.name) +" is in the room!")
        elif self.type == "Object": 
            print("You find " + str(self.obj) + " " + str(self.location) + ". Inside of it is a " + str(self.contents))
        elif self.type == "Stairs":
            print("The room is bare except for a set of stairs winding upwards and downwards.")
        elif self.type == "Boss" and self.sequel:
            if self.final:
                print("The throne room doors groan open. Zayan himself rises to face you!")
            else:
                print("The guardian of this floor, " + self.boss_name + ", blocks the way down!")
        elif self.type == "Boss":
            print("You push open the doors, and reveal the guardian of Zayan's treasures, " + self.boss_name + " The Dragon!")
        
        return self.type 
        
