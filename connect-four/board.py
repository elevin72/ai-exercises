from __future__ import annotations
from enum import Enum
import math
import random

WIDTH = 7
HEIGHT = 6

combos = {
        ' XXX':  30,
        'X XX':  30,
        'XX X':  30,
        'XXX ':  30,
        'XX  ':  5,
        ' XX ':  5,
        '  XX':  5,
        'X X ':  5,
        ' X X':  5,
        'X  X':  5,
        'X   ':  1,
        ' X  ':  1,
        '  X ':  1,
        '   X':  1,

        ' OOO':  -30,
        'O OO':  -30,
        'OO O':  -30,
        'OOO ':  -30,
        'OO  ':  -5,
        ' OO ':  -5,
        '  OO':  -5,
        'O O ':  -5,
        ' O O':  -5,
        'O  O':  -5,
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
    
    @staticmethod
    def is_winning(s1: WinningSquare, s2: WinningSquare) -> bool:
        if s1.turn == s2.turn:
            if s1.immediate and s2.immediate and s1.index != s2.index:
                return True
            if (s1.immediate or s2.immediate) and abs(s1.index[0] - s2.index[0]) == 1 and s1.index[1] == s2.index[1]:
                return True
        return False

class Board:

    def __init__(self, board=None, turn=None):
        self.board = board or [' '*WIDTH for _ in range(HEIGHT)]
        self.turn = turn or 'X'
        self.end_state = None
        self.value = self.evaluate()

    def print(self):
        print("\n" + self.turn + " to play")
        for i,row in enumerate(self.board):
            print(str(HEIGHT-i), end="")
            for spot in row:
                print("|" + spot, end="")
            print("|")
        print("  1 2 3 4 5 6 7\n")

    def is_legal_move(self, col):
        return self.board[0][col] == ' '

    def play(self, col: int) -> Board:
        # if not self.is_legal_move(col):
        #     print("Move: " + str(col))
        #     raise RuntimeError("Move is not legal")
        for i in range(len(self.board)):
            if i == HEIGHT-1 or self.board[i + 1][col] != ' ':
                board = self.board.copy()
                board[i] = self.board[i][:col] + self.turn + self.board[i][col+1:]
                if self.turn == 'X':
                    turn = 'O'
                else:
                    turn = 'X'
                return Board(board=board, turn=turn)

    def get_next_states(self) -> list[Board]:
        next_states = []
        for i in range(WIDTH):
            if self.is_legal_move(i):
                next_states.append(self.play(i))
        if next_states == []:
            self.end_state = EndState.tie
        random.shuffle(next_states)
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
        for i in range(HEIGHT):
            value += self.contains_value([(i,j) for j in range(WIDTH)])

        # vertical
        for j in range(WIDTH):
            value += self.contains_value([(i,j) for i in range(HEIGHT)])

        # diagonal top-left to bottom-right
        for i in range(4):
            value += self.contains_value(self.get_primary_diagonal((0,i)))
        for i in range(1,3):
            value += self.contains_value(self.get_primary_diagonal((i,0)))

        # diagonal top-right to bottom-left
        for i in range(3,7):
            value += self.contains_value(self.get_secondary_diagonal((0,i)))
        for i in range(1,3):
            value += self.contains_value(self.get_secondary_diagonal((i,6)))

        # check blocks of threes
        value += self._check_winning_squares()

        return value

    def _stringify(self, indices: list[tuple(int, int)]) -> str:
        ret = ""
        for index in indices:
            ret += self.board[index[0]][index[1]]
        return ret

    def game_over(self):
        return self.end_state != None

    def _game_over(self, line: str) -> int:
        for pattern in ['XXXX','OOOO']:
            if pattern in line:
                if pattern == 'XXXX':
                    self.end_state = EndState.X_win
                    return math.inf
                if pattern == 'OOOO':
                    self.end_state = EndState.O_win
                    return -math.inf
        return 0

    def contains_value(self, indices: list[tuple(int,int)]) -> int:
        line = self._stringify(indices)
        value = 0
        value += self._game_over(line)
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
        if index[0] == HEIGHT - 1 or self.board[index[0] + 1][index[1]] != ' ':
            immediate = True
        elif (self.board[index[0] + 1][index[1]] == ' ' and
                (index[0] == HEIGHT - 2 or self.board[index[0] + 2][index[1]] != ' ')):
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
                if WinningSquare.is_winning(self.w_squares[i], self.w_squares[j]):
                    """ Then I have 2 winning squares and even if it is not my turn I will win"""
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
        while index[0] != -1 and index[1] != -1 and index[0] != HEIGHT and index[1] != WIDTH:
            ret.append(index)
            index = (index[0] + 1, index[1] + 1)
        return ret

    def get_secondary_diagonal(self, index: tuple(int, int)) -> list[tuple(int,int)]:
        ret = []
        while index[0] != -1 and index[1] != -1 and index[0] != HEIGHT and index[1] != WIDTH:
            ret.append(index)
            index = (index[0] + 1, index[1] - 1)
        return ret




