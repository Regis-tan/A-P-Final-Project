#Imports
import random

#Defining the game_parameters class (This class contains the values for grid size and artillery placemement number)
class game_parameters:
    def __init__(self, grid_size, artillery_number):
        self.grid_size = grid_size
        self.artillery_number = artillery_number

#Defining the game_board class (This class contains the string value for the game board grid)
class game_board:
    def __init__(self, size):
        self.size = size
        self.board = [["O" for _ in range(size)] for _ in range(size)]

#Defining the print_seperator function (This function prints a seperator used to split menus)
def print_seperator():
    print("="*45)

def print_small_seperator():
    print("-"*40)

#Prints the game board with the enemy's and player's grid
def print_board(player_board, enemy_board, show_enemy_grid=True):
    print("Your Board:\t\t\tEnemy's Board:")

    #Prints the column headers for player's board.
    print("  " + " ".join(str(i + 1) for i in range(player_board.size)) + "\t\t\t\t" + "  " + " ".join(str(i + 1) for i in range(enemy_board.size)))

    #Prints the actual game board grid for both enemy and player
    for i, (player_row, enemy_row) in enumerate(zip(player_board.board, enemy_board.board)):
        enemy_row_display = " ".join(cell if cell == "x" or (not show_enemy_grid and cell == "a") else "O" if cell != "e" else "e" for cell in enemy_row)
        enemy_row_display = enemy_row_display.replace("a", "O")  # Hide enemy artillery
        player_row_display = " ".join(cell if cell != "e" else "e" for cell in player_row)
        print(chr(ord('A') + i) + " " + player_row_display + "\t\t\t\t" + chr(ord('A') + i) + " " + enemy_row_display)

#Makes a singular grid according to the game parameters with no actual data (It is used during player's placement phase)
def print_grid(size):
    #Calculate the width
    col_label_width = len(str(size)) + 1

    #Prints the columns
    print("",""*col_label_width, end="")
    for col in range(1, size + 1):
        print(f"{col:{col_label_width}}", end="")
    print()

    #Prints the grids
    for row in range(size):
        print(f"{chr(ord('A') + row):<{col_label_width - 1}}", end=" ")
        for col in range(size):
            print("O ", end="")
        print()

#Prompts the player to place down the specified number of artillery pieces.
def place_artillery(board, num_artillery,player_name):
    print_small_seperator()
    print(f"Player, enter the positions for {num_artillery} artillery pieces.")
    #For loop repeats the prompt to place an artillery piece, it will do this until the prompt has been repeated as much as the artillery number.
    for _ in range(num_artillery):
        while True:
            try:
                position = input(f"Enter the position for artillery (e.g., A-1): ").upper()
                #Takes the input and places the artillery in the desired location, it also checks if the location is available or not.
                if len(position) == 3 and position[0].isalpha() and position[1] == "-" and position[2].isdigit():
                    x = ord(position[0]) - ord('A')
                    y = int(position[2]) - 1
                    if 0 <= x < len(board) and 0 <= y < len(board) and board[x][y] == "O":
                        board[x][y] = "a"
                        break
                    else:
                        print("Invalid position. Please choose an empty cell.")
                else:
                    print("Invalid input. Please enter a valid position.")
            except ValueError:
                print("Invalid input. Please enter a valid position.")

#Enemy ai that chooses a random grid in the board using the previously imported random functions
def enemy_place_artillery(board, num_artillery):
    print("\nThe enemy is placing its artillery pieces.")
    for _ in range(num_artillery):
        #Places the artillery in a random location that is in the range of the grid
        while True:
            x = random.randint(0, len(board) - 1)
            y = random.randint(0, len(board) - 1)
            if board[x][y] == "O":
                board[x][y] = "a"
                break

#Prompts the user to input a guess and check whether the location is available or not
def get_user_guess(board):
    while True:
        try:
            guess = input(f"Your turn, enter your guess (e.g., A-1): ").upper()
            if len(guess) == 3 and guess[0].isalpha() and guess[1] == "-" and guess[2].isdigit():
                x = ord(guess[0]) - ord('A')
                y = int(guess[2]) - 1
                if 0 <= x < len(board) and 0 <= y < len(board):
                    return x, y
                else:
                    print("Invalid guess. Out of bounds.")
            else:
                print("Invalid input. Please enter a valid guess.")
        except ValueError:
            print("Invalid input. Please enter a valid guess.")

#Checks the enemy's and user's if it hits or not.
def check_guess(board, x, y):
    if board[x][y] == "a":
        print("Hit!")
        board[x][y] = "x"
        return True
    elif board[x][y] == "O" or board[x][y] or board[x][y]:
        print("Miss!")
        board[x][y] = "e"
        return False

#Returns whether the game is over or not.
def is_game_over(player_board, enemy_board, artillery_number):
    return all(all(cell != "a" for cell in row) for row in player_board.board) or all(all(cell != "a" for cell in row) for row in enemy_board.board)

