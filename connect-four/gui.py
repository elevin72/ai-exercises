import pygame as pg
import sys
from board import *
from abminimax import *
import time
from client import Client

BLACK = (0,0,0)
GREY = (152, 158, 158)
WHITE = (200, 200, 200)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GRID_HEIGHT = 300
GRID_WIDTH = 350
WINDOW_HEIGHT = 400
WINDOW_WIDTH = 400
DEPTH=4

def main():
    global SCREEN, CLOCK
    pg.init()
    SCREEN = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    CLOCK = pg.time.Clock()
    SCREEN.fill(GREY)
    b = Board()
    human,ai = get_player()
    client = get_client()
    p = False

    while True:
        if b.end_state != EndState.NOT_DONE:
            b.print()
            print("game over")
            game_over(b)
            time.sleep(7)
            exit()
        if b.turn != human:
            if not p:
                b.print()
                p = True
            a,b = ab_minimax(b, DEPTH, -math.inf, math.inf, ai == 'X')
            print('Minimax value:', a)
            print('Heuristic Value:', b.evaluate())
            # time.sleep(1)
        else:
            b = client.play(b)

            
        # for event in pg.event.get():
        #     if event.type == pg.QUIT:
        #         pg.quit()
        #         sys.exit()
        #     if event.type == pg.MOUSEBUTTONDOWN:
        #         pos = pg.mouse.get_pos()
        #         if (pos[1] > 0 and pos[1] < WINDOW_HEIGHT and
        #                 pos[0] > 0 and pos[0] < WINDOW_WIDTH and
        #                 b.turn == human):
        #             move = ( pos[0] - 25 ) // 50
        #             print('move:', move)
        #             if b.is_legal_move(move):
        #                 if p:
        #                     b.print()
        #                     p = False
        #                 b = b.play(move)
        #                 print('Heuristic Value:', b.evaluate())
        drawGrid()
        drawCircles(b)
        pg.display.update()

def drawGrid():
    blockSize = 50 #Set the size of the grid block
    for x in range(25, GRID_WIDTH, blockSize):
        for y in range(25, GRID_HEIGHT, blockSize):
            rect = pg.Rect(x, y, blockSize, blockSize)
            pg.draw.rect(SCREEN, BLACK, rect, 1)


def drawCircles(b):
    for i,row in enumerate(b.board):
        for j,space in enumerate(row):
            if space == 'X':
                pg.draw.circle(SCREEN, RED, ((j+1)*50, (i+1)*50), 20)
            if space == 'O':
                pg.draw.circle(SCREEN, YELLOW, ((j+1)*50, (i+1)*50), 20)



def get_client():
    client = Client("10.7.11.153")
    client.connect(("10.7.11.27", 6969))
    return client

def get_player():
    r = pg.Rect(0, 0, WINDOW_WIDTH/2, WINDOW_HEIGHT)
    y = pg.Rect(WINDOW_WIDTH/2, 0, WINDOW_WIDTH/2, WINDOW_HEIGHT)
    pg.draw.rect(SCREEN, RED, r)
    pg.draw.rect(SCREEN, YELLOW, y)
    pg.display.update()
    user = None
    while user == None:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                pos = pg.mouse.get_pos()
                if (pos[0] > 0 and pos[0] < WINDOW_WIDTH/2 and
                    pos[1] > 0 and pos[1] < WINDOW_HEIGHT
                    ):
                    user = 'X'
                    ai = 'O'
                elif (pos[0] > WINDOW_WIDTH/2 and pos[0] < WINDOW_WIDTH and
                    pos[1] > 0 and pos[1] < WINDOW_HEIGHT
                    ):
                    user = 'O'
                    ai = 'X'
    SCREEN.fill(GREY)
    pg.display.update()
    return user,ai


def game_over(board: Board):
    if board.end_state == EndState.X_WIN:
        print("X/Red Won!")
    if board.end_state == EndState.O_WIN:
        print("O/Yellow Won!")
    if board.end_state == EndState.TIE:
        print("Its a tie!")



main()
