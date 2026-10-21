# Names: Sreekar Karra, Zayan Sikder, John Steele
# Period: 2
# Date Last Edited: 10/20/26

#Configuring imports 
import random
from tqdm import tqdm
import time 
from room import Room
import os 
# import names 

# names.get_full_name()




#Using basic dictionaries as preset difficulties
PRESET_PROB_LOW = {"Empty" : 30, "Object" : 40, "Monster" : 30}

PRESET_PROB_MED = {"Empty" : 30, "Object" : 30, "Monster" : 40}

PRESET_PROB_HARD = {"Empty" : 25, "Object" : 25, "Monster" : 50}
    

#Easter egg: colby wuz here 
#The above easter egg was under the request of Colby Goldberg. The following individual had no part of writing the code, but simply wanted an easter egg. 

#Randomly selects room using the dictionary for chances 
def room_selection(values: dict):
    chance = 0 
    prob = random.randint(1, 100)
    for val in values:
        chance += values[val]
        if prob <= chance:
            return val 
    return val

#Random name generation for each room, simply combining to random list choices
def random_room_name():
    p_room_names_1 = ["The Cellar of", "The Library of", "The Kitchen of", "The Ballroom of", "The Office of", "The Chapel of", "The Garden of", "The Tower of", "The Pool of", "The Dining Room of", "The Armory of", "The Vault of"]
    p_room_names_2 = ["Sin", "Doom", "Despair", "Wrath", "Envy", "Sloth", "Shadows", "Greed"]

    return random.choice(p_room_names_1) + " " + random.choice(p_room_names_2)

#Basic sanity check to make sure the generated map meets all the specific requirements; should basically never fail unless something horrible has gone wrong
def map_sanity_check(map:list): 
    errors = []
    flr = 0
    #Check to see if spawn room is clear & BOSS in right room 
    if map[0][0].type != "Empty": errors.append("First room is not clear")
    if map[-1][-1].type != "Boss": errors.append("Boss not put in right position")
    #Check to make sure there are enough stairs 
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
    #If any errors, fail and print. Else, succeed. 
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

#Simple admin function used to show room layout for debugging. 
def render(map:dict):
    print()
    for floor in map:
        for room in floor:
            print("[" + room.type + "] ", end="")
        print()
    print()

#Generate the map using difficulty parameter, # of floors, # of rooms, whetheer or not to show layout and if game is base or stage two.
def map_generation(room_probability:dict, floors, rooms, debug = False, sequel = False):
    map = [] 
    #Cool library that makes loading bars, but they finish too quick for it to be cool. 
    print("Generating floors...")
    for i in tqdm(range(floors)):
        floor = [] 
        print("Generating rooms for floor " + str(i) + "...")
        for j in tqdm(range(rooms)):
            #Randomly generating room
            room_type = room_selection(room_probability)
            floor.append(Room(random_room_name(), room_type, floor=i, sequel=sequel))
        map.append(floor)
    #Goes back afterwords and forces in stairs to make sure there are ways to get up and down 
    print("Generating stairs...")
    for i in tqdm(range(floors)):
        if i == 0:
            map[i].insert(random.randint(1, rooms), Room(random_room_name(), "Stairs"))
        else:
            map[i].insert(random.randint(0, rooms), Room(random_room_name(), "Stairs"))
    #Clears the spawn room 
    map[0][0] = Room("The Antechamber of the Labyrinth", "Empty")
    #Boss for stage 1 & Boss + Mini-bosses for stage 2
    if sequel:
        for i in range(floors):
            if i == floors - 1:
                #Final boss asignment
                map[i].append(Room("The Throne of Zayan", "Boss", floor=i, sequel=True, final=True))
            else:
                #Mini boss asignment 
                map[i].append(Room("The Guardian Hall of Floor " + str(i + 1), "Boss", floor=i, sequel=True))
    if not sequel:
        for index in range(len(map[-1])):
            #Boss of stage 1 added to map, makes sure that if stairs were there then they are not overwritten. 
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
    #Renders map layout if an admin
    if debug:
        render(map)
    #Makes sure map has basic win-ability (could be won if monsters did not occur)
    sane = map_sanity_check(map)
    return map, sane 

