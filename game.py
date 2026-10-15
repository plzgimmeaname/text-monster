## NAMES: 
## Period:
## Date Last Edited: 
## Text monster game: The goal of this game is to beat the monsters and claim the prize at the end of the dungeon.

# Map of the dungeon
# Feel free to adapt and design your own level. The whole map must be at least 3 floors and 15 rooms total, though.
map = [['prize', 'boss monster', 'sword', 'sword', 'stairs down'], # top floor
       ['magic stones', 'monster', 'stairs down', 'empty', 'stairs up'], # middle floor
       ['empty', 'sword', 'stairs up', 'monster', 'empty']] # bottom floor
          # ^ player starts here

# Items in the player's possession
inventory = {}

# Player's current position in the dungeon
# The player starts in the first room on floor 2
currentFloor = 2 # This is the "bottom floor"
currentRoom = 0 # This is the first empty room on the bottom floor

# Keep track of whether the game is in progress or over (so we know when to stop the game loop)
gameOver = False
gameState = ""

while not gameOver:
    # Describe the room the player is in
    room = map[currentFloor][currentRoom]


    if room == 'empty':
        print('You are in an empty room.')
    # You need to handle describing the other cases..
    elif room == 'sword':
        print("There is a sword in this room.")

    # Get command from the player
    choice = input('Command? ')

    # Respond to command
    if choice == 'help':
        # Help: display all commands
        print("TODO: Implement")
    elif choice == 'left':
        print("TODO: Implement")
    else:
        print('Command not recognized. Type "help" to see all commands.')

# end while loop

if gameState == 'won':
    print('You won the game! :)')
else:
    print('You lost the game. :( Maybe next time.')