# Names: Sreekar Karra, Zayan Sikder, John Steele
# Period: 2
# Date Last Edited: 10/20/26

#Item class made 
class Item:
    #Constructor, defines item name, affected stats, and what equip slot it is 
    def __init__(self, name, stats:list[tuple], equip_type: int):
        self.name = name
        self.stat_effects = stats 
        self.equip = equip_type

    # Simple getter function 
    def get_stat_effects(self):
        return self.stat_effects


#Simple dictionary used for weapon power/attack values 
WEAPONS = {
    "Rusty Dagger": 1,
    "Iron Sword": 3,
    "Steel Blade": 5,
    "Flame Axe": 7,
    "Zayan's Bane": 10,
}

# We had planned for their to be items other than weapons that increase other attributes like max health
# dodge chance, speed, etc but did not have time to implement them. 