import random
import copy

""" Moves """
""" Note that sum of opposite moves is 5 """
UP = 1
LEFT = 2
RIGHT = 3
DOWN = 4

class Board:
    
    def __init__(self, n, tiles = None):
        self.n = n
        self.tiles = tiles or self._finished_tiles(n)
        self.empty_tile = self.tiles.index(0)
        self.end_state = self._finished_tiles(n)

    @staticmethod
    def _finished_tiles(n):
        return list(range(n*n))

    def copy(self):
        return copy.deepcopy(self)

    def randomize(self):
        for _ in range(self.n**3):
            self = self.do_random_move()
        return self


    def move_is_legal(self, move):
        if move == UP:
            return self.empty_tile >= self.n
        elif move == DOWN:
            return self.empty_tile < self.n**2 - self.n
        elif move == LEFT:
            return self.empty_tile % self.n != 0
        elif move == RIGHT: 
            return self.empty_tile % self.n != self.n - 1
        
    def do_move(self, move):
        if not self.move_is_legal(move):
            raise RuntimeError("The empty tile cannot be moved in the given direction.")
        new_empty_tile = self.empty_tile
        if move == UP:
            new_empty_tile -= self.n
        elif move == DOWN:
            new_empty_tile += self.n
        elif move == LEFT:
            new_empty_tile -= 1
        elif move == RIGHT:
            new_empty_tile += 1

        tiles = self.tiles.copy()
        tiles[self.empty_tile] = self.tiles[new_empty_tile]
        tiles[new_empty_tile] = 0
        return Board(self.n, tiles)

    def do_random_move(self):
        moves = [1, 2, 3, 4]
        random.shuffle(moves)
        for move in moves:
            if self.move_is_legal(move):
                return self.do_move(move)
        raise RuntimeError("The empty tile cannot be moved in any direction.")

    def is_solved(self):
        return self.tiles == self.end_state


    def print_board(self):
        for i in range(self.n):
            for j in range(self.n):
                print(self.tiles[self.n * i + j], end=" ")
            print("")




            