#Contains most of the game's logic, it also utilizes alot of the previous functions
def game_logic(current_parameters):
    #Makes the boards for both the enemy and player the same as the parameters defined
    player_board = game_board(current_parameters.grid_size)
    enemy_board = game_board(current_parameters.grid_size)

    #Uses the previous functions (place_artiller and enemy_place_artillery)
    place_artillery(player_board.board, current_parameters.artillery_number, "Player")
    enemy_place_artillery(enemy_board.board, current_parameters.artillery_number)

    #Assigns 0 to the match_turns variable.
    match_turns = 0

    #Game main game loop.
    while True:
        #Adds 1 to the match_turns variable.
        match_turns += 1

        #Prints the boards and seperator.
        print_seperator()
        print_board(player_board, enemy_board, show_enemy_grid=False)

        #Checks if the player's guess is correct or not.
        print_small_seperator()
        player_guess = get_user_guess(enemy_board.board)
        if check_guess(enemy_board.board, *player_guess):
            current_parameters.artillery_number -= 1
            #The player has guessed correctly, it prints some extra info.
            print(f"You destroyed an enemy artillery piece! Remaining enemy artillery pieces: {current_parameters.artillery_number}")
            print_small_seperator()
        else:
            #The player has not guessed correctly, it shows the number of remaining artillery pieces and that its the enemy's turn.
            print(f"Remaining enemy artillery pieces: {current_parameters.artillery_number}")
            print_small_seperator()

        #Checks if the game is over or not and if the player or enemy won after the player's guess.
        if is_game_over(player_board, enemy_board, current_parameters.artillery_number):
            if all(all(cell != "a" for cell in row) for row in player_board.board):
                #The enemy has won, the player has no more artillery pieces.
                print(f"Game over! You lost all your artillery pieces. The enemy wins.\n-Turns taken: {match_turns}")
                input("Press enter to return to the main menu.\n")
            else:
                #The player has won, the enemy has no more artillery pieces.
                print(f"Congratulations! You destroyed all enemy artillery pieces. You win!\n-Turns taken: {match_turns}")
                input("Press enter to return to the main menu.\n")
            #Prints a seperator and calls the main_menu() function.
            print_seperator()
            main_menu()

        #Makes the enemy's turn, it chooses a random value in the board.
        enemy_guess = (random.randint(0, current_parameters.grid_size - 1), random.randint(0, current_parameters.grid_size - 1))
        print("Enemy's turn: ")
        if check_guess(player_board.board, *enemy_guess):
            #The enemy has guessed correctly.
            print("The enemy destroyed one of your artillery pieces!")

        #Prompts the user to enter something to make the game continue.
        print_small_seperator()
        input("Press enter to continue.\n")

        #Checks if the game is over or not and if the player or enemy won after the enemy's guess.
        if is_game_over(player_board, enemy_board, current_parameters.artillery_number):
            if all(all(cell != "a" for cell in row) for row in player_board.board):
                #The enemy has won, the player has no more artillery pieces.
                print(f"Game over! You lost all your artillery pieces. The enemy wins.\n-Turns taken: {match_turns}")
                input("Press enter to return to the main menu.\n")
            else:
                #The player has won, the enemy has no more artillery pieces.
                print(f"Congratulations! You destroyed all enemy artillery pieces. You win!\n-Turns taken: {match_turns}")
                input("Press enter to return to the main menu.\n")
            #Prints a seperator and calls the main_menu() function.
            print_seperator()
            main_menu()

#Defines the set_parameters() function.
def set_parameters():
    #Prompts the user to enter game parameters.
    print("Please enter your game parameters.")
    
    try:
        grd_size = int(input("Enter the grid size: "))
        arty_num = int(input("Enter the number of artillery pieces: "))
    except ValueError:
        print("Value error, please input a single integer value.")
        print_small_seperator()
        return set_parameters()

    grds = grd_size**2

    if grds < arty_num:
        print("You cannot have more artillery pieces than grids.")
        print_small_seperator()
        return set_parameters()
    elif grds > 81:
        print("Your grid cannot be bigger than 9x9.")
        print_small_seperator()
        return set_parameters()
    else:
        print_small_seperator()
        return grd_size, arty_num


#Defines the main_menu() function, it displays all the options available and also prompts the users to input a string (0,1,2).
def main_menu():
    print("Welcome to Artillery Commander!")
    print(" 1. Enter game \n 2. Help \n 0. Exit")
    main_option = str(input("Enter option (0-2): "))
    print_seperator()
    if main_option == "1":
        #Goes into the game.
        game_menu()
    elif main_option == "2":
        #Goes into the help menu.
        help_menu()
    elif main_option == "0":
        #Ends the program.
        print("Thanks for playing the game.")
        exit()
    else:
        #Unavailable option.
        print("Option unavailable")
        print_seperator()
        main_menu()
    
#Defines the help_menu() function, it displays information that the player can use to know how to play the game.
def help_menu():
    print("Help Menu")
    print("-Set game parameters, grid size (length of side) and number of artillery pieces. \n-Place artillery pieces, only one artillery piece can occupy a grid. \n-Guess enemy artillery locations. \n-The player loses when they have no artillery pieces remaining. \nExtra Notes: \n  -'a' indicates your artillery pieces \n  -'x' indicates destroyed artillery pieces \n  -'e' indicates an empty grid that has been hit")
    #Asks the user to press enter to return to the menu.
    input("Press enter to return to the main menu.\n")
    print_seperator()
    main_menu()

#Defines the game_menu() function, it utilizes the game_logic() function and also asks the user for the game parameters(grid size and artillery placement number.).
def game_menu():
    #Assigns values to grid_size and artillery_number.
    parameter_list = set_parameters()
    grid_size = parameter_list[0]
    artillery_number = parameter_list[1]

    #Makes an object fron the class game_parameters with the current parameter variables.
    current_parameters = game_parameters(grid_size, artillery_number)

    #Prints the parameters chosen and a grid to show the player.
    print(f"Game parameters set! Grid Size = {current_parameters.grid_size}x{current_parameters.grid_size}, Artillery Amount = {current_parameters.artillery_number}")
    print_seperator()
    print("Your grid:")
    print_grid(grid_size)

    #Calls the game_logic() function and gives it the current parameters, this starts the gameplay loop.
    game_logic(current_parameters)

#Calls the game and seperator function to open the program.
print_seperator()
main_menu()