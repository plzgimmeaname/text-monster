import maps as dungeon
import player 
import random 
import room
import os 
import sys 
import getpass
from item import Item, WEAPONS
import storyline



game_on = True 

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "zayan"

active_window = None

def clear_screen():
    if active_window is not None:
        active_window.set_text("")
    else:
        os.system('cls' if os.name == 'nt' else 'clear')

def admin_login():
    while True:
        choice = input("Log in as admin to enable debug mode? (YES/NO): ").strip().upper()
        if choice == "NO":
            return False
        elif choice == "YES":
            username = input("Username: ").strip()
            password = getpass.getpass("Password: ")
            if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
                print("Admin access granted. Debug mode enabled.\n")
                return True
            print("Access denied.\n")
            return False
        else:
            print("I don't understand your answer. Tell me YES or NO.")

def ask_positive_int(prompt):
    while True:
        try:
            value = int(input(prompt))
        except ValueError:
            print('Not a valid number.')
            continue
        if value < 1:
            print('Must be at least 1.')
            continue
        return value



class Game:
    def __init__(self, debug:bool = False, window = None, sequel:bool = False, name = None):
        self.debug = debug
        self.window = window
        self.sequel = sequel
        self.moves = ["right"]
        self.floors_cleared = []
        if name is None:
            name = input("What is your name, adventurer?: ").strip()
        if name == "":
            name = "Adventurer"
        self.player = player.Player(name)
        if sequel:
            self.player.pickup("Health Potion")
            self.player.pickup("Health Potion")
            difficulty = dungeon.PRESET_PROB_HARD
            stories = 5
            rooms = 6
            self.player.max = 20
            self.player.hp = 20
            self.player.atk = 2
            self.player.equip_weapon(Item("Rusty Dagger", [("attack", WEAPONS["Rusty Dagger"])], 1))
            self.player.pickup("Magic Stone")
            print("<------------------------->\nThe Labyrinth of Zayan II\n")
        else:
            difficulty = None
            while True:
                while True:
                    try:
                        mapdiff = int(input("<------------------------->\nDifficulty Menu:\n1. LOW\n2. MED\n3. HIGH\nChoose your option: "))
                        break
                    except ValueError:
                        print("Invalid input. Not a number.")
                if mapdiff == 1:
                    difficulty = dungeon.PRESET_PROB_LOW
                    break
                elif mapdiff == 2:
                    difficulty = dungeon.PRESET_PROB_MED
                    break
                elif mapdiff == 3:
                    difficulty = dungeon.PRESET_PROB_HARD
                    break
                else:
                    print('Invalid input. Select either 1, 2, or 3.\n')
                    continue
            print('<------------------>\n')
            print("<------------------------->\nRooms Customization:\n")
            stories = ask_positive_int("How many floors would you like?: ")
            rooms = ask_positive_int("How many rooms would you like?: ")
        mapgen = dungeon.map_generation(difficulty, stories, (rooms - 1), debug=debug, sequel=sequel)
        self.game_map = mapgen[0]
        if mapgen[1] == 1:
            print("Map generated successfully.")
        else:
            print("Map generated with errors.")
        self.current_room: room.Room = self.game_map[self.player.y][self.player.x]

        self.valid_commands = ["RIGHT", "LEFT", "UP", "DOWN", "FIGHT", "INVENTORY", "STATUS", "PICKUP", "HELP"]# trying new way to do if-else inputs 

        self.alive = True 
        self.escaped = False 
        if not self.sequel:
            print(storyline.get_story(self.player.name))
        print("State the action you wish to take (use 'help' to get all valid commands)")
    def move_right(self):
        self.moves.append("right")
        if self.current_room.type == "Monster" and self.current_room.explored == False and self.escaped == False and not self.moves[-2] == "left":
            print("You try to flee the monster which strikes you down in the process.")
            self.alive = False 
            return
        try: 
            self.current_room = self.game_map[self.player.y][self.player.x + 1]
            self.player.move("rightward")
            self.escaped = False
        except IndexError: 
            print("There is no doorway to a room to the right.")
    def move_left(self):
        self.moves.append("left")
        if self.current_room.type == "Monster" and self.current_room.explored == False and self.escaped == False and not self.moves[-2] == "right":
            print("You try to flee the monster which strikes you down in the process.")
            self.alive = False 
            return
        try: 
            if (self.player.x - 1) >= 0:
                self.current_room = self.game_map[self.player.y][self.player.x-1]
                self.player.move("leftward")
                self.escaped = False
            else:
                print("There is no doorway to a room to the left.")
        except IndexError: 
            print("There is no doorway to a room to the left.")
    def move_up(self):
        self.moves.append('up')
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
        self.moves.append('down')
        if self.current_room.type == "Stairs":
            if self.sequel and self.player.y not in self.floors_cleared:
                print("The stairs are sealed until the guardian of this floor falls.")
                return
            try:
                self.current_room = self.game_map[self.player.y+1][self.player.x]
                self.player.move("downward")
            except IndexError:
                print("The way downward was a trick of the light, there are no further floors below.")
        else:
            print("There are no stairs to climb downwards in this room.")

    def fight(self):
        if self.current_room.explored == True or self.current_room.type not in ("Monster", "Boss"):
            print("There are no monsters to fight here.")
            return None
        else:
            monster = self.current_room.monster
            print("You face " + monster.name + "!")
            while self.player.is_alive() and monster.hp > 0:
                print()
                print(self.player.name + " HP: " + str(self.player.hp) + "/" + str(self.player.max) + " | " + monster.name + " HP: " + str(max(monster.hp, 0)) + "/" + str(monster.max))
                action = input("Fight command? (ATTACK/HEAL/FLEE/STONE): ").strip().upper()
                if action == "ATTACK":
                    if monster.dodged():
                        print(monster.name + " dodges your attack.")
                    else:
                        damage = self.player.attack()
                        print(monster.take_damage(damage))
                        if monster.hp <= 0:
                            break
                elif action == "FLEE":
                    if monster.can_flee(self.player.speed):
                        print("You slip away from " + monster.name + ".")
                        self.escaped = True
                        return None
                    print("You fail to escape!")
                elif action == "HEAL":
                    if self.player.hp >= self.player.max:
                        print("You are already at full health.")
                        continue
                    if self.player.discard("Health Potion"):
                        self.player.heal(self.player.max // 2)
                        print("You drink a health potion and recover some health.")
                    else:
                        print("You do not have a health potion.")
                        continue
                elif action == "STONE":
                    if self.player.discard("Magic Stone"):
                        self.player.heal(self.player.max)
                        print("Your magic stone dissolves into light and restores your health.")
                    else:
                        print("You do not have a magic stone.")
                        continue
                else:
                    print("Invalid fight command.")
                    continue
                if self.player.dodged():
                    print("You dodge " + monster.name + "'s attack.")
                else:
                    print(self.player.take_damage(monster.attack()))
            if not self.player.is_alive():
                print(monster.name + " strikes you down.")
                self.alive = False
                return 0
            print("You defeat " + monster.name + ". Huzzah!")
            if self.current_room.type == "Monster":
                self.player.heal(self.player.max // 8)
            if self.sequel:
                for message in self.player.gain_xp(monster.max):
                    print(message)
            if self.current_room.type == "Boss":
                if self.sequel:
                    self.floors_cleared.append(self.player.y)
                    if self.current_room.final:
                        return 2
                    self.player.heal(self.player.max)
                    print("The guardian falls. The stairs down unseal, and your wounds close.")
                    return 1
                return 2
            return 1

    def prequel_fight(self):
        if self.debug:
            return 1
        if self.current_room.explored == True:
            print("There are no monsters to fight here.")
            return 
        else:
            if self.current_room.type == "Monster": 
                if self.player.does_have("Sword"): 
                    print('OK')
                    print("You attack and defeat the monster. Huzzah!")
                    self.player.discard("Sword")
                    return 1 
                else:
                    if self.player.does_have("Magic Stone"):
                        print('OK')
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
                else:
                    print('You fail to fight the mighty dragon guarding the treasure of Zayan.') 
                    print('You lie on the ground, staring at the ceiling, watching as your life slowly ebbs away from you.')
                    self.alive = False
                    return 0

    def inventory(self):
        self.player.display_inventory() 

    def pickup(self):
        item = self.current_room.get_item() 
        if item == 0 or self.current_room.explored == True:
            print("This room does not have any items in it")
            return False
        elif item in WEAPONS:
            self.player.equip_weapon(Item(item, [("attack", WEAPONS[item])], 1))
            return True
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
            if self.window is not None:
                self.window.set_room(self.current_room.type, self.current_room.explored)
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
                    if not self.sequel:
                        outcome = self.prequel_fight()
                        if outcome == 0:
                            #clear_screen()
                            print("You have failed to delve into my labyrinth. Slain by one of my minions.")
                            break
                        elif outcome is None:
                            continue
                        elif outcome == 2:
                            print("Victorious, you claim the grand prize of The Labyrinth of Zayan: An A+/100 test grade from Mr. Miller!!")
                            print("You go home and sleep well at night, knowing the world is a little safer from the threats of the Grand and Powerful Zayan...")
                            print("The End.")
                            return 2
                        self.current_room.explore()
                    else:
                        outcome = self.fight()
                        if outcome == 0:
                            #clear_screen()
                            print("You have failed to delve into my labyrinth. Slain by one of my minions.")
                            break
                        elif outcome is None:
                            continue
                        elif outcome == 2:
                            print("Zayan falls, and the labyrinth crumbles into dust around you.")
                            print("Victorious, you walk into the Portal of Exit and out into the sunlight, the true master of the Labyrinth.")
                            print("The End.")
                            return 0
                        self.current_room.explore()
                elif user_input == "INVENTORY":
                    self.inventory() 
                elif user_input == "STATUS":
                    self.player.check_status()
                elif user_input == "PICKUP":
                    succeed = self.pickup()
                    if not succeed: continue 
                    self.current_room.explore()
                elif user_input == "HELP":
                    self.help()
                if self.debug:
                    dungeon.render(self.game_map)
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
                clear_screen()
                return 1
            elif choice == "NO":
                print("Then this labyrinth you shall strive against no further.")
                return 0 
            else:
                print("I don't understand your answer. Tell me YES or NO. ")
                continue
        
        


def launch_sequel(name):
    try:
        import window_game
    except ImportError:
        print("The sequel needs pygame to open its window. Install it with: pip install pygame")
        return
    print()
    print("You have defeated the Guardian of the Outer Tomb. However, Zayan has sealed the way out with a magical barrier.")
    print("In order to defeat him, you must go further down to beat Zayan himself and enter through the Portal of Exit.")
    print("A window opens: The Labyrinth of Zayan II.")
    sequel_window = window_game.WindowGame()
    sequel_window.hero_name = name
    sequel_window.loop()

def main(window = None, sequel = False, name = None):
    global game_on, active_window
    active_window = window
    game_on = True 
    try:
        while game_on:
            if sequel:
                game = Game(False, window, True, name)
            else:
                game = Game(admin_login(), window)
            end = game.loop()
            if end == 2:
                game_on = False 
                launch_sequel(game.player.name)
                break 
            if end == 0:
                game_on = False 
                break 
    except (EOFError, KeyboardInterrupt):
        print()
    print("Thank you for playing The Labyrinth of Zayan.")


if __name__ == "__main__":
    main()
