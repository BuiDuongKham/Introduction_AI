import numpy as np
import copy


class Othello:
    def __init__(self, board, depth=3):
        # self.board = np.zeros((8,8))
        # self.board[3,3] = 1
        # self.board[4,4] = 1
        # self.board[3,4] = -1
        # self.board[4,3] = -1
        # self.turn = -1
        # self.passed = False
        # self.winner = 0
        # self.legal_moves = self.get_legal_moves()
        # self.game_over = False
        # # self.score = self.get_score()
        # self.history = []
        # self.history.append(copy.deepcopy(self.board))
        # self.depth = depth
        self.board = board
        self.turn = -1
        self.passed = False
        self.winner = 0
        self.legal_moves = self.get_legal_moves()
        self.game_over = False
        # self.score = self.get_score()
        self.history = []
        self.history.append(copy.deepcopy(self.board))
        self.depth = depth

    def get_legal_moves(self):
        legal_moves = []
        for i in range(8):
            for j in range(8):
                if self.board[i, j] == 0:
                    if self.check_legal_move(i, j):
                        legal_moves.append((i, j))
        return legal_moves

    def check_legal_move(self, i, j):
        if self.board[i, j] != 0:
            return False
        for di in [-1, 0, 1]:
            for dj in [-1, 0, 1]:
                if di == 0 and dj == 0:
                    continue
                if self.check_legal_move_direction(i, j, di, dj):
                    return True
        return False

    def check_legal_move_direction(self, i, j, di, dj):
        if i + di < 0 or i + di > 7 or j + dj < 0 or j + dj > 7:
            return False
        if self.board[i + di, j + dj] == 0 or self.board[i + di, j + dj] == self.turn:
            return False
        for k in range(2, 8):
            if i + k * di < 0 or i + k * di > 7 or j + k * dj < 0 or j + k * dj > 7:
                return False
            if self.board[i + k * di, j + k * dj] == 0:
                return False
            if self.board[i + k * di, j + k * dj] == self.turn:
                return True

    def make_move(self, i, j):
        if self.board[i, j] != 0:
            return False
        if (i, j) not in self.get_legal_moves():
            return False
        self.board[i, j] = self.turn
        for di in [-1, 0, 1]:
            for dj in [-1, 0, 1]:
                if di == 0 and dj == 0:
                    continue
                if self.check_legal_move_direction(i, j, di, dj):
                    self.make_move_direction(i, j, di, dj)
        self.turn *= -1
        self.legal_moves = self.get_legal_moves()
        self.history.append(copy.deepcopy(self.board))

        # check win

        if len(self.legal_moves) == 0:
            self.turn *= -1
            self.legal_moves = self.get_legal_moves()
            if len(self.legal_moves) == 0:
                self.game_over = True
                self.winner = np.sign(self.get_score())

        return True

    def make_move_direction(self, i, j, di, dj):
        for k in range(1, 8):
            if self.board[i + k * di, j + k * dj] == self.turn:
                break
            self.board[i + k * di, j + k * dj] = self.turn

    def get_score(self):
        score = 0
        for i in range(8):
            for j in range(8):
                if (i == 0 or i == 7) and (j == 0 or j == 7):
                    score += 10 * self.board[i, j]
                elif (i == 0 or i == 7) or (j == 0 or j == 7):
                    score += 6 * self.board[i, j]
                elif (i == 1 and j == 1) or (i == 1 and j == 6) or (i == 6 and j == 1) or (i == 6 and j == 6):
                    score += 5 * self.board[i, j]
                elif (i == 1 or i == 6) or (j == 1 or j == 6):
                    score += 4 * self.board[i, j]
                elif (i == 2 and j == 2) or (i == 2 and j == 5) or (i == 5 and j == 2) or (i == 5 and j == 5):
                    score += 3 * self.board[i, j]
                elif (i == 2 or i == 5) or (j == 2 or j == 5):
                    score += 2 * self.board[i, j]
                else:
                    score += self.board[i, j]
        return score

    # alpha beta pruning
    def undo_move(self):
        self.history.pop()
        self.board = copy.deepcopy(self.history[-1])
        self.turn *= -1
        self.legal_moves = self.get_legal_moves()

    def max_val(self, alpha, beta, depth):
        # print(depth)
        # print(self.board)
        # print(self.get_score())
        if depth == 0:
            return self.get_score()
        v = -np.inf
        for move in self.get_legal_moves():
            condition = self.make_move(move[0], move[1])
            v = max(v, self.min_val(alpha, beta, depth - 1))
            if condition:
                self.undo_move()
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_val(self, alpha, beta, depth):
        # print(depth)
        # print(self.board)
        # print(self.get_score())
        if depth == 0:
            return self.get_score()
        v = np.inf
        for move in self.get_legal_moves():
            condition = self.make_move(move[0], move[1])
            v = min(v, self.max_val(alpha, beta, depth - 1))
            if condition:
                self.undo_move()
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    def alpha_beta_for_max_vertex(self, depth):
        v = -np.inf
        alpha = -np.inf
        beta = np.inf
        best_move = None
        for move in self.get_legal_moves():
            condition = self.make_move(move[0], move[1])
            new_v = self.min_val(alpha, beta, depth - 1)
            if condition:
                self.undo_move()
            if new_v >= v:
                v = new_v
                best_move = move
            if v >= beta:
                return v, best_move
            alpha = max(alpha, v)
        return v, best_move

    def alpha_beta_for_min_vertex(self, depth):
        v = np.inf
        alpha = -np.inf
        beta = np.inf
        best_move = None
        for move in self.get_legal_moves():
            condition = self.make_move(move[0], move[1])
            new_v = self.max_val(alpha, beta, depth - 1)
            if condition:
                self.undo_move()
            if new_v <= v:
                v = new_v
                best_move = move
            if v <= alpha:
                return v, best_move
            beta = min(beta, v)
        return v, best_move

    def alpha_beta(self):
        if self.turn == 1:
            return self.alpha_beta_for_max_vertex(self.depth)
        else:
            return self.alpha_beta_for_min_vertex(self.depth)