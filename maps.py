import random
from tqdm import tqdm
from room import Room
# import names 

# names.get_full_name()





PRESET_PROB_LOW = {"Empty" : 30, "Object" : 40, "Monster" : 30}

PRESET_PROB_MED = {"Empty" : 30, "Object" : 30, "Monster" : 40}

PRESET_PROB_HARD = {"Empty" : 25, "Object" : 25, "Monster" : 50}

    



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