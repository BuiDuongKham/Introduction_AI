import numpy as np

def check_array_presence(arr, list_of_arrays):
    for array in list_of_arrays:
        if (array == arr).all():
            return True
    return False

def manhattan_distance(state, desired_state):
    distance = 0
    for i in range(state.shape[0]):
        for j in range(state.shape[1]):
            if state[i,j] != 0:
                x, y = np.where(desired_state == state[i,j])
                distance += abs(x[0] - i) + abs(y[0] - j)
    return distance

def get_possible_moves(state,desired_state, x, y, current_depth):
    possible_moves = []
    if x > 0:
        clone_state = state.copy()
        temp = clone_state[x-1, y]
        clone_state[x-1, y] = clone_state[x, y]
        clone_state[x, y] = temp
        possible_moves.append({'state': clone_state, 'pos': (x-1, y), 'parent': state, 'depth': current_depth+1,'score': manhattan_distance(clone_state, desired_state)})

    if x < state.shape[0]-1:
        clone_state = state.copy()
        temp = clone_state[x+1, y]
        clone_state[x+1, y] = clone_state[x, y]
        clone_state[x, y] = temp
        possible_moves.append({'state': clone_state, 'pos': (x+1, y), 'parent': state, 'depth': current_depth+1,
                               'score': manhattan_distance(clone_state, desired_state)})

    if y > 0:
        clone_state = state.copy()
        temp = clone_state[x, y-1]
        clone_state[x, y-1] = clone_state[x, y]
        clone_state[x, y] = temp
        possible_moves.append({'state': clone_state, 'pos': (x, y-1), 'parent': state, 'depth': current_depth+1, 'score': manhattan_distance(clone_state, desired_state)})

    if y < state.shape[1]-1:
        clone_state = state.copy()
        temp = clone_state[x, y+1]
        clone_state[x, y+1] = clone_state[x, y]
        clone_state[x, y] = temp
        possible_moves.append({'state': clone_state, 'pos': (x, y+1), 'parent': state, 'depth': current_depth+1, 'score': manhattan_distance(clone_state, desired_state)})

    return possible_moves