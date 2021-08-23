'''
# יוצר מחסנית ״משוכללת״
[stack, max. depth, init. state, try next level?]
stack - a simple stack as defined at stack.py
max.depth - the current search depth of ID
init.state - the initial state of the problem
try next level - is there a reason to search deeper
'''

from stack import *
from state import *
from typing import Optional


class Frontier:
    def __init__(self, start_state: State):
        self.stack = Stack()
        self.stack.push(start_state)
        self.depth = 1
        self.start_state = start_state
        self.go_deeper = False # 8==D
        self.total_items_pushed = 0

    def is_empty(self):
        return self.stack.is_empty() and not self.go_deeper

    def insert(self, state: State):
        if state.solution_len() <= self.depth:
            self.stack.push(state)
            # self.start_state = self.start_state or state
            self.total_items_pushed += 1
        else:
            self.go_deeper = True

    def extract(self) -> State:
        if self.stack.is_empty():   # check is there are no states in the stack
            if self.go_deeper:          # check if there is a reason to search deeper
                self.depth += 1             # increase search depth
                self.go_deeper = False      # meanwhile there is no evidence to  a need to search deeper
                return self.start_state     # return the initial state
        return self.stack.pop()   # if there are items in the stack ...



    
