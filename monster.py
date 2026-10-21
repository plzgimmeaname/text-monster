# Names: Sreekar Karra, Zayan Sikder, John Steele
# Period: 2
# Date Last Edited: 10/20/26

#Configure imports 
import random 

# Create basic monster class for name, hp, damage (amount dealt to player), dodge (change to avoid damage), and speed (change to catch player when they flee)
class Monster:
    def __init__(self, name:str, hp:int, attack:int, dodge_chance:float, speed:int):
        self.name = name 
        self.hp = hp 
        self.max = hp 
        self.atk = attack 
        self.dodge_chance = dodge_chance
        self.alive = True 
        self.speed = speed 

    #Checks to see if player can flee, the faster monster is the less likely they can S
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

    #Check to see if the monster dodges the player's attack 
    def dodged(self):
        dodge_chance = self.dodge_chance * 100 
        probabilty = random.randint(1, 100)
        if probabilty < dodge_chance:
            return True
        else:
            return False 

    #Return damage to player with small amount added for variability 
    def attack(self):
        rand_increase = random.randint(1,3)
        return self.atk + rand_increase

    #Take damage 
    def take_damage(self, damage:int):
        self.hp = self.hp - damage 
        return f"The monster took {damage} points of damage."

    #I don't think we use it, but if we were to expand game this would allow monster to heal without going over max hp
    def heal(self, health:int):
        self.hp = min(self.hp + health, self.max)
        return f"The monster healed for {health} points of health."

    #Checks if monster should die 
    def is_alive(self):
        if self.hp <= 0:
            self.alive = False 
        return self.alive
