import math
from random import choice

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


def display_board():
    for x in game_board:
        for y in enumerate(x):
            if y[0] == len(game_board) - 1:
                print(y[1], end="")
            else:
                print(y[1], " ", end="")
        print()
    print()

# display_board(game_board)
# print(game_board)
# print("Choices are as follows:\n1 2 3\n4 5 6\n6 7 8\n")


HUMAN = -1
COMPUTER = +1

humans_character = None
computers_character = None
human_is_starting_player = None


# Ask user if they want to be X or O.
while humans_character is None:
    user_input = input('Choose your character (X or O): ')

    if user_input.isalpha() and user_input.upper() == "X":
        humans_character = 'X'
        computers_character = 'O'
    elif user_input.isalpha() and user_input.upper() == "O":
        humans_character = 'O'
        computers_character = 'X'
    else:
        print("[Error]: Invalid choice.")
    print()

# Ask user if they want to start first.
while human_is_starting_player is None:
    user_input = input('First to start? (Y or N): ')

    if user_input.isalpha() and user_input.upper() == "Y":
        human_is_starting_player = True
        print("Go.")
    elif user_input.isalpha() and user_input.upper() == "N":
        human_is_starting_player = False
        print("Waiting for AI's choice.")

    else:
        print("[Error]: Invalid choice.")
    print()


# Returns all empty cells (cells where player can play).
def get_empty_cells(state):
    cells = []

    for x, row in enumerate(state):
        for y, cell in enumerate(row):
            if cell == '_':
                cells.append([x, y])
    return cells


# Returns True if specified player has won, False otherwise.
def test_player_win(state, player):
    win_states = [
        [state[0][0], state[0][1], state[0][2]], # Row 0, horizontally
        [state[1][0], state[1][1], state[1][2]], # Row 1, horizontally
        [state[2][0], state[2][1], state[2][2]], # Row 2, horizontally
        [state[0][0], state[1][0], state[2][0]], # Row 0, vertically
        [state[0][1], state[1][1], state[2][1]], # Row 1, vertically
        [state[0][2], state[1][2], state[2][2]], # Row 2, vertically
        [state[0][0], state[1][1], state[2][2]], # Row 0, downwards diagonally right
        [state[2][0], state[1][1], state[0][2]], # Row 2, upwards diagonally right
    ]

    return [player, player, player] in win_states


# Returns True if player can play at specified cell, False otherwise.
def is_valid_move(x, y):
    return [x, y] in get_empty_cells(game_board)


# Returns True if a player has won the game, False otherwise.
def is_game_over(state):
    return test_player_win(state, HUMAN) or test_player_win(state, COMPUTER)


# Places the X/O onto the board if it's a valid move.
def place_move(x, y, player):
    if is_valid_move(x, y):
        game_board[x][y] = player
        return True
    else:
        return False


# Simulates the current game board state. +1 for COMPUTER win, -1 for HUMAN win, 0 for draw.
def run_simulation(state):
    if test_player_win(state, COMPUTER):
        score = +1
    elif test_player_win(state, HUMAN):
        score = -1
    else:
        score = 0

    return score


def minimax(state, depth, player):
    if player == COMPUTER:
        best = [-1, -1, -math.inf]
    else:
        best = [-1, -1, +math.inf]

    if depth == 0 or is_game_over(state):
        score = run_simulation(state)
        return [-1, -1, score]

    # todo: Finish implementation. Why [-1, -1, ...]?


def ai_turn(computers_choice, humans_choice):
    depth = len(get_empty_cells(game_board))
    if depth == 0 or is_game_over(game_board):
        return

    if depth == 9:
        x = choice([0, 1, 2])
        y = choice([0, 1, 2])
    else:
        move = minimax(game_board, depth, COMPUTER)
        x, y = move[0], move[1]

    place_move(x, y, COMPUTER)


# Continue game until completion (Draw, Win, Loss).
while len(get_empty_cells(game_board)) > 0 and not is_game_over(game_board):
    if not human_is_starting_player:
        ai_turn(computers_character, humans_character)

    display_board()

    # todo: Human choice implementation
    user_input = input('Choose a location (top left is 1; bottom right is 9): ')
    if user_input.isdigit() and 1 <= int(user_input) <= 9:
        print("Good.")

    else:
        print("[Error]: Invalid choice.")

    ai_turn(computers_character, humans_character)
