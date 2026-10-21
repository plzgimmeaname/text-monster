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
        fix_map(map)
        
    print("Map finalized.")
    print()
    print()
    print()
    print("<------------- The Labyrinth of Zayan ---------------->")
    if debug:
        render(map)
    sane = map_sanity_check(map)
    return map, sane 


def stairs_column(floor:list[Room]):
    for index in range(len(floor)):
        if floor[index].type == "Stairs":
            return index

def get_path(map:list[list[Room]]):
    path = []
    x = 0 
    for i in range(len(map)):
        if i == len(map) - 1:
            target = len(map[i]) - 1 
        else:
            target = stairs_column(map[i])
        if target >= x:
            step = 1 
        else:
            step = -1 
        for col in range(x, target + step, step):
            if not (i == 0 and col == 0):
                path.append((i, col))
        x = target 
    return path 

def change_room(floor:list[Room], col:int, kind:str, contents = None):
    new_room = Room(floor[col].name, kind)
    if contents != None:
        new_room.contents = contents 
    floor[col] = new_room 

def place_item(map:list[list[Room]], path:list, index:int, item:str):
    for kind in ("Empty", "Object"):
        for j in range(index - 1, -1, -1):
            if map[path[j][0]][path[j][1]].type == kind:
                change_room(map[path[j][0]], path[j][1], "Object", item)
                return True 
    return False 

def path_pass(map:list[list[Room]], path:list, patch:bool):
    swords = 0 
    stones = 0 
    for index in range(len(path)):
        i = path[index][0]
        j = path[index][1]
        room = map[i][j]
        if room.type == "Object":
            if room.contents == "Sword" and swords + stones < 3 and (stones == 1 or swords + stones < 2):
                swords += 1 
            elif room.contents == "Magic Stone" and stones == 0:
                stones += 1 
        elif room.type == "Monster":
            if swords == 0:
                if patch and not place_item(map, path, index, "Sword"):
                    change_room(map[i], j, "Empty")
                return False 
            swords -= 1 
        elif room.type == "Boss":
            if swords > 0 and stones > 0:
                return True 
            if patch:
                if stones == 0:
                    place_item(map, path, index, "Magic Stone")
                else:
                    place_item(map, path, index, "Sword")
            return False 
    return False 

def fix_map(map:list[list[Room]]):
    path = get_path(map)
    for attempt in range(300):
        if path_pass(map, path, True):
            break 
    monsters = 0 
    swords = 0 
    off_path = []
    on_path = []
    for i in range(len(map)):
        for j in range(len(map[i])):
            room = map[i][j]
            if room.type == "Monster":
                monsters += 1 
            elif room.type == "Object" and room.contents == "Sword":
                swords += 1 
            elif room.type == "Empty" and (i, j) != (0, 0):
                if (i, j) in path:
                    on_path.append((i, j))
                else:
                    off_path.append((i, j))
    random.shuffle(off_path)
    random.shuffle(on_path)
    while monsters < 3 and len(off_path) > 0:
        spot = off_path.pop()
        change_room(map[spot[0]], spot[1], "Monster")
        monsters += 1 
    spots = off_path + on_path 
    while swords < 4 and len(spots) > 0:
        spot = spots.pop()
        change_room(map[spot[0]], spot[1], "Object", "Sword")
        swords += 1 

def valid(map:list[list[Room]]):
    monsters = 0 
    swords = 0 
    for floor in map:
        for room in floor:
            if room.type == "Monster":
                monsters += 1 
            elif room.type == "Object" and room.contents == "Sword":
                swords += 1 
    if monsters < 3 or swords < 4:
        return False 
    return path_pass(map, get_path(map), False)
