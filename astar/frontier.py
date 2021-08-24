'''
# יוצר מחסנית ״משוכללת״
[stack, max. depth, init. state, try next level?]
stack - a simple stack as defined at stack.py
max.depth - the current search depth of ID
init.state - the initial state of the problem
try next level - is there a reason to search deeper
'''

from state import *
from pqueue import *
from typing import Optional

class Frontier:
    def __init__(self, heuristic):
        self.queue = Pqueue(heuristic)
        self.total_items_pushed = 0

    def is_empty(self):
        return self.queue.is_empty()

    def insert(self, state: State):
        self.queue.push(state)
        self.total_items_pushed += 1

    def extract(self) -> Optional[State]:
        if self.queue.is_empty():
            return None
        print("\nPriority = ", end="")
        print(str(self.queue.priority(self.queue.heap[0])))
        return self.queue.pop()



    
