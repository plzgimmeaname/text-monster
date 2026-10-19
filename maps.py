import random
from tqdm import tqdm
import time 
from room import Room
import os 
# import names 

# names.get_full_name()





PRESET_PROB_LOW = {"Empty" : 30, "Object" : 40, "Monster" : 30}

PRESET_PROB_MED = {"Empty" : 30, "Object" : 30, "Monster" : 40}

PRESET_PROB_HARD = {"Empty" : 25, "Object" : 25, "Monster" : 50}

def move_valid(current: tuple, movement: tuple, sword: bool, map:list[list[Room]], magic_stone:bool):
    if movement[1] != 0:
        return False 
    if map[current[1] + movement[1]][current[0] + movement[0]].type == "Monster":
        return sword 
    elif map[current[1] + movement[1]][current[0] + movement[0]].type == "Empty" or map[current[1] + movement[1]][current[0] + movement[0]].type == "Stairs" or map[current[1] + movement[1]][current[0] + movement[0]].type == "Object":
        return True 
    else:
        if sword == True and magic_stone == True:
            return True 
        else:
            return False 


    

def mapping_algorithm(map:list[list[Room]]) -> bool:
    monster_count = 0 
    player_x = 0 
    player_y = 0 
    sword_count = 0 
    magic_stone = 0 
    floor = 0 
    playing = True 
    while playing:
        right = 0 
    

#Easter egg: colby wuz here 
#The above easter egg was under the request of Colby Goldberg. The following individual had no part of writing the code, but simply wanted an easter egg. 


def room_selection(values: dict):
    chance = 0 
    prob = random.randint(1, 100)
    for val in values:
        chance += values[val]
        if prob <= chance:
            return val 
    return val

def random_room_name():
    p_room_names_1 = ["The Cellar of", "The Library of", "The Kitchen of", "The Ballroom of", "The Office of", "The Chapel of", "The Garden of", "The Tower of", "The Pool of", "The Dining Room of", "The Armory of", "The Vault of"]
    p_room_names_2 = ["Sin", "Doom", "Despair", "Wrath", "Envy", "Sloth", "Shadows", "Greed"]

    return random.choice(p_room_names_1) + " " + random.choice(p_room_names_2)

# for i in range(30):
#     print(room_selection(vals1))
def map_sanity_check(map:list): 
    errors = []
    flr = 0
    if map[0][0].type != "Empty": errors.append("First room is not clear")
    if map[-1][-1].type != "Boss": errors.append("Boss not put in right position")
    for floor in map:
        flr += 1 
        stairspl = 0 
        for room in floor:
            if room.type == "Stairs":
                stairspl += 1 
        if stairspl == 1:
            pass
        else:
            errors.append("Incorrect # of stairs!!! FLR: " + str(flr))
    if len(errors) > 0:
        print()
        print("#### ERRORS ####")
        for error in errors:
            print("     - " + error)
        print("################")
        print()
        return 0 
    else:
        return 1 

def render(map:dict):
    print()
    for floor in map:
        for room in floor:
            print("[" + room.type + "] ", end="")
        print()
    print()


def map_generation(room_probability:dict, floors, rooms, debug = False, sequel = False):
    map = [] 
    print("Generating floors...")
    for i in tqdm(range(floors)):
        floor = [] 
        print("Generating rooms for floor " + str(i) + "...")
        for j in tqdm(range(rooms)):
            room_type = room_selection(room_probability)
            floor.append(Room(random_room_name(), room_type, floor=i, sequel=sequel))
        map.append(floor)
    print("Generating stairs...")
    for i in tqdm(range(floors)):
        if i == 0:
            map[i].insert(random.randint(1, rooms), Room(random_room_name(), "Stairs"))
        else:
            map[i].insert(random.randint(0, rooms), Room(random_room_name(), "Stairs"))
    map[0][0] = Room("The Antechamber of the Labyrinth", "Empty")
    if sequel:
        for i in range(floors):
            if i == floors - 1:
                map[i].append(Room("The Throne of Zayan", "Boss", floor=i, sequel=True, final=True))
            else:
                map[i].append(Room("The Guardian Hall of Floor " + str(i + 1), "Boss", floor=i, sequel=True))
    if not sequel:
        for index in range(len(map[-1])):
            if map[-1][index].type != "Stairs":
                boss = Room("The Treasure Hall of Zayan", "Boss")
                map[-1][index] = boss
                break
        map[-1].remove(boss)
        map[-1].insert(len(map[-1]), boss)
        
    print("Map finalized.")
    print()
    print()
    print()
    print("<------------- The Labyrinth of Zayan ---------------->")
    if debug:
        render(map)
    sane = map_sanity_check(map)
    return map, sane 


def valid(map:list[list[Room]]):
    stairs = None 
    starting = (0,0)
    sword = 0 
    magic = 0 
    for index, floor in enumerate(map):
        if index == len(map) - 1:
            break 
        for jindex, room in enumerate(floor):
            if room.type == "Stairs":
                stairs = (jindex, index)
        difference = stairs[0] - starting[0]
        if difference > 0: #right
            for i in range(difference):
                if floor[starting[0] + (i + 1)].type == "Object":
                    if floor[i + 1].contents == "Sword":
                        sword += 1 
                    else:
                        magic += 1 
                elif floor[starting[0] + (i + 1)].type == "Monster":
                    if sword > 0:
                        sword -= 1 
                        continue 
                    else:
                        return False 
                elif floor[starting[0] + (i + 1)].type == "Empty": continue 
        else: 
            difference = abs(difference)
            for i in range(1, difference):
                if floor[starting[0] - 1].type == "Object":
                    if floor[starting[0] - 1].contents == "Sword":
                        sword +=1 
                    else:
                        magic += 1 
                elif floor[starting[0] - 1].type == "Monster":
                    if sword > 0:
                        sword -= 1 
                    else:
                        return False 
                elif floor[starting[0] - 1].type == "Empty": pass 

        starting = (stairs[0], stairs[1] + 1)

    boss = (len(map) - 1 , len(map[-1]) - 1 )

    room_diff = boss[0] - starting[0]

    for i in range(1, room_diff): 
        if map[-1][starting[0] + i].type == "Object":
            if map[-1][starting[0] + i].contents == "Sword":
                sword += 1 
            else:
                magic += 1 
        elif map[-1][starting[0] + i].type == "Monster":
            if sword > 0:
                sword -= 1 
            else:
                return False 
        elif map[-1][starting[0] + i].type == "Empty" or map[-1][starting[0] + i].type == "Stairs":
            pass 
        elif map[-1][starting[0] + i].type == "Boss":
            if sword > 0 and magic > 0:
                return True 
            else:
                return False 

    #print("Sword: ", sword)
    #print("Magic Stones: ", magic)
    if sword > 0 and magic > 0:
        return True 
    else:
        return False 


