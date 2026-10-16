import random 

class Room:
    def __init__(self, name, type, object=None):
        self.name = name
        self.explored = False 
        self.type = type 
        self.contents = self.random_contents() 
        if self.type == "Monster":
            self.monster = self.random_monster_name()
        elif self.type == "Object": 
            self.obj = self.random_obj()
            self.location = self.random_location()
        elif self.type == "Boss":
            self.boss_name = self.random_boss_name()

    def random_contents(self):
        items = ["Sword", "Sword", "Sword", "Sword", "Magic Stone", "Sword", "Sword"]
        return random.choice(items)

    def random_monster_name(self):
        p_names = ["Orge", "Troll", "Evil Fairy", "Young Dragon", "Giant Spider"]
        return random.choice(p_names)

    def random_location(self):
        p_locations = ["in the corner of the room", "in the center of the room", "just behind the door", "set upon an old stone bench"]
        return random.choice(p_locations) 

    def random_obj(self):
        p_obj = ["a crate", "a desk", "a chest", "a coffer"]
        return random.choice(p_obj)

    def random_boss_name(self):
        p_boss = ["Smolder", "Azopolxferz", "Crimson"]
        return random.choice(p_boss)

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
            print("Watch out! A " + str(self.random_monster_name()) +" is in the room!")
        elif self.type == "Object": 
            print("You find " + str(self.random_obj()) + " " + str(self.random_location()) + ". Inside of it is a " + str(self.contents))
        elif self.type == "Stairs":
            print("The room is bare except for a set of stairs winding upwards and downwards.")
        elif self.type == "Boss":
            print("You push open the doors, and reveal the guardian of Zayan's treasures, " + self.random_boss_name() + " The Dragon!")
        
        return self.type 
        
