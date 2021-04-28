import numpy as np


class TicTacToe:
    def __init__(self, player_marker):
        self.initialize_game()
        self.player_turn = 'X'
        self.person_marker = player_marker
        self.ai_marker = self.get_oponent_marker(player_marker)

        self.winner_to_message = {
            self.person_marker: 'You win!',
            self.ai_marker: 'You lost!',
            '.': 'Its a tie.'
        }

    def get_score(self, winner):
        if winner == '.':
            return 0
        if winner == self.person_marker:
            return -1 - np.count_nonzero(self.current_state == '.')
        return 1 + np.count_nonzero(self.current_state == '.')

    def get_oponent_marker(self, marker):
        return 'X' if marker == 'O' else 'O'

    def initialize_game(self):
        self.current_state = np.zeros((3, 3), 'U1')
        self.current_state.fill('.')

    def draw_board(self):
        for i in range(0, 3):
            for j in range(0, 3):
                print('{}'.format(self.current_state[i][j]), end=" ")
            print()
        print()

    def is_valid(self, x, y):
        if x < 0 or x > 2 or y < 0 or y > 2:
            return False
        return self.current_state[x][y] == '.'

    def get_winner(self):
        # Vertical win
        for i in range(3):
            column = self.current_state[:, i]
            if column[0] != '.' and np.all(column == column[0]):
                return column[0]

        # Horizontal win
        for i in range(0, 3):
            if self.current_state[i][0] != '.' and np.all(self.current_state[i] == self.current_state[i][0]):
                return self.current_state[i][0]

        # Main diagonal win
        main_diag = self.current_state.diagonal()
        if main_diag[0] != '.' and np.all(main_diag == main_diag[0]):
            return main_diag[0]

        # Secondary diagonal win
        sec_diag = np.fliplr(self.current_state).diagonal()
        if sec_diag[0] != '.' and np.all(sec_diag == sec_diag[0]):
            return sec_diag[0]

        if '.' in self.current_state:
            return None

        # a tie
        return '.'

    def max_alpha_beta(self, alpha, beta, marker):
        maxv = float('-inf')
        move = (None, None)

        winner = self.get_winner()

        if winner is not None:
            return self.get_score(winner), move

        for i in range(3):
            for j in range(3):
                if self.current_state[i][j] == '.':
                    self.current_state[i][j] = marker

                    m, _ = self.min_alpha_beta(
                        alpha, beta, self.get_oponent_marker(marker))
                    if m > maxv:
                        maxv = m
                        move = (i, j)
                    self.current_state[i][j] = '.'

                    if maxv >= beta:
                        return maxv, move
                    alpha = max(alpha, maxv)

        return maxv, move

    def min_alpha_beta(self, alpha, beta, marker):

        minv = float('inf')
        move = (None, None)
        winner = self.get_winner()

        if winner is not None:
            return self.get_score(winner), move

        for i in range(3):
            for j in range(3):
                if self.current_state[i][j] == '.':
                    self.current_state[i][j] = marker
                    m, _ = self.max_alpha_beta(
                        alpha, beta, self.get_oponent_marker(marker))
                    if m < minv:
                        minv = m
                        move = (i, j)
                    self.current_state[i][j] = '.'

                    if minv <= alpha:
                        return minv, move

                    beta = min(beta, minv)

        return minv, move

    def change_player_turn(self):
        self.player_turn = self.get_oponent_marker(self.player_turn)

    def play_alpha_beta(self):
        while True:
            self.draw_board()
            winner = self.get_winner()

            if winner is not None:
                print(self.winner_to_message[winner])
                return

            if self.player_turn == self.person_marker:

                while True:
                    m, (x, y) = self.min_alpha_beta(
                        float('-inf'), float('inf'), self.person_marker)
                    print('Recommended move: X = {}, Y = {}'.format(x + 1, y + 1))

                    x = int(input('Enter X: ')) - 1
                    y = int(input('Enter Y: ')) - 1

                    if self.is_valid(x, y):
                        self.current_state[x][y] = self.person_marker
                        self.change_player_turn()
                        break
                    else:
                        print('Cannot play there. Insert coordinates again.')

            else:
                m, (x, y) = self.max_alpha_beta(
                    float('-inf'), float('inf'), self.ai_marker)
                self.current_state[x][y] = self.ai_marker
                self.change_player_turn()


if __name__ == "__main__":

    print('Pick X or O (X goes first) :')
    while True:
        marker = input()
        if marker != 'X' and marker != 'O':
            print('Invalid input. Please pick X or O :')
        else:
            break
    game = TicTacToe(marker)
    game.initialize_game()
    game.play_alpha_beta()
