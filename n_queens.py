import random
import numpy as np
import time


class NQueens:
    def __init__(self, n):
        self.start_time = time.time()
        self.n = n

    def generate_board(self):
        self.board = np.zeros([n, n], dtype=int)
        self.queens = []
        i = 0
        self.queens_pos = np.zeros(n+1)
        self.f_row = np.zeros(n + 1)
        self.f_mdiag = np.zeros(2*n + 1)
        self.f_sdiag = np.zeros(2*n + 1)
        # for i in range(n):
        #     col = i + 1
        #     j = random.randint(0, n-1)
        #     self.board[i][j] = 1
        #     self.queens.append((i, j))

        for i in range(1, n + 1):
            j = random.randint(1, n)
            self.queens_pos[i] = j
            self.f_row[j] += 1
            self.f_mdiag[j + i] += 1
            self.f_sdiag[self.n - j + 1 + i] += 1
        self.conflicts = self.get_all_conflicts()

    def get_all_conflicts(self):
        conflicts = 0
        for i in range(1, self.n * 2):
            x = self.f_row[i] if i <= self.n else 0
            y = self.f_mdiag[i]
            z = self.f_sdiag[i]
            conflicts += (x * (x-1) // 2)
            conflicts += (y * (y-1) // 2)
            conflicts += (z * (z-1) // 2)
        return int(conflicts)

    
    def get_queen_conflicts(self, row, col, freq):
        return int(freq[row] * (freq[row] - 1) // 2)

    def get_all_queen_conflicts(self, row, col):
        return int(self.f_row[row] * (self.f_row[row] - 1) // 2) + \
            int(self.f_mdiag[row + col] * (self.f_mdiag[row + col] - 1) // 2) + \
            int(self.f_sdiag[self.n + col + 1 - row] * (self.f_sdiag[self.n + col + 1 - row] - 1) // 2)


    def has_conflicts(self):
        return self.conflicts > 0

    def solve2(self):
        self.generate_board()
        no_changes_counter = 0
        while(self.has_conflicts()):
            min_attacks = self.n + 1
            col = random.randint(1, n)
            row = int(self.queens_pos[col])
            best_position = (0, 0)
            pos = (row, col)
            for i in range(1, self.n + 1):
                new_pos = (i, col)
                self.move(pos, new_pos)
                conflicts = self.get_all_queen_conflicts(i, col)
                if(conflicts < min_attacks):
                    best_position = new_pos
                    min_attacks = conflicts
                self.move(new_pos, pos)
            self.move(pos, best_position)  
        print("--- %s seconds ---" % (time.time() - self.start_time))
        print(self.queens_pos)

    def move(self, pos, new_pos):
        self.queens_pos[pos[1]] = new_pos[0]
        self.conflicts -= self.get_all_queen_conflicts(pos[0], pos[1])
        self.f_row[pos[0]] -= 1
        self.f_row[new_pos[0]] += 1
        self.f_mdiag[pos[0] + pos[1]] -= 1
        self.f_mdiag[new_pos[0] + new_pos[1]] += 1
        self.f_sdiag[self.n + new_pos[1] + 1 - new_pos[0]] += 1
        self.f_sdiag[self.n + pos[1] + 1 - pos[0]] -= 1
        self.conflicts += self.get_all_queen_conflicts(new_pos[0], new_pos[1])
        

    def solve(self):
        self.generate_board()
        no_changes_counter = 0
        while(not self.all_queens_safe()):
            min_attacks = self.n + 1
            picked = self.get_random_queen()
            best_position = (-1, -1)

            for i in range(self.n):
                new_pos = (picked[0], i)
                self.move_queen(picked, new_pos)
                conflicts = self.count_coflicts_for_queen(new_pos)
                if(conflicts < min_attacks):
                    best_position = new_pos
                    min_attacks = conflicts
                self.move_queen(new_pos, picked)
            if(picked == best_position):
                no_changes_counter += 1
            else:
                no_changes_counter = 0
            self.move_queen(picked, best_position)
            if(no_changes_counter > self.n):
                # force move queen
                j = random.randint(0, n-1)
                self.move_queen(picked, (picked[0], j))
                no_changes_counter = 0

    def count_coflicts_for_queen(self, current):
        assert current in self.queens  # checks to make sure given position is a queen
        conflicts = 0
        for queen in self.queens:
            if self.can_be_hit(current, queen):
                conflicts += 1
            if conflicts == 3:
                return 3
        return conflicts

    def move_queen(self, from_pos, to_pos):
        self.board[from_pos[0]][from_pos[1]] = 0
        self.board[to_pos[0]][to_pos[1]] = 1
        self.queens.remove(from_pos)
        self.queens.append(to_pos)

    def get_random_queen(self):
        index = random.randint(0, n - 1)
        return self.queens[index]

    def all_queens_safe(self):
        for queen in self.queens:
            if self.is_under_attack(queen):
                return False
        return True

    def is_under_attack(self, current):
        for queen in self.queens:
            if self.can_be_hit(current, queen):
                return True
        return False

    def can_be_hit(self, queen, enemy):
        if queen != enemy:
            # by col
            if(enemy[1] == queen[1]):
                return True
            # by row
            if(enemy[0] == queen[0]):
                return True
            # by diagonal
            if (abs(queen[0] - enemy[0]) == abs(enemy[1] - queen[1])):
                return True
        return False

    def row_attack(self, queen, enemy):
        return queen[0] == enemy[0]

    def num_to_tile(self, num):
        return '_' if num == 0 else '*'

    def print_board(self):
        for row in self.board:
            print(" ".join(self.num_to_tile(tile) for tile in row))


if __name__ == "__main__":
    print('Input number of queens:')
    n = int(input())
    nQueens = NQueens(n)
    nQueens.solve2()
    # nQueens.print_board()