#Gets the position of the stairs in the floor 
def stairs_column(floor:list[Room]):
    for index in range(len(floor)):
        if floor[index].type == "Stairs":
            return index

#Gets the sortest possible path the boss room 
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

# Creates a new room at that position, not really needed as we can just set the contents on the next line if necessary. 
def change_room(floor:list[Room], col:int, kind:str, contents = None):
    new_room = Room(floor[col].name, kind)
    if contents != None:
        new_room.contents = contents 
    floor[col] = new_room 

# Finds an empty room and loads in an object here, basically to meet the game requirements for certain number of items if they did not already appear on path. 
def place_item(map:list[list[Room]], path:list, index:int, item:str):
    for kind in ("Empty", "Object"):
        for j in range(index - 1, -1, -1):
            if map[path[j][0]][path[j][1]].type == kind:
                #Where the change room is called. But again, we could just do: 
                # map[path[j][0], path[j][1]] = Room(name, Object)
                # map[path[j][0], path[j][1]].contents = item
                change_room(map[path[j][0]], path[j][1], "Object", item)
                return True 
    return False 

#Kind of acts like imaginary user exploring the shortest path and having the encounters with each room, pickup items, fight monsters, check if items are suffcient for boss. 
#Orginally all of this was part of the valid function as one big check: Can user beat on shortest path? Yes/No. Sreekar reformatted it so the extra objects are added in instead of just regenerating entire map. 
def path_pass(map:list[list[Room]], path:list, patch:bool):
    # Psuedo inventory 
    swords = 0 
    stones = 0 
    for index in range(len(path)):
        i = path[index][0]
        j = path[index][1]
        room = map[i][j]
        #Encounter each room and resolves it with gain item, fight monster and win, fight monster and lose, and fight boss and win/loss.
        if room.type == "Object":
            if room.contents == "Sword" and swords + stones < 3 and (stones == 1 or swords + stones < 2):
                swords += 1 
            elif room.contents == "Magic Stone" and stones == 0:
                stones += 1 
        elif room.type == "Monster":
            if swords == 0:
                # Checks if sword can be placed before encounter with monster. 
                if patch and not place_item(map, path, index, "Sword"):
                    change_room(map[i], j, "Empty")
                return False 
            swords -= 1 
        elif room.type == "Boss":
            if swords > 0 and stones > 0:
                return True 
            if patch:
                #Checks to see if a sword or stone could be placed before boss in path to enable win. 
                if stones == 0:
                    place_item(map, path, index, "Magic Stone")
                else:
                    place_item(map, path, index, "Sword")
            return False 
    return False 

# Function to fix the current map into a working version 
def fix_map(map:list[list[Room]]):
    #Gets the shortest path 
    path = get_path(map)
    #300 attempts for path corrections 
    for attempt in range(300):
        #Checks through map to see if path is valid 
        if path_pass(map, path, True):
            break 
    #Map values 
    monsters = 0 
    swords = 0 
    off_path = []
    on_path = []
    #Checks to see values and puts rooms in to either on or off the path to boss 
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
    #Shuffles the path and not on the path. 
    random.shuffle(off_path)
    random.shuffle(on_path)
    
    #Next section is making sure minimum game elements are in map. 

    #Tries to insert monster in random off path spot 
    while monsters < 3 and len(off_path) > 0:
        spot = off_path.pop()
        change_room(map[spot[0]], spot[1], "Monster")
        monsters += 1 
    spots = off_path + on_path 
    #Tries to insert sword in random empty spot
    while swords < 4 and len(spots) > 0:
        spot = spots.pop()
        change_room(map[spot[0]], spot[1], "Object", "Sword")
        swords += 1 

#The start of the checks, first checks if general requirements are met before passing it off to the path check 
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
