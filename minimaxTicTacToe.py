import math
import os
from random import choice

game_board = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0]
]

HUMAN = -1
COMPUTER = +1


def display_board(state, c_choice, h_choice):
    chars = {
        -1: h_choice,
        +1: c_choice,
        0: ' '
    }

    # str_line = '-------------'
    str_line = '_____________'

    print('\n' + str_line)
    for row in state:
        for cell in enumerate(row):
            symbol = chars[cell[1]]
            if cell[0] == 0 or cell[0] == 2:
                print(f'| {symbol} |', end='')
            elif cell[0] == 1:
                print(f' {symbol} ', end='')

        print('\n' + str_line)


# Returns all empty cells (cells where player can play).
def get_empty_cells(state):
    cells = []

    for x, row in enumerate(state):
        for y, cell in enumerate(row):
            if cell == 0:
                cells.append([x, y])
    return cells


# Returns True if specified player has won, False otherwise.
def test_player_win(state, player):
    win_states = [
        [state[0][0], state[0][1], state[0][2]],  # Row 0, horizontally
        [state[1][0], state[1][1], state[1][2]],  # Row 1, horizontally
        [state[2][0], state[2][1], state[2][2]],  # Row 2, horizontally
        [state[0][0], state[1][0], state[2][0]],  # Row 0, vertically
        [state[0][1], state[1][1], state[2][1]],  # Row 1, vertically
        [state[0][2], state[1][2], state[2][2]],  # Row 2, vertically
        [state[0][0], state[1][1], state[2][2]],  # Row 0, downwards diagonally right
        [state[2][0], state[1][1], state[0][2]],  # Row 2, upwards diagonally right
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


# Returns a utility value from the current state. +1 for COMPUTER win, -1 for HUMAN win, 0 for draw.
def evaluate(state):
    if test_player_win(state, COMPUTER):
        score = +1
    elif test_player_win(state, HUMAN):
        score = -1
    else:
        score = 0

    return score


# Choose optimal play based on state, depth & player. Returns list of [best row, best column, best score]
def minimax(state, depth, player):
    if player == COMPUTER:
        best = [-1, -1, -math.inf]
    else:
        best = [-1, -1, +math.inf]

    if depth == 0 or is_game_over(state):
        score = evaluate(state)
        return [-1, -1, score]

    for cell in get_empty_cells(state):
        x, y = cell[0], cell[1]
        state[x][y] = player
        score = minimax(state, depth - 1, -player)
        state[x][y] = 0
        score[0], score[1] = x, y

        if player == COMPUTER and score[2] > best[2]:
            best = score  # Max value
        elif player == HUMAN and score[2] < best[2]:
            best = score  # Min value

    return best


def ai_turn(computers_character, humans_character):
    depth = len(get_empty_cells(game_board))
    if depth == 0 or is_game_over(game_board):
        return

    os.system("cls")
    print("AI's turn!")

    if depth == 9:
        x = choice([0, 1, 2])
        y = choice([0, 1, 2])
    else:
        move = minimax(game_board, depth, COMPUTER)
        x, y = move[0], move[1]

    place_move(x, y, COMPUTER)
    display_board(game_board, computers_character, humans_character)
    print()


def human_turn(computers_character, humans_character):
    depth = len(get_empty_cells(game_board))
    if depth == 0 or is_game_over(game_board):
        return

    move = -1

    # Move coordinates represented sequentially from top left, 1 to bottom right, 9.
    moves = {
        1: [0, 0], 2: [0, 1], 3: [0, 2],
        4: [1, 0], 5: [1, 1], 6: [1, 2],
        7: [2, 0], 8: [2, 1], 9: [2, 2],
    }

    # todo: Clearing screen isn't working...
    os.system("cls")
    print("Your turn!")
    display_board(game_board, computers_character, humans_character)

    while move < 1 or move > 9:
        try:
            move = int(input('Choose a location (top left is 1; bottom right is 9): '))
            coord = moves[move]
            can_move = place_move(coord[0], coord[1], HUMAN)

            if not can_move:
                print("[Error]: Invalid move.")
                move = -1
        except (EOFError, KeyboardInterrupt):
            print('Program was forcibly terminated or a critical error occurred.')
            exit()
        except (KeyError, ValueError):
            print("[Error]: Invalid choice.")

    print()


def display_results(computers_character, humans_character):
    if test_player_win(game_board, HUMAN):
        display_board(game_board, computers_character, humans_character)
        print('YOU WIN!')
    elif test_player_win(game_board, COMPUTER):
        display_board(game_board, computers_character, humans_character)
        print('YOU LOSE!')
    else:
        display_board(game_board, computers_character, humans_character)
        print('DRAW!')


def player_vs_ai():
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

    # Ask user if they want to start first.
    while human_is_starting_player is None:
        user_input = input('First to start? (Y or N): ')

        if user_input.isalpha() and user_input.upper() == "Y":
            human_is_starting_player = True
        elif user_input.isalpha() and user_input.upper() == "N":
            human_is_starting_player = False

        else:
            print("[Error]: Invalid choice.")
        print()

    # Continue game until completion (Draw, Win, Loss).
    while len(get_empty_cells(game_board)) > 0 and not is_game_over(game_board):
        if not human_is_starting_player:
            ai_turn(computers_character, humans_character)

        human_turn(computers_character, humans_character)
        ai_turn(computers_character, humans_character)

    display_results(computers_character, humans_character)


def ai_vs_ai(computer1_is_starting_player: bool):
    # Computer 1/2's character choice is insignificant, so default them.
    computer1s_character = 'X'
    computer2s_character = 'O'
    # Being the starting player can be advantageous.
    computer1_is_starting_player = computer1_is_starting_player

    while len(get_empty_cells(game_board)) > 0 and not is_game_over(game_board):
        # if not computer1_is_starting_player:
        #     ai_turn(computer1s_character, computer2s_character)
        #
        # human_turn(computer1s_character, computer2s_character)
        ai_turn(computer1s_character, computer2s_character)

    display_results(computer1s_character, computer2s_character)


player_vs_ai()
# ai_vs_ai(True)

