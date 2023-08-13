import itertools
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

def verify_slution(solution = [0, 3, 1, 5, 0, 4, 0, 2, 1, 5, 3, 4, 0, 5, 2, 0, 3]):
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
        # print("before i=", i, ",", sum(cubic_space.flatten()), ", d=", solution[i], "s=", start[-1])
        r, c = check_cubic(cubic_space.copy(), start[-1].copy(), all_directions[solution[i]], lengths[i])
        if r < 0:
            print("Invalid solution!")
            return False
        else:
            start.append(start[-1] + all_directions[solution[i]] * lengths[i])
            cubic_space = c
            # print("i=", i, ",", sum(cubic_space.flatten()), ": ", solution[:i+1], "r=", r, "s=", start[-1])
    if sum(cubic_space.flatten()) != x_max * y_max * z_max:
        return False
    else:
        return True

# check if the cubic is valid
def check_cubic(cubic_space, s, direction, length):
    s_init = s.copy()
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
        return 0, cubic_space # not all cubes are occupied
    else:
        return 1, cubic_space

# new move
def new_move_push_stack(stack, s, i, c):
    stack['start'].append(s)
    stack['directions'].append(i)
    stack['cubic_space'].append(c)

# go back to the previous move
def go_back_pop_stack(stack):
    stack['start'].pop()
    dir_prev = stack['directions'].pop()
    stack['cubic_space'].pop()
    m = possible_moves(stack, 0)
    while len(stack['directions']) > 0 and dir_prev == m[-1][0]:
        stack['start'].pop()
        dir_prev = stack['directions'].pop()
        stack['cubic_space'].pop()
    return dir_prev

# generate next move
def possible_moves(stack, start_index, all_directions = puzzle_config()['all_directions']):
    if len(stack['directions']) == 0:
        m = [(i, d) for i, d in enumerate(all_directions) if i >= start_index]
    elif stack['directions'][-1] == 0 or stack['directions'][-1] == 1:
        m = [(i, d) for i, d in enumerate(all_directions) if i >= start_index and i > 1]
    elif stack['directions'][-1] == 2 or stack['directions'][-1] == 3:
        m = [(i, d) for i, d in enumerate(all_directions) if i >= start_index and (i < 2 or i > 3)]
    elif stack['directions'][-1] == 4 or stack['directions'][-1] == 5:
        m = [(i, d) for i, d in enumerate(all_directions) if i >= start_index and i < 4]
    pass

    return m

def solve_puzzle():
    config = puzzle_config()
    lengths = config['lengths']
    all_directions = config['all_directions']
    x_max = config['x']
    y_max = config['y']
    z_max = config['z']
    solved_flag = False
    pop_flag = False
    new_trial_flag = True
    cubic_space = [np.zeros((z_max, y_max, x_max))] # 0 means empty, 1 means occupied
    cubic_space[0][0, 0, 2] = 1
    stack = {'start': config['start'].copy(), 'directions': [], 'cubic_space': cubic_space}
    loop_count = 0
    while solved_flag == False:
        loop_count += 1
        # print("loop_count=", loop_count, ", stack['directions']=", stack['directions'])
        if len(stack['directions']) == 0 or new_trial_flag == True:
            start_index = 0
            new_trial_flag = False
        else:
            start_index = dir_prev + 1
            
        m = possible_moves(stack, start_index)
        for i, d in m:
            r, c = check_cubic(cubic_space[-1].copy(), stack['start'][-1].copy(), d, lengths[len(stack['directions'])])
            
            if r >= 0: # Found a valid one-step direction, push to the stack
                new_move_push_stack(stack, stack['start'][-1] + d * lengths[len(stack['directions'])], i, c)
                new_trial_flag = True
                if r == 1:
                    solved_flag = True
                break

            if i == m[-1][0]: # No valid direction, pop the stack
                pop_flag = True
        
        if pop_flag:
            pop_flag = False
            dir_prev = go_back_pop_stack(stack)
            if len(stack['directions']) == 0:
                print("No solution!")
                return -1

    print("*** Solved: ", stack['directions'])
    return stack['directions']

# Run doctests
if __name__ == "__main__":
    print(doctest.testmod())
    sol = solve_puzzle()
    print("solution is ", verify_slution(sol))
else:
    print("snake_cubic.py is imported")
    