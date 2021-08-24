from __future__ import annotations
from enum import Enum
import math

combos = {
        ' XXX':  5,
        'X XX':  5,
        'XX X':  5,
        'XXX ':  5,
        'XX  ':  2,
        ' XX ':  2,
        '  XX':  2,
        'X X ':  2,
        ' X X':  2,
        'X  X':  2,
        'X   ':  1,
        ' X  ':  1,
        '  X ':  1,
        '   X':  1,

        ' OOO':  -5,
        'O OO':  -5,
        'OO O':  -5,
        'OOO ':  -5,
        'OO  ':  -2,
        ' OO ':  -2,
        '  OO':  -2,
        'O O ':  -2,
        ' O O':  -2,
        'O  O':  -2,
        'O   ':  -1,
        ' O  ':  -1,
        '  O ':  -1,
        '   O':  -1,
        }


class EndState(Enum):
    O_win = 0
    X_win = 1
    tie = 2

class WinningSquare:

    def __init__(self, index, turn, immediate):
        self.index = index
        self.turn = turn
        self.immediate = immediate

class Board:

    def __init__(self, board=None, turn=None):
        self.board = board or [' '*7 for _ in range(7)]
        self.turn = turn or 'X'
        self.value = self.evaluate()
        self.end_state = None

    def print(self):
        print("\n" + self.turn + " to play")
        for i,row in enumerate(self.board):
            print(str(i) + " ", end="")
            for spot in row:
                print("|" + spot + "|", end="")
            print("")
        print("   0  1  2  3  4  5  6\n")

    def is_legal_move(self, col):
        return self.board[0][col] == ' '

    def drop_piece(self, col: int) -> Board:
        if not self.is_legal_move(col):
            print("Move: " + str(col))
            raise RuntimeError("Move is not legal")
        for i in range(len(self.board)):
            if i == 6 or self.board[i + 1][col] != ' ':
                board = self.board.copy()
                board[i] = self.board[i][:col] + self.turn + self.board[i][col+1:]
                if self.turn == 'X':
                    turn = 'O'
                else:
                    turn = 'X'
                return Board(board=board, turn=turn)

    def get_next_states(self) -> list[Board]:
        next_states = []
        for i in range(7):
            if self.is_legal_move(i):
                next_states.append(self.drop_piece(i))
        return next_states

    def check_for_tie(self):
        if self.board[0].count(' ') == 0:
            self.end_state = EndState.tie
            return True
        return False

    def evaluate(self) -> int:
        if self.check_for_tie():
            return 0
        value = 0
        self.w_squares = []

        # horizontals
        for i in range(7):
            value += self.contains_value([(i,j) for j in range(7)])

        # vertical
        for j in range(7):
            value += self.contains_value([(i,j) for i in range(7)])

        # diagonal top-left to bottom-right
        for i in range(3,-1,-1):
            value += self.contains_value(self.get_primary_diagonal((i,0)))
        for i in range(1,4):
            value += self.contains_value(self.get_primary_diagonal((0,i)))

        # diagonal top-right to bottom-left
        for i in range(3,7):
            value += self.contains_value(self.get_secondary_diagonal((0,i)))
        for i in range(1,4):
            value += self.contains_value(self.get_secondary_diagonal((i,6)))

        # check blocks of threes
        value += self._check_winning_squares()

        return value

    def _stringify(self, indices: list[tuple(int, int)]) -> str:
        ret = ""
        for index in indices:
            ret += self.board[index[0]][index[1]]
        return ret

    def contains_value(self, indices: list[tuple(int,int)]) -> int:
        line = self._stringify(indices)
        value = 0
        for pattern in ['XXXX','OOOO']:
            if pattern in line:
                if pattern == 'XXXX':
                    self.end_state = EndState.X_win
                    return math.inf
                if pattern == 'OOOO':
                    self.end_state = EndState.O_win
                    return -math.inf
        for combo in combos:
            if combo in line:
                value += combos[combo]
                if combo.count(' ') == 1: # 3 of other character
                    """ Get index that contains potentially winning square"""
                    index = indices[line.index(combo) + combo.index(' ')]
                    self._save_square(index, combo)
        return value

    def _save_square(self, index, combo):
        if 'X' in combo:
            turn = 'X'
        else:
            turn = 'O'
        """ Below logic just checking if the given index has something underneath it,
            other piece or bottom of board"""
        if index[0] == 6 or self.board[index[0] + 1][index[1]] != ' ':
            immediate = True
        elif (self.board[index[0] + 1][index[1]] == ' ' and
                (index[0] == 5 or self.board[index[0] + 2][index[1]] != ' ')):
            immediate = False
        else:
            return # dont care about square
        self.w_squares.append(WinningSquare(index, turn, immediate))

    def _check_winning_squares(self) -> int:
        """ elements of w_squares are of type WinningSquare"""
        for i in range(len(self.w_squares)):
            if (self.w_squares[i].immediate and self.turn == self.w_squares[i].turn):
                """ Then it is my turn and I have a winning square"""
                if self.turn == 'X':
                    return 1000
                else:
                    return -1000
            for j in range(i+1 ,len(self.w_squares)):
                if ((self.w_squares[i].immediate or
                    self.w_squares[j].immediate) and
                    self.w_squares[i].index != self.w_squares[j].index and 
                    self.w_squares[i].turn == self.w_squares[j].turn):
                    """ Then I have 2 winning squares and even if not my turn I will win"""
                    if self.w_squares[i].turn == 'X':
                        return 1000
                    else:
                        return -1000
        return 0

    def get_column(self, i) -> list[tuple(int,int)]:
        ret = []
        for j in range(self.board):
            ret.append((i,j))
        return ret
            

    def get_primary_diagonal(self, index: tuple(int, int)) -> list[tuple(int,int)]:
        ret = []
        while index[0] != -1 and index[1] != -1 and index[0] != 7 and index[1] != 7:
            ret.append(index)
            index = (index[0] + 1, index[1] + 1)
        return ret


    def get_secondary_diagonal(self, index: tuple(int, int)) -> list[tuple(int,int)]:
        ret = []
        while index[0] != -1 and index[1] != -1 and index[0] != 7 and index[1] != 7:
            ret.append(index)
            index = (index[0] + 1, index[1] - 1)
        return ret




