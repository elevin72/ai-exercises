from abminimax import *
from board import *

DEPTH = 2

board = Board()
while True:
    user = input("Select you color.\nX to go first, O to go second\n")
    if user == 'X' or user == 'O':
        break
print("Game start.\nX goes first.\nEnter a number 0-6 to drop a piece on the board.")

while board.value != math.inf and board.value != -math.inf:
    board.print()
    if board.turn == user:
        move = int(input("Your turn: "))
        while not board.is_legal_move(move):
            move = int(input("Illegal, please try again: "))
        board = board.drop_piece(move)
    else:
        board = ab_minimax(board, DEPTH, -math.inf, math.inf, user == 'O')[1]

board.print()
if (board.value > 0 and user == 'X' or
    board.value < 0 and user == 'O'):
    print("Congratulations, you won!")
else:
    print("Better luck next time")
