'''
The state is a list of 2 items: the board, the path
The target for 8-puzzle is: (zero is the hole)
012
345
678
'''

from board import *

class State:
    def __init__(self, board, solution):
        self.board = board
        self.solution = solution

    @staticmethod
    def random_start(n):
        return State(Board(n).randomize(), [])

    def get_next_states(self):
        next_states = []
        solution_is_empty = self.solution == []
        # move_is_backwards = self.solution[-1] + move == 5
        for move in range(1,5):    # 1 - 4
            if (self.board.move_is_legal(move) and (solution_is_empty or self.solution[-1] + move != 5)):     # see note at top of board.py
                next_states.append(State(self.board.do_move(move), self.solution + [move]))
        return next_states

    def solution_len(self):
        return len(self.solution)

    def is_solved(self):
        return self.board.is_solved()

    def print_solution(self):
        str = ""
        for move in self.solution:
            if move == 1:
                str += " "
            elif move == 2:
                str += " "
            elif move == 3:
                str += " "
            elif move == 4:
                str += " "
        print(str)

