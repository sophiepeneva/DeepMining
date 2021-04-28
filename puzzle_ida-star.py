from math import sqrt
import copy
import numpy as np
from collections import deque


class Puzzle:

    def __init__(self, size, board, g_score=0, move=None, parent=None):
        self.size = size
        self.n = int(sqrt(size))
        self.board = board
        self.blank_index = self.find_blank()
        self.g_score = g_score
        self.move = move
        self.distance = None
        self.parent = parent
        self.min_cost = float('inf')

    def find_blank(self):
        for i, tile in enumerate(self.board):
            if tile == 0:
                return i
        return -1

    def count_inversions(self, goal):
        inversions = 0
        for i in range(self.size - 1):
            for j in range(i + 1, self.size):
                vi = self.board[i]
                vj = self.board[j]
                if goal.index(vi) > goal.index(vj):
                    inversions += 1
        return inversions

    def is_solvable(self, goal):
        inversions = self.count_inversions(goal)

        # if the size is odd, the number of inversions should be even
        if self.size % 2 == 1 and inversions % 2 == 0:
            return True

        # if the blank is on an even row and the number of inversions is odd
        # if the blank is on an odd row and the number of inversions is even
        blank_row_idx = self.blank_index // self.n
        if (self.n - blank_row_idx) % 2 != inversions % 2:
            return True

        return False

    def manhattan_distance(self, goal):

        # 

        return sum(abs(b % self.n - g % self.n) + abs(b//self.n - g//self.n)
                   for b, g in ((self.board.index(i), goal.index(i)) for i in range(1, self.size)))

    def get_dist(self, goal):
        if self.distance is None:
            self.distance = self.manhattan_distance(goal)
        return self.distance

    def f(self, goal):
        return self.get_dist(goal) + self.g_score

    def get_move_name(self):
        if(self.move is not None):
            move_names = ['down', 'left', 'up', 'right']
            return move_names[self.move]
        return None

    def get_next_states(self):
        # row
        x = 0
        y = 0

        as_matrix = np.asarray(self.board).reshape(self.n, self.n)
        for i in range(self.n):
            for j in range(self.n):
                if as_matrix[i][j] == 0:
                    x = i
                    y = j

        # down, left, up, right
        positions = [(x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1)]
        states = [self.get_state(position, as_matrix, x, y)
                  for position in positions]
        children = [Puzzle(self.size, states[i], self.g_score + 1, i, self)
                    for i in range(4) if states[i] is not None]
        return children

    def get_state(self, position, as_matrix, x, y):
        if position[0] < 0 or position[0] >= self.n or position[1] < 0 or position[1] >= self.n:
            return None
        next_state = copy.deepcopy(as_matrix)
        temp = next_state[position[0]][position[1]]
        next_state[position[0]][position[1]] = 0
        next_state[x][y] = temp
        return next_state.reshape(1, self.size).tolist()[0]

        index = int(self.n*position[0] + position[1])
        next_state = copy.deepcopy(self.board)
        next_state[self.blank_index] = next_state[index]
        next_state[index] = 0
        return next_state

    def print_board_pretty(self):
        print(np.asarray(self.board).reshape(self.n, self.n))


class Solver:
    def __init__(self, start, size, blank_index):
        self.opened = []
        self.closed = []
        self.goal = self.get_goal(size, blank_index)
        self.start = Puzzle(size + 1, start)
        self.solution = None

    def get_goal(self, size, blank_index):
        blank_index = size if blank_index == -1 else blank_index - 1
        start = [i for i in range(1, blank_index + 1)]
        end = [i for i in range(blank_index + 1, size + 1)]
        return start + [0] + end

    def solve(self):
        # if(not self.start.is_solvable(self.goal)):
        #     print('not solvable')
        #     return
        path = self.ida_star_search(self.start)
        if path is None:
            print('could not solve')
        sol = path[0] #path that reached the solution

        moves = []
        while sol is not None:
            #print(sol.print_board_pretty())
            move = sol.get_move_name()
            if move:
                moves.insert(0, move)
            sol = sol.parent
        print(len(moves))
        print(*moves, sep="\n")

    def ida_star_search(self, board):
        threshold = board.get_dist(self.goal)
        path = deque([board])
        boards = deque()
        while path:
            min_dist = self.search(path, boards, threshold)
            if min_dist == 0:
                return path
            elif min_dist is float('inf'):
                # not solvable
                return None
            else:
                # set the new minimum number of steps
                threshold = min_dist
                print(threshold)

    def search(self, path, boards, threshold):

        node = path[0]
        f = node.f(self.goal)

        if f > threshold:
            return f

        if node.get_dist(self.goal) == 0:
            return 0

        min_cost = float('inf')
        moves = node.get_next_states()

        for idx, move in enumerate(moves):
            if move.board not in boards:
                path.appendleft(move)
                boards.appendleft(move.board)

                min_dist = self.search(path, boards, threshold)
                if min_dist == 0:
                    return 0
                min_cost = min(min_cost, min_dist)

                path.popleft()
                boards.popleft()

        return min_cost


if __name__ == "__main__":
    print('Input number of tiles:')
    n = int(input())
    print('Input position of the blank space:')
    i = int(input())
    print('Input order of tiles separated by spaces')
    vector = [int(x) for x in input().split(" ")]
    solver = Solver(vector, n, i)
    solver.solve()
