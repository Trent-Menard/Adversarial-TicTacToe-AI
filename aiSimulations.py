import math
import sys
from random import choice
from time import time, sleep

game_board = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0]
]

HUMAN = -1
COMPUTER = +1

humans_character = 'X'
computers_character = 'O'


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


def set_move_ABP(board, x, y, player):
    board[x][y] = player


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


# Alpha-Beta Minimax algorithm for choosing the best move
def abminimax(board, depth, alpha, beta, player):
    row = -1
    col = -1
    if depth == 0 or is_game_over(board):
        return [row, col, evaluate(board)]

    best_score = -math.inf if player == 1 else math.inf
    moves = get_empty_cells(board)
    for cell in moves:
        set_move_ABP(board, cell[0], cell[1], player)
        score = abminimax(board, depth - 1, alpha, beta, -player)
        set_move_ABP(board, cell[0], cell[1], 0)

        if player == 1:
            if score[2] > best_score:
                best_score = score[2]
                row = cell[0]
                col = cell[1]
                alpha = max(alpha, best_score)
                if alpha >= beta:
                    break
        else:
            if score[2] < best_score:
                best_score = score[2]
                row = cell[0]
                col = cell[1]
                beta = min(beta, best_score)
                if alpha >= beta:
                    break

    return [row, col, best_score]


def MM_turn(board, computers_character, humans_character, verbose=False):
    depth = len(get_empty_cells(game_board))
    if depth == 0 or is_game_over(game_board):
        return

    if depth == 9:
        x = choice([0, 1, 2])
        y = choice([0, 1, 2])
    else:
        move = minimax(game_board, depth, COMPUTER)
        x, y = move[0], move[1]

    set_move_ABP(board, x, y, COMPUTER)

    if verbose:
        print("AI O's turn!")
        display_board(game_board, computers_character, humans_character)
        print()


def ABP_turn(board, verbose=False):
    if len(get_empty_cells(board)) == 0:
        return

    if len(get_empty_cells(board)) == 9:
        x = choice([0, 1, 2])
        y = choice([0, 1, 2])
        set_move_ABP(board, x, y, -1)
    else:
        result = abminimax(board, len(get_empty_cells(board)), -math.inf, math.inf, -1)
        set_move_ABP(board, result[0], result[1], -1)

    if verbose:
        print("AI X's turn!")
        display_board(game_board, computers_character, humans_character)
        print()


games_played = 0
ai_x_wins = 0
ai_o_wins = 0
draws = 0

ai_x_decision_time = 0
ai_o_decision_time = 0

GAMES_PER_SIMULATION = 100
GAME_ITERATIONS = 3

print("Running simulations, please wait.")

for i in range(0, GAME_ITERATIONS):
    for x in range(0, GAMES_PER_SIMULATION):
        print(f"\rIteration: {i + 1}/{GAME_ITERATIONS}, simulation: {x + 1}/{GAMES_PER_SIMULATION}", end="", flush=True)

        # Continue game until completion (Draw, Win, Loss).
        while len(get_empty_cells(game_board)) > 0 and not is_game_over(game_board):
            start_time = time()
            MM_turn(game_board, computers_character, humans_character)
            end_time = time()
            ai_o_decision_time = ai_o_decision_time + (end_time - start_time)

            start_time = time()
            ABP_turn(game_board)
            end_time = time()
            ai_x_decision_time = ai_x_decision_time + (end_time - start_time)

        if test_player_win(game_board, computers_character):
            ai_o_wins = ai_o_wins + 1
        elif test_player_win(game_board, humans_character):
            ai_x_wins = ai_x_wins + 1
        else:
            draws = draws + 1

        # display_results(computers_character, humans_character)
        games_played = games_played + 1

        # Reset the board.
        game_board = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]

print()
print()
print(f"Games played: {games_played}")
print(f"AI X wins: {ai_x_wins}")
print(f"AI O wins: {ai_o_wins}")
print(f"Draws: {draws}")
print(f"AI X total decision time: {ai_x_decision_time} seconds")
print(f"AI O total decision time: {ai_o_decision_time} seconds")
