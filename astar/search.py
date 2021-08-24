from frontier import *
import time

# Starting state:
# 2 8 7
# 1 5 6
# 3 0 4


ITERATIONS = 1000

def h0(state: State):
    return 0

def h1(state: State):
    """ Count how many correctly placed tiles """
    delta = [state.board.end_state[i] - state.board.tiles[i] for i in state.board.tiles]
    return sum(x != 0 for x in delta)

def h2(state: State):
    """ summed manhattan distance for each tile """
    n = state.board.n
    retval = 0
    for i in state.board.tiles:
        row_i = i // n
        col_i = i % n
        row_t = state.board.tiles.index(i) // n
        col_t = state.board.tiles.index(i) % n
        retval += abs(row_i - row_t) + abs(col_i - col_t)
    return retval



def search(n, start_state = None):
    start_state = start_state or State.random_start(n)
    print(start_state.board.tiles)
    start_state.board.print_board()
    # frontier = Frontier(lambda state: len(state.solution) + h0(state))
    # frontier = Frontier(lambda state: len(state.solution) + h1(state))
    frontier = Frontier(lambda state: len(state.solution) + h2(state))
    frontier.insert(start_state)
    while not frontier.is_empty():
        state = frontier.extract()
        print("")
        state.board.print_board()
        if state != None:
            if state.is_solved():
                print("Solution: ", end="")
                state.print_solution()
                print("length of solution: " + str(len(state.solution)))
                print("States checked: " + str(frontier.total_items_pushed))
                return (len(state.solution), frontier.total_items_pushed)
            next_states = state.get_next_states()
            for next_state in next_states:
                frontier.insert(next_state)
    raise RuntimeError("No Solutions")





def search_n(n):
    print(str(n))
    avg_depth = 0
    avg_num_items_pushed = 0
    max_depth = 0
    for i in range(ITERATIONS):
        # print("Puzzle #" + str(i+1))
        # start_time = time.time()
        (a,b) = search(n)
        max_depth = max(max_depth, a)
        avg_depth += a
        avg_num_items_pushed += b
        # print("time taken: " + format(time.time() - start_time, ".4f"))
        # print("")
    print("average length of solution = " + str(avg_depth /ITERATIONS) + 
            "\navg number of states checked: " + str(avg_num_items_pushed / ITERATIONS) +
            "\nmax depth: " + str(max_depth))

search_n(3)
search_n(3)
search_n(3)
search_n(3)
search_n(3)
