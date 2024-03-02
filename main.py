import math

game_board = [
    ['_', '_', '_'],
    ['_', '_', '_'],
    ['_', '_', '_']
]


def calculate_min(state):
    utility = math.inf
    for s in state:
        utility = min(utility, calculate_max(state))
    return utility


def calculate_max(state):
    utility = -math.inf
    for s in state:
        utility = max(utility, calculate_min(state))
    return utility


def play_x(state, is_initial_play):
    if is_initial_play:
        # Center is always optimal play.
        state[1][1] = 'X'


def play_o(state, is_initial_play):
    if is_initial_play:
        # Center is always optimal play.
        state[1][1] = 'O'


def display_board():
    for x in game_board:
        for y in enumerate(x):
            if y[0] == len(game_board) - 1:
                print(y[1], end="")
            else:
                print(y[1], " ", end="")
        print()
    print()


play_x(game_board, True)

# display_board(game_board)
# print(game_board)
# print("Choices are as follows:\n1 2 3\n4 5 6\n6 7 8\n")

humans_character = None
computers_character = None
human_is_starting_player = None

while humans_character is None:
    choice = input('Choose your character (X or O): ')

    if choice.isalpha() and choice.upper() == "X":
        humans_character = 'X'
        computers_character = 'O'
    elif choice.isalpha() and choice.upper() == "O":
        humans_character = 'O'
        computers_character = 'X'
    else:
        print("[Error]: Invalid choice.")
    print()

while human_is_starting_player is None:
    choice = input('First to start? (Y or N): ')

    if choice.isalpha() and choice.upper() == "Y":
        human_is_starting_player = True
        print("Go.")
    elif choice.isalpha() and choice.upper() == "N":
        print("Waiting for AI's choice.")
    else:
        print("[Error]: Invalid choice.")
    print()


choice = input('Choose a location (top left is 1; bottom right is 9): ')
if choice.isdigit() and 1 <= int(choice) <= 9:
    print("Good.")
else:
    print("[Error]: Invalid choice.")

# def determine_winner(state):


def get_empty_cells(state):
    cells = []

    for x, row in enumerate(state):
        for y, cell in enumerate(row):
            if cell == '_':
                cells.append([x, y])

    return cells


def is_valid_move(x, y):
    return [x, y] in get_empty_cells(game_board)

# def is_valid_move(x, y):
#     return [x, y] in game_board == '_'
