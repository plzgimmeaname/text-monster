import random
from tqdm import tqdm
# import names 

# names.get_full_name()



#all_maps = [vals, vals2, vals3, vals4, vals5]

low_dif = {'Empty' : 30, 'Sword' : 40, 'Monster' : 15, 'Boss' : 5, 'Heal' : 10}

# add med_dif and high_dif lists



def room_selection(values: dict):
    chance = 0 
    for val in values:
        chance += values[val]
        prob = random.randint(0, 100)
        if prob <= chance:
            return val 
        else: 
            continue 

# for i in range(30):
#     print(room_selection(vals1))
def mapgen (roomtypes: dict, stories, minrooms, maxrooms):
    map = []
    for i in tqdm(range((stories))):
        numofrooms = random.randint(minrooms, maxrooms)
        floor = []
        for i in range(numofrooms):
            val = room_selection(roomtypes)
            floor.append(val)
        map.append(floor)
    map[0][0] = 'empty'
    for i in range(stories):
        map[i].insert(random.randint(0, (stories - 1)), 'stairs')
    return map
