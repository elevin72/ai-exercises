from board import *

def ab_minimax(board: Board, depth: int, alpha: int, beta: int, MAX: bool):
    if depth == 0 or abs(board.value) == math.inf:
        return board.value,board
    next_states = board.get_next_states()
    best_state = None
    if MAX:
        value = -math.inf
        for next_state in next_states:
            minimax = ab_minimax(next_state, depth - 1, alpha, beta, False)[0]
            if minimax > value:
                value = minimax
                best_state = next_state
            if value >= beta:
                break # beta cutoff
            alpha = max(alpha, value)
    else:
        value = math.inf
        for next_state in next_states:
            minimax = ab_minimax(next_state, depth - 1, alpha, beta, True)[0]
            if minimax < value:
                value = minimax
                best_state = next_state
            if value <= alpha: # alpha cutoff
                break # beta cutoff
            beta = max(beta, value)
    return value,best_state


