from abminimax import *


# b = Board(
#        [' OXX OO',
#         'OXXO XX',
#         'XXOX OX',
#         'OXOO OO',
#         'XOXO XO',
#         'XOOOXXX'],
#         'X')

# b = Board(
#        ['XOXX OO',
#         'OXXO XX',
#         'XXOX OX',
#         'OXOO OO',
#         'XOXOOXO',
#         'XOOOXXX'],
#b = Board(
#       ['       ',
#        '       ',
#        '       ',
#        '       ',
#        '       ',
#        '       '],
#        'X')

b = Board(
       ['  XX   ',
        '  OO   ',
        ' XOO   ',
        ' OOX   ',
        ' XXO   ',
        ' XOXXXO'],
        'O')

b.evaluate()

a = ab_minimax(b, 2, -math.inf, math.inf, b.turn == 'X')[1]
b.evaluate()

c = Board(
        ['       ',
         '   X   ',
         '   OO  ',
         '  OOX  ',
         '  XXO  ',
         ' XXOXO '],
        'O')


# for _ in range(100):
#     d = ab_minimax(b, 2, -math.inf, math.inf, True)[1]
#     d.print()
