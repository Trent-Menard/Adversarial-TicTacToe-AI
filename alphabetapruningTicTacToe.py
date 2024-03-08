from random import choice
from math import inf

# The Tic-Tac-Toe board
board = [[0, 0, 0],
         [0, 0, 0],
         [0, 0, 0]]

# Function to display the game board
def Gameboard(board):
    chars = {1: 'X', -1: 'O', 0: ' '}
    for x in board:
        for y in x:
            ch = chars[y]
            print(f'| {ch} ', end='')
        print('|\n' + '_____________')
    print("")
    print('===============')
    print("")

# Function to clear the game board
def Clearboard(board):
    for x, row in enumerate(board):
        for y, col in enumerate(row):
            board[x][y] = 0


# Function to check if a player has won
def winningPlayer(board, player):
    conditions = [[board[0][0], board[0][1], board[0][2]],
                  [board[1][0], board[1][1], board[1][2]],
                  [board[2][0], board[2][1], board[2][2]],
                  [board[0][0], board[1][0], board[2][0]],
                  [board[0][1], board[1][1], board[2][1]],
                  [board[0][2], board[1][2], board[2][2]],
                  [board[0][0], board[1][1], board[2][2]],
                  [board[0][2], board[1][1], board[2][0]]]

    if [player, player, player] in conditions:
        return True

    return False

# Function to check if the game has been won
def gameWon(board):
    return winningPlayer(board, 1) or winningPlayer(board, -1)


# Function to print the game result
def printResult(board):
    if winningPlayer(board, 1):
        print('Player has won! ' + '\n')
    elif winningPlayer(board, -1):
        print('AI has won! ' + '\n')
    else:
        print('The game is over with the result of Draw' + '\n')


# Function to get the list of blank positions on the board
def blanks(board):
    blank = []
    for x, row in enumerate(board):
        for y, col in enumerate(row):
            if board[x][y] == 0:
                blank.append([x, y])
    return blank


# Function to check if the board is full
def boardFull(board):
    if len(blanks(board)) == 0:
        return True
    return False


# Function to set a move on the board
def setMove(board, x, y, player):
    board[x][y] = player


# Function to evaluate the game state
def evaluate(board):
    if winningPlayer(board, 1):
        return 1
    elif winningPlayer(board, -1):
        return -1
    else:
        return 0


# Heuristic function for the AI
def heuristic(board):
    return evaluate(board)


# Alpha-Beta Minimax algorithm for choosing the best move
def abminimax(board, depth, alpha, beta, player):
    row = -1
    col = -1
    if depth == 0 or gameWon(board):
        return [row, col, heuristic(board)]

    best_score = -inf if player == 1 else inf
    moves = blanks(board)
    for cell in moves:
        setMove(board, cell[0], cell[1], player)
        score = abminimax(board, depth - 1, alpha, beta, -player)
        setMove(board, cell[0], cell[1], 0)

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


# Function for the AI's move (playing as O)
def o_comp(board):
    if len(blanks(board)) == 9:
        x = choice([0, 1, 2])
        y = choice([0, 1, 2])
        setMove(board, x, y, -1)
        Gameboard(board)
    else:
        result = abminimax(board, len(blanks(board)), -inf, inf, -1)
        setMove(board, result[0], result[1], -1)
        Gameboard(board)


# Function for the AI's move (playing as X)
def x_comp(board):
    print(len(blanks(board)))
    if len(blanks(board)) == 9:
        x = choice([0, 1, 2])
        y = choice([0, 1, 2])
        setMove(board, x, y, 1)
        Gameboard(board)
    else:
        result = abminimax(board, len(blanks(board)), -inf, inf, 1)
        setMove(board, result[0], result[1], 1)
        Gameboard(board)

# Function for a player's move
def playerMove(board):
    valid_input = False
    while not valid_input:
        try:
            position = int(input("Enter the position (1-9): "))
            if position >= 1 and position <= 9:
                row = (position - 1) // 3
                col = (position - 1) % 3
                if board[row][col] == 0:
                    setMove(board, row, col, 1)
                    valid_input = True
                else:
                    print("Invalid move. The position is already occupied.")
            else:
                print("Invalid input. Please enter a number from 1 to 9.")
        except ValueError:
            print("Invalid input. Please enter a number from 1 to 9.")

    Gameboard(board)


# Function for player vs. player mode
def pvp():
    Clearboard(board)
    currentPlayer = 1

    while not (boardFull(board) or gameWon(board)):
        if currentPlayer == 1:
            print("The move of Player is: ")
            playerMove(board)
        else:
            print("The move of AI is: ")
            o_comp(board)
        currentPlayer *= -1

    printResult(board)


# Function for AI vs. AI mode
def ai_vs_ai():
    Clearboard(board)
    currentPlayer = 1

    while not (boardFull(board) or gameWon(board)):
        if currentPlayer == 1:
            print("The move of AI 1 is: ")
            x_comp(board)
        else:
            print("The move of AI 2 is: ")
            o_comp(board)
        currentPlayer *= -1

    printResult(board)


# pvp()
ai_vs_ai()