import random 

class Room:
    def __init__(self, name, type, object=None):
        self.name = name
        self.explored = False 
        self.type = type 
        self.contents = object 

    def random_monster_name(self):
        p_names = ["Ogre", "Troll", "Evil Fairy", "Young Dragon", "Giant Spider"]
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

    def enter(self):
        if self.explored == True:
            print("You enter an already explored room...")
            return 0 
        print("You enter " + self.name + "...")
        if self.type == 0: 
            print("The room is empty; you are safe, for now...")
        elif self.type == 1: 
            print("Watch out! A " + str(self.random_monster_name()) +" is in the room!")
        elif self.type == 2: 
            print("You enter the room and find a " + str(self.random_obj()) + " " + str(self.random_location()) + ". Inside of it is " + str(self.contents))
        elif self.type == 3:
            print("The room is bare except for a set of stairs winding upwards and downwards.")
        elif self.type == 4:
            print("You push open the doors, and reveal the guardian of Zayan's treasures, " + self.random_boss_name() + "!")

        return self.type 
        
