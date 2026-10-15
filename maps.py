import random
# import names 

# names.get_full_name()



#all_maps = [vals, vals2, vals3, vals4, vals5]

vals1 = {"Bossroom": 10, "Prize": 40, "Monster": 30, "Sword": 20}

vals2 = {"Hacking Terminal": 10, "Blade Runner": 90} 

# vals3 = {""}

# vals4 = {}

# vals5 = {}



def room_selection(values: dict):
    chance = 0 
    for val in values:
        chance += values[val]
        prob = random.randint(0, 100)
        if prob <= chance:
            return val 
        else: 
            continue 

for i in range(30):
    print(room_selection(vals1))
    