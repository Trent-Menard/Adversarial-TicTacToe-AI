import alphabetapruningTicTacToe
import minimaxTicTacToe
from minimaxTicTacToe import get_empty_cells, is_game_over, test_player_win, display_board, \
    minimax, place_move
from alphabetapruningTicTacToe import abminimax
from random import choice

game_board = minimaxTicTacToe.game_board
HUMAN = minimaxTicTacToe.HUMAN
COMPUTER = minimaxTicTacToe.COMPUTER


# Same as minimaxTicTacToe.ai_turn() except passes player to act as either HUMAN or COMPUTER.
def ai_turn_new(player):
    depth = len(get_empty_cells(game_board))
    if depth == 0 or is_game_over(game_board):
        return

    print("AI's turn!")

    if depth == 9:
        x = choice([0, 1, 2])
        y = choice([0, 1, 2])
    else:
        move = minimax(game_board, depth, player)
        x, y = move[0], move[1]

    place_move(x, y, player)
    # display_board(game_board, computers_character, humans_character)
    print()

# humans_character = None
# computers_character = None
# human_is_starting_player = None
#
# Continue game until completion (Draw, Win, Loss).


while len(get_empty_cells(game_board)) > 0 and not is_game_over(game_board):
    ai_turn_new(COMPUTER)
    print(game_board)

    # -1: AI, O
    # 1: Human, X

    res = all.o_comp(game_board)
    print(game_board)

# # Game over message
# if test_player_win(game_board, HUMAN):
#     display_board(game_board, computers_character, humans_character)
#     print('YOU WIN!')
# elif test_player_win(game_board, COMPUTER):
#     display_board(game_board, computers_character, humans_character)
#     print('YOU LOSE!')
# else:
#     display_board(game_board, computers_character, humans_character)
#     print('DRAW!')