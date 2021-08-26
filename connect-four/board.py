from __future__ import annotations
from collections import namedtuple
from enum import Enum
import math
import random

WIDTH = 7
HEIGHT = 6

combos = {
        ' XXX':  10,
        'X XX':  10,
        'XX X':  10,
        'XXX ':  10,
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

        ' OOO':  -10,
        'O OO':  -10,
        'OO O':  -10,
        'OOO ':  -10,
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

Index = namedtuple('Index', 'row col')

class Threat:
    def __init__(self, index: Index, turn: str):
        self.index = index
        self.turn = turn
    
    def is_one_away(self, other) -> bool:
        return abs(self.index.row - other.index.row) == 1 and self.index.col == other.index.col

    def __eq__(self, o: object) -> bool:
        return self.index == o.index and self.turn == o.turn

    def __hash__(self) -> int:
        return hash(self.index.row) + hash(self.index.col) + hash(self.turn)


    
class Board:

    def __init__(self, board=None, turn=None):
        self.board = board or [' '*WIDTH for _ in range(HEIGHT)]
        self.turn = turn or 'X'
        if self.turn == 'X':
            self.parity = 1
            self.factor = 1
        else:
            self.parity = 0
            self.factor = -1
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
        self._print()

    def _print(self):
        print("b = Board(")
        print("       ['" + self.board[0] + "',")
        print("        '" + self.board[1] + "',")
        print("        '" + self.board[2] + "',")
        print("        '" + self.board[3] + "',")
        print("        '" + self.board[4] + "',")
        print("        '" + self.board[5] + "'],")
        print("        '" + self.turn + "')")

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

        value = 0
        self.x_threats = set()
        self.o_threats = set()

        # horizontals
        for i in range(HEIGHT):
            value += self.contains_value([Index(i,j) for j in range(WIDTH)])

        # vertical
        for j in range(WIDTH):
            value += self.contains_value([Index(i,j) for i in range(HEIGHT)])

        # diagonal top-left to bottom-right
        for i in range(4):
            value += self.contains_value(self.get_primary_diagonal(Index(0,i)))
        for i in range(1,3):
            value += self.contains_value(self.get_primary_diagonal(Index(i,0)))

        # diagonal top-right to bottom-left
        for i in range(3,7):
            value += self.contains_value(self.get_secondary_diagonal(Index(0,i)))
        for i in range(1,3):
            value += self.contains_value(self.get_secondary_diagonal(Index(i,6)))

        # check threats
        value += self._check_threats1(self.x_threats)
        value += self._check_threats1(self.o_threats)
        value += self._check_threats2(self.x_threats, 1)
        value += self._check_threats2(self.o_threats, 0)

        if self.end_state == None and self.check_for_tie():
            return 0

        return value

    def _stringify(self, indices: list[Index]) -> str:
        ret = ""
        for index in indices:
            ret += self.board[index.row][index.col]
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

    # save local threats, and pre-threats
    def contains_value(self, indices: list[Index]) -> int:
        line = self._stringify(indices)
        value = 0
        value += self._game_over(line)
        for combo in combos:
            if combo in line:
                value += combos[combo]
                if combo.count(' ') == 1: # 3 of other character
                    """ Get index that contains threat"""
                    index = indices[line.index(combo) + combo.index(' ')]
                    self._save_threat(index, combo)
        return value

    def _save_threat(self, index: Index, combo: str):
        if 'X' in combo:
            self.x_threats.add(Threat(index, 'X'))
        else:
            self.o_threats.add(Threat(index, 'O'))

    def _check_threats1(self, threats: set[Threat]) -> int:
        immediates = 0
        value = 0
        for t1 in threats:
            if t1.index.row == HEIGHT - 1 or self.board[t1.index.row + 1][t1.index.col] != ' ':
                if t1.turn == self.turn:
                    value += 10000 * self.factor
                immediates += 1
            if immediates > 1:
                value += 10000 * self.factor
            for t2 in threats:
                if t1.is_one_away(t2):
                    if t1.turn == 'X':
                        factor = 1
                    else:
                        factor = -1
                    value += 100 * factor # * (t1.index.row + t2.index.row) # a lil janky
        return value

    def _check_threats2(self, threats: set[Threat], parity) -> int:
        value = 0
        for threat in threats:
            if threat.index.row % 2 == parity:
                if threat.turn == 'X':
                    factor = 1
                else:
                    factor = -1
                value += 1000 * threat.index.row * factor 
        return value

    def get_column(self, i) -> list[tuple(int,int)]:
        ret = []
        for j in range(self.board):
            ret.append((i,j))
        return ret
            

    def get_primary_diagonal(self, index: Index) -> list[Index]:
        ret = []
        while index.row != -1 and index.col != -1 and index.row != HEIGHT and index.col != WIDTH:
            ret.append(index)
            index = Index(index.row + 1, index.col + 1)
        return ret

    def get_secondary_diagonal(self, index: Index) -> list[tuple(int,int)]:
        ret = []
        while index.row != -1 and index.col != -1 and index.row != HEIGHT and index.col != WIDTH:
            ret.append(index)
            index = Index(index.row + 1, index.col - 1)
        return ret




                

        # def threats_under(threat, o_threats, parity) -> bool:
        #     if threat.index.row == HEIGHT:
        #         return False
        #     for row in range(threat.index.row + 1, HEIGHT+1):
        #         for ot in o_threats:
        #             if ot.index.row < row and ot.index.col == ot.index.col and ot.index.row % 2 == parity:
        #                 return True
        #     return False

        # count_threats = lambda threats, parity: sum(1 for t in threats if t.index.row % 2 == parity)
        # x_odd_threats_wto_o_threats_under = sum(1 for t in self.x_threats if t.index.row % 2 == 1 and not threats_under(t, self.o_threats, 0))
        # o_odd_threats = count_threats(self.o_threats, 1)
        # o_even_threats = count_threats(self.o_threats, 0)

        # for xt in self.x_threats:
        #     if (
        #             xt.index.row % 2 == 1 and 
        #             not threats_under(xt, self.o_threats, 0) and
        #             {ot for ot in self.o_threats if ot.index.row % 2 == 1 and ot.index.col != xt.index.col} == set()
        #             ) or ( x_odd_threats_wto_o_threats_under > o_odd_threats and o_even_threats == 0):
        #         return 100
        # if o_even_threats > 0:
        #     return -100
        # return 0
