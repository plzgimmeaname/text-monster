import maps as map 
import player 
import random 
import room
import os 
import sys 



game_on = True 



class Game:
    def __init__(self, debug:bool = False):
        self.debug = debug
        self.player = player.Player()
        difficulty = None
        while True:
            while True:
                try:
                    mapdiff = int(input("<------------------------->\nDifficulty Menu:\n1. LOW\n2. MED\n3. HIGH\nChoose your option: "))
                    break
                except ValueError:
                    print("Invalid input. Not a number.")
            if mapdiff == 1:
                difficulty = map.PRESET_PROB_LOW
                break
            elif mapdiff == 2:
                difficulty = map.PRESET_PROB_MED
                break
            elif mapdiff == 3:
                difficulty = map.PRESET_PROB_HARD
                break
            else:
                print('Invalid input. Select either 1, 2, or 3.\n')
                continue
        print('<------------------>\n')
        print("<------------------------->\nRooms Customization:\n")
        while True:
            try:
                stories = int(input("How many floors would you like?: "))
                break
            except ValueError:
                print('Not a valid number.')
                continue
        while True:
            try:
                rooms = int(input("How many rooms would you like?: "))
                break
            except ValueError:
                print('Not a valid number.')
                continue
        mapgen = map.map_generation(difficulty, stories, rooms, debug=debug)
        self.game_map = mapgen[0]
        if mapgen[1] == 1:
            print("Map generated successfully.")
        else:
            print("Map generated with errors.")
        self.current_room: room.Room = self.game_map[self.player.y][self.player.x]

        self.valid_commands = ["RIGHT", "LEFT", "UP", "DOWN", "FIGHT", "INVENTORY", "PICKUP", "HELP"]# trying new way to do if-else inputs 

        self.alive = True 
        print("State the action you wish to take (use 'help' to get all valid commands)")

    def move_right(self):
        if self.current_room.type == "Monster" and self.current_room.explored == False:
            print("You try to flee the monster which strikes you down in the process.")
            self.alive = False 
        try: 
            self.current_room = self.game_map[self.player.y][self.player.x + 1]
            self.player.move("rightward")
        except IndexError: 
            print("There is no doorway to a room to the right.")
    def move_left(self):
        if self.current_room.type == "Monster" and self.current_room.explored == False:
            print("You try to flee the monster which strikes you down in the process.")
            self.alive = False 
        try: 
            if (self.player.x - 1) >= 0:
                self.current_room = self.game_map[self.player.y][self.player.x-1]
                self.player.move("leftward")
            else:
                print("There is no doorway to a room to the left.")
        except IndexError: 
            print("There is no doorway to a room to the left.")
    def move_up(self):
        if self.current_room.type == "Stairs":
            try:
                if (self.player.y - 1) >= 0:
                    self.current_room = self.game_map[self.player.y-1][self.player.x]
                    self.player.move("upward")
                else:
                    print("The way upwards was a trick of the light, there are no further floors above.")
            except IndexError:
                print("The way upwards was a trick of the light, there are no further floors above.")
        else:
            print("There are no stairs to climb upwards in this room.")
    def move_down(self):
        if self.current_room.type == "Stairs":
            try:
                self.current_room = self.game_map[self.player.y+1][self.player.x]
                self.player.move("downward")
            except IndexError:
                print("The way downward was a trick of the light, there are no further floors below.")
        else:
            print("There are no stairs to climb downwards in this room.")

    def fight(self):
        if self.debug:
            return 1
        if self.current_room.explored == True:
            print("There are no monsters to fight here.")
            return 
        else:
            if self.current_room.type == "Monster": 
                if self.player.does_have("Sword"): 
                    print("You attack and defeat the monster. Huzzah!")
                    self.player.discard("Sword")
                    return 1 
                else:
                    if self.player.does_have("Magic Stone"):
                        print("You are caught offguard without a weapon, but your magic stone dissolves into light and banishes the monster, saving you.")
                        self.player.discard("Magic Stone")
                        return 1 
                    else:
                        print("You are caught offguard without a weapon and are swiftly devoured by the monster.")
                        self.alive = False
                        return 0 
            elif self.current_room.type == "Boss":
                if self.player.does_have("Sword") and self.player.does_have("Magic Stone"):
                    os.system('cls')
                    print("You fight a hard and long battle against the great and terrible dragon.")
                    print("Just before the dragon strikes you with its mighty fangs...")
                    print("Your magical gem glows, blinding the dragon.")
                    print("You strike and slay the monster!")
                    return 2 

    def inventory(self):
        self.player.display_inventory() 

    def pickup(self):
        item = self.current_room.get_item() 
        if item == 0 or self.current_room.explored == True:
            print("This room does not have any items in it")
            return False
        else:
            self.player.pickup(item)
            return True 


    def help(self):
        print()
        print("|HELP: VALID COMMANDS|")
        for command in self.valid_commands: 
            print("   - " + command)
        print("|--------------------|")
        print()


    def loop(self):  
        while self.alive: 
            print() 
            print("<--- Room " + str(self.player.x + 1) + " | Floor " + str(self.player.y + 1) + " --->")   
            room_type = self.current_room.enter()
            if room_type == "Empty":
                self.current_room.explore()
            user_input = input("Command?: ")
            user_input = user_input.upper()  
            if user_input in self.valid_commands:
                if user_input == "RIGHT":
                    self.move_right()
                elif user_input == "LEFT":
                    self.move_left()
                elif user_input == "UP":
                    self.move_up() 
                elif user_input == "DOWN":
                    self.move_down()
                elif user_input == "FIGHT":
                    outcome = self.fight()
                    if outcome == 0:
                        #os.system('cls')
                        print("You have failed to delve into my labyrinth. Devoured by one of my minions.")
                        break
                    elif outcome == 2:
                        print("Victorious, you claim the grand prize of The Labyrinth of Zayan: An A+/100 test grade from Mr. Miller!!")
                        print("You go home and sleep well at night, doint the world is a little safer from the threats of the Grand and Powerful Zayan...")
                        print("The End.")
                        print("Thank you for playing The Labyrinth of Zayan.")
                        sys.exit(0)
                    self.current_room.explore()
                elif user_input == "INVENTORY":
                    self.inventory() 
                elif user_input == "PICKUP":
                    succeed = self.pickup()
                    if not succeed: continue 
                    self.current_room.explore()
                elif user_input == "HELP":
                    self.help()
                if self.debug:
                    map.render(self.game_map)
            else:
                print("Invalid Command.")
                continue 
            print("<------------------------>")
        print("However, I am a fair evil overlord... I shall grant you another chance, should you accept it.")
        print("     -- Zayan, master of the labyrinth")
        while True:
            choice = input("Try again? ")
            choice = choice.strip()
            choice = choice.upper() 
            if choice == "YES":
                os.system('cls')
                return 1
            elif choice == "NO":
                print("Then this labyrinth you shall strive against no further.")
                return 0 
            else:
                print("I don't understand your answer. Tell me YES or NO. ")
                continue
        
        


if __name__ == "__main__":
    while game_on:
        game = Game(True)
        end = game.loop()
        if end == 0:
            game_on = False 
            break 
        else:
            continue
    print("Thank you for playing The Labyrinth of Zayan.")