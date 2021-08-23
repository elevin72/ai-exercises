from frontier import *
import time

# Starting state:
# 2 8 7
# 1 5 6
# 3 0 4


ITERATIONS = 100

def search(n, start_state = None):
    start_state = start_state or State.random_start(n)
    # print(start_state.board.tiles)
    start_state.board.print_board()
    frontier = Frontier(start_state)
    while not frontier.is_empty():
        state = frontier.extract()
        if state != None:
            if state.is_solved():
                print("Solution: ", end="")
                state.print_solution()
                print("length of solution: " + str(len(state.solution)))
                print("states checked: " + str(frontier.total_items_pushed))
                return (len(state.solution), frontier.total_items_pushed)
            next_states = state.get_next_states()
            for next_state in next_states:
                frontier.insert(next_state)
    raise RuntimeError("No Solutions")





def search_n(n):
    avg_depth = 0
    avg_num_items_pushed = 0
    max_depth = 0
    for i in range(ITERATIONS):
        print("Puzzle #" + str(i+1))
        start_time = time.time()
        (a,b) = search(n)
        max_depth = max(max_depth, a)
        avg_depth += a
        avg_num_items_pushed += b
        print("time taken: " + format(time.time() - start_time, ".4f"))
        print("")
    print("average length of solution = " + str(avg_depth /ITERATIONS) + 
            "\navg number of states checked: " + str(avg_num_items_pushed / ITERATIONS) +
            "\nmax depth: " + str(max_depth))

# search(3, State(Board(3, [8,6,7,2,5,4,3,0,1], 7), []) )
n = 3
tiles = [7,6,4,5,2,8,1,3,0]
search(n, State(Board(n, tiles), []))
# search_n(3)
# search(3)
# search_n(3)

