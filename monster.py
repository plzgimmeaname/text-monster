import random 

class Monster:
    def __init__(self, name:str, hp:int, attack:int, dodge_chance:float, speed:int):
        self.name = name 
        self.hp = hp 
        self.max = hp 
        self.atk = attack 
        self.dodge_chance = dodge_chance
        self.alive = True 
        self.speed = speed 

    def can_flee(self, player_speed:int) -> bool: 
        difference = self.speed - player_speed
        if difference < 1:
            return True 
        else:
            flee = random.randint(0, difference)
            if flee == 0:
                return True
            else:
                return False 

    def dodged(self):
        dodge_chance = self.dodge_chance * 100 
        probabilty = random.randint(1, 100)
        if probabilty < dodge_chance:
            return True
        else:
            return False 

    def attack(self):
        rand_increase = random.randint(1,3)
        return self.atk + rand_increase

    def take_damage(self, damage:int):
        self.hp = self.hp - damage 
        return f"The monster took {damage} points of damage."

    def heal(self, health:int):
        gain = self.hp + health
        if (self.hp + gain) > self.max:
            self.hp = self.max
        else:
            self.hp += gain 
        return f"The monster healed for {health} points of health."

    def alive(self):
        if self.hp <= 0:
            self.alive = False 
        return self.alive
 