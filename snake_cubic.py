import numpy as np
import doctest

# Define the initial state of the snake cubic puzzle
def puzzle_config():
    lengths = np.array([2, 2, 2, 2, 1, 1, 1, 2, 2, 1, 1, 2, 1, 2, 1, 1, 2])
    start = [np.array([2, 0, 0])] # starting point
    all_directions = np.array([[-1, 0, 0], [1, 0, 0],
                    [0, -1, 0], [0, 1, 0],
                    [0, 0, -1], [0, 0, 1]])
    x = 3
    y = 3
    z = 3
    config = {'lengths': lengths, 
              'start': start, 
              'all_directions': all_directions, 
              'x': x, 
              'y': y, 
              'z': z}
    return config

def cubic_space_init():
    config = puzzle_config()
    x_max = config['x']
    y_max = config['y']
    z_max = config['z']
    start_init = config['start'][0]
    cubic_space = np.zeros((z_max, y_max, x_max))
    cubic_space[start_init[2], start_init[1], start_init[0]] = 1
    return cubic_space

def verify_slution(solution = [0, 3, 1, 5, 0, 4, 0, 2, 1, 5, 3, 4, 0, 5, 2, 0, 3]):
    if len(solution) != len(puzzle_config()['lengths']):
        print("Invalid solution!")
        return False
    config = puzzle_config()
    lengths = config['lengths']
    start = config['start']
    all_directions = config['all_directions']
    x_max = config['x']
    y_max = config['y']
    z_max = config['z']
    s = start[0].copy()
    cubic_space = np.zeros((z_max, y_max, x_max))
    cubic_space[s[2], s[1], s[0]] = 1
    for i in range(len(solution)):
        r, c = check_cubic(cubic_space.copy(), start[-1].copy(), all_directions[solution[i]], lengths[i])
        if r < 0:
            print("Invalid solution!")
            return False
        else:
            start.append(start[-1] + all_directions[solution[i]] * lengths[i])
            cubic_space = c
    if sum(cubic_space.flatten()) != x_max * y_max * z_max:
        return False
    else:
        return True

# check if the cubic is valid
def check_cubic(cubic_space, s, direction, length):
    config = puzzle_config()
    x_max = config['x']
    y_max = config['y']
    z_max = config['z']
    for j in range(length):
        s += direction
        if max(s) > 2 or min(s) < 0:
            return -1, cubic_space # out of range
        cubic_space[s[2], s[1], s[0]] += 1
        if cubic_space[s[2], s[1], s[0]] > 1:
            return -2, cubic_space # overlap
    if sum(cubic_space.flatten()) != x_max * y_max * z_max:
        return 0, cubic_space # not all positions are occupied
    else:
        return 1, cubic_space # all positions are occupied

# push the new move to the stack
def new_move_push_stack(stack, start, direction, cubic_space):
    stack['start'].append(start)
    stack['directions'].append(direction)
    stack['last_tried_dir'].append(-1) # -1 means no direction has been tried
    stack['cubic_space'].append(cubic_space)

# go back to the previous move(s)
def go_back_pop_stack(stack):
    stack['start'].pop()
    stack['directions'].pop()
    stack['last_tried_dir'].pop()
    stack['cubic_space'].pop()

# generate next move given the current state
def possible_moves(stack, all_directions = puzzle_config()['all_directions']):
    if len(stack['directions']) == 0 or len(stack['last_tried_dir']) == 0:
        m = [(i, d) for i, d in enumerate(all_directions) if i >= 0]
    elif stack['directions'][-1] == 0 or stack['directions'][-1] == 1:
        m = [(i, d) for i, d in enumerate(all_directions) if i > stack['last_tried_dir'][-1] and i > 1]
    elif stack['directions'][-1] == 2 or stack['directions'][-1] == 3:
        m = [(i, d) for i, d in enumerate(all_directions) if i > stack['last_tried_dir'][-1] and (i < 2 or i > 3)]
    elif stack['directions'][-1] == 4 or stack['directions'][-1] == 5:
        m = [(i, d) for i, d in enumerate(all_directions) if i > stack['last_tried_dir'][-1] and i < 4]
    pass

    return m

def solve_puzzle():
    config = puzzle_config()
    lengths = config['lengths']
    cubic_space = [] # 0 means empty, 1 means occupied
    cubic_space.append(cubic_space_init().copy())
    stack = {'start': config['start'].copy(), 
             'directions': [],
             'last_tried_dir': [-1],
             'cubic_space': cubic_space}
    trial_count = 0
    while True:
        m = possible_moves(stack)
        for i, d in m:
            trial_count += 1
            r, c = check_cubic(cubic_space[-1].copy(), stack['start'][-1].copy(), d, lengths[len(stack['directions'])])
            print("Trying [", trial_count, "trials ]: ", stack['directions'], "->", i)
            stack['last_tried_dir'][-1] = i
            if r >= 0: # Found a valid one-step direction, push to the stack
                new_move_push_stack(stack, stack['start'][-1] + d * lengths[len(stack['directions'])], i, c)
                if r == 1:
                    print("*** Solved [", trial_count, "trials ]: ", stack['directions'])
                    return stack['directions']
                break
                        
        while len(possible_moves(stack)) == 0:
            go_back_pop_stack(stack) # continue to go back until there is a possible move
        
        if len(stack['directions']) == 0:
            print("No solution!")
            return -1

if __name__ == "__main__":
    print(doctest.testmod())
    sol = solve_puzzle()
    print("solution is ", verify_slution(sol))
else:
    print("snake_cubic.py is imported")
    