import numpy as np
import datetime
from ds import Stack, Queue, PriorityQueue
from ultis import check_array_presence, manhattan_distance, get_possible_moves
class Puzzle:
    print(np.__version__)
    def __init__(self, initial_state, desired_state, iterations=1000):

        # find the position of number 0 in initial state
        self.time = None
        x, y = np.where(initial_state == 0)

        self.x1 = x[0]
        self.y1 = y[0]
        self.initial_state = initial_state
        self.desired_state = desired_state
        self.visited_states = []
        self.visited_states.append(
            {
                'state': initial_state,
                'pos': (self.x1, self.y1),
                'parent': None,
                'depth': 0,
                'score': manhattan_distance(initial_state, desired_state)
            }
        )
        self.found = False
        self.maximum_iterations = iterations


    def dfs(self):
        count = 0
        time_start = datetime.datetime.now()
        self.dfs_storage = Stack()
        self.dfs_storage.push(
            {
                'state': self.initial_state,
                'pos': (self.x1, self.y1),
                'parent': None,
                'depth': 0,
                'score': manhattan_distance(self.initial_state, self.desired_state)
            }
        )

        # clear visited state first
        self.found = False
        self.visited_states = []
        self.visited_states.append(
            {
                'state': self.initial_state,
                'pos': (self.x1, self.y1),
                'parent': None,
                'depth': 0,
                'score': manhattan_distance(self.initial_state, self.desired_state)
            }
        )


        while self.dfs_storage.getSize() > 0 and count < self.maximum_iterations:
            count += 1
            current_state = self.dfs_storage.pop()

            if (current_state['state'] == self.desired_state).all():
                self.found = True
                time_end = datetime.datetime.now()
                self.time = time_end - time_start
                print('found in ', time_end - time_start, ' seconds')
                return
            possible_moves = get_possible_moves(current_state['state'], self.desired_state, current_state['pos'][0], current_state['pos'][1], current_depth= current_state['depth'])


            for move in possible_moves:

                if (move['state'] == self.desired_state).all():
                    self.visited_states.append(move)
                    self.found = True
                    print('found')
                    time_end = datetime.datetime.now()
                    self.time = time_end - time_start
                    print('found in ', time_end - time_start, ' seconds')
                    return

                if  not check_array_presence(move['state'], list(map(lambda x: x['state'], self.visited_states ))) and not self.found:
                    self.dfs_storage.push(move)
                    self.visited_states.append(move)

        time_end = datetime.datetime.now()
        self.time = (time_end - time_start)
        print('not found after ', time_end - time_start, ' seconds')

    def bfs(self):
        count = 0
        time_start = datetime.datetime.now()
        self.bfs_storage = Queue()
        self.bfs_storage.enqueue(
            {
                'state': self.initial_state,
                'pos': (self.x1, self.y1),
                'parent': None,
                'depth': 0
            }
        )

        # clear visited state first
        self.found = False
        self.visited_states = []
        self.visited_states.append(
            {
                'state': self.initial_state,
                'pos': (self.x1, self.y1),
                'parent': None,
                'depth': 0
            }
        )
        while self.bfs_storage.getSize() > 0 and count < self.maximum_iterations:
            count += 1
            current_state = self.bfs_storage.dequeue()

            if (current_state['state'] == self.desired_state).all():
                self.found = True
                time_end = datetime.datetime.now()
                self.time = time_end - time_start
                print('found in ', time_end - time_start, ' seconds')
                return
            possible_moves = get_possible_moves(current_state['state'], self.desired_state, current_state['pos'][0], current_state['pos'][1], current_depth= current_state['depth'])

            for move in possible_moves:

                if (move['state'] == self.desired_state).all():
                    self.visited_states.append(move)
                    self.found = True
                    time_end = datetime.datetime.now()
                    self.time = time_end - time_start
                    print('found in ', time_end - time_start, ' seconds')
                    return

                if not check_array_presence(move['state'], list(map(lambda x: x['state'], self.visited_states ))) and not self.found:
                    self.bfs_storage.enqueue(move)
                    self.visited_states.append(move)

        time_end = datetime.datetime.now()
        self.time = time_end - time_start
        print('not found after ', time_end - time_start, ' seconds')

    def dfs_with_limited_depth(self, depth):
        count = 0
        time_start = datetime.datetime.now()
        self.dfs_storage = Stack()
        self.dfs_storage.push(
            {
                'state': self.initial_state,
                'pos': (self.x1, self.y1),
                'parent': None,
                'depth': 0,
                'score': manhattan_distance(self.initial_state, self.desired_state)
            }
        )

        # clear visited state first
        self.found = False
        self.visited_states = []
        self.visited_states.append(
            {
                'state': self.initial_state,
                'pos': (self.x1, self.y1),
                'parent': None,
                'depth': 0,
                'score': manhattan_distance(self.initial_state, self.desired_state)
            }
        )

        while self.dfs_storage.size >0 and count < self.maximum_iterations:
            count += 1
            current_state = self.dfs_storage.pop()

            if (current_state['state'] == self.desired_state).all():
                self.found = True
                time_end = datetime.datetime.now()
                self.time = time_end - time_start
                print('found in ', time_end - time_start, ' seconds')
                return
            possible_moves = get_possible_moves(current_state['state'], self.desired_state, current_state['pos'][0], current_state['pos'][1], current_depth= current_state['depth'])

            for move in possible_moves:

                if (move['state'] == self.desired_state).all():
                    self.visited_states.append(move)
                    self.found = True
                    time_end = datetime.datetime.now()
                    self.time = time_end - time_start
                    print('found in ', time_end - time_start, ' seconds')
                    return

                if not check_array_presence(move['state'], list(map(lambda x: x['state'], self.visited_states ))) and not self.found and move['depth'] < depth:
                    self.dfs_storage.push(move)
                    self.visited_states.append(move)

        time_end = datetime.datetime.now()
        self.time = time_end - time_start
        print('not found after ', time_end - time_start, ' seconds')

    def heuristic1(self):
        count = 0
        time_start = datetime.datetime.now()
        self.heuristic1_storage = PriorityQueue()
        self.heuristic1_storage.insert(
            {
                'state': self.initial_state,
                'pos': (self.x1, self.y1),
                'parent': None,
                'depth': 0,
                'score': manhattan_distance(self.initial_state, self.desired_state)
            }
        )

        # clear visited state first
        self.found = False
        self.visited_states = []
        self.visited_states.append(
            {
                'state': self.initial_state,
                'pos': (self.x1, self.y1),
                'parent': None,
                'depth': 0,
                'score': manhattan_distance(self.initial_state, self.desired_state)
            }
        )

        while not self.heuristic1_storage.isEmpty() and count < self.maximum_iterations:
            count += 1
            current_state = self.heuristic1_storage.dequeue()

            if (current_state['state'] == self.desired_state).all():
                self.found = True
                time_end = datetime.datetime.now()
                self.time = time_end - time_start
                print('found in ', time_end - time_start, ' seconds')
                return
            possible_moves = get_possible_moves(current_state['state'], self.desired_state, current_state['pos'][0], current_state['pos'][1], current_depth= current_state['depth'])

            for move in possible_moves:

                if (move['state'] == self.desired_state).all():
                    self.visited_states.append(move)
                    self.found = True
                    time_end = datetime.datetime.now()
                    self.time = time_end - time_start
                    print('found in ', time_end - time_start, ' seconds')
                    return

                if not check_array_presence(move['state'], list(map(lambda x: x['state'], self.visited_states ))) and not self.found:
                    self.heuristic1_storage.insert(move)
                    self.visited_states.append(move)
        time_end = datetime.datetime.now()
        self.time = time_end - time_start
        print('not found after ', self.time, ' seconds')

    def retrieve(self):

        self.path = None

        if self.found:
            path = []
            current_state = self.visited_states[-1]
            while current_state['parent'] is not None:
                path.append(current_state)
                for state in self.visited_states:
                    if (state['state'] == current_state['parent']).all():
                        current_state = state
                        break
            path.append(current_state)
            self.path = path[::-1]
        else:
            return
