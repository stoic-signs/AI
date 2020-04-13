import random
import numpy as np
import copy
from collections import namedtuple
import itertools
# from utils import vectors_add

GameState = namedtuple('GameState', 'to_move, utility, board, moves')


def basic_minimax(state, game):
    player = game.to_move(state)

    def max_val(state):
        if game.terminal_test(state):
            return game.utility(state, player)
        val = -np.inf
        for action in game.actions(state):
            val = max(val, min_val(game.result(state, action)))
        return val

    def min_val(state):
        if game.terminal_test(state):
            return game.utility(state, player)
        val = np.inf
        for action in game.actions(state):
            val = min(val, max_val(game.result(state, action)))
        return val

    return max(game.actions(state), key=lambda action:
               min_val(game.result(state, action)))


def minimax_cutoff(state, game, d=5, cutoff_test=None, eval_fn=None):
    player = game.to_move(state)
    print(cutoff_test)

    def max_val(state, depth):
        if cutoff_test(state, depth):
            return eval_fn(state)
        val = -np.inf
        for action in game.actions(state):
            val = max(val, min_val(game.result(state, action), depth + 1))
        return val

    def min_val(state, depth):
        if cutoff_test(state, depth):
            return eval_fn(state)
        val = np.inf
        for action in game.actions(state):
            val = min(val, max_val(game.result(state, action), depth + 1))
        return val

    # return max(game.actions(state), key=lambda a:
    #            min_val(game.result(state, action)))
    cutoff_test = (cutoff_test or (lambda state, depth: depth >
                                   d or game.terminal_test(state)))
    eval_fn = eval_fn or (lambda state: game.utility(state, player))
    return max(game.actions(state), key=lambda action:
               min_val(game.result(state, action), 1))


def alpha_beta_pruning(state, game):
    player = game.to_move(state)

    def max_val(state, alpha, beta):
        if game.terminal_test(state):
            return game.utility(state, player)
        val = -np.inf
        for action in game.actions(state):
            val = max(val, min_val(game.result(state, action), alpha, beta))
            if val >= beta:
                return val
            alpha = max(alpha, val)
        return val

    def min_val(state, alpha, beta):
        if game.terminal_test(state):
            return game.utility(state, player)
        val = np.inf
        for action in game.actions(state):
            val = min(val, max_val(game.result(state, action), alpha, beta))
            if val <= alpha:
                return val
            beta = min(beta, val)
        return val

    best_score = -np.inf
    beta = np.inf
    best_act = None
    for action in game.actions(state):
        val = min_val(game.result(state, action), best_score, beta)
        if val > best_score:
            best_score = val
            best_act = action
    return best_act


def alpha_beta_cutoff(state, game, d=5, cutoff_test=None, eval_fn=None):
    player = game.to_move(state)
    print(cutoff_test)

    def max_val(state, alpha, beta, depth):
        if cutoff_test(state, depth):
            return eval_fn(state)
        val = -np.inf
        for action in game.actions(state):
            val = max(val, min_val(game.result(
                state, action), alpha, beta, depth + 1))
            if val >= beta:
                return val
            alpha = max(alpha, val)
        return val

    def min_val(state, alpha, beta, depth):
        if cutoff_test(state, depth):
            return eval_fn(state)
        val = np.inf
        for action in game.actions(state):
            val = min(val, max_val(game.result(
                state, action), alpha, beta, depth + 1))
            if val <= alpha:
                return val
            beta = min(beta, val)
        return val

    cutoff_test = cutoff_test or (
        lambda state, depth: depth > d or game.terminal_test(state))
    eval_fn = eval_fn or (lambda state: game.utility(state, player))
    best_score = -np.inf
    beta = np.inf
    best_act = None
    for action in game.actions(state):
        val = min_val(game.result(state, action), best_score, beta, 1)
        if val > best_score:
            best_score = val
            best_act = action
    return best_act


class TicTacToe:
    def __init__(self, n=3, k=3):
        self.n = n
        self.k = k
        self.num_moves = 0
        moves = [(x, y) for x in range(1, self.n + 1)
                 for y in range(1, self.n + 1)]
        self.initial = GameState(to_move='X', utility=0, board={}, moves=moves)

    def actions(self, state):
        return state.moves

    def result(self, state, move):
        if move not in state.moves:
            return state
        board = state.board.copy()
        board[move] = state.to_move
        moves = list(state.moves)
        moves.remove(move)
        self.num_moves += 1
        return GameState(to_move=('O' if state.to_move == 'X' else 'X'),
                         utility=self.compute_utility(
                             board, move, state.to_move),
                         board=board, moves=moves)

    def utility(self, state, player):
        return state.utility if player == 'X' else -state.utility

    def terminal_test(self, state):
        return state.utility != 0 or len(state.moves) == 0

    def to_move(self, state):
        return state.to_move

    def display(self, state):
        board = state.board
        for x in range(1, self.n + 1):
            for y in range(1, self.n + 1):
                print(board.get((x, y), '.'), end=' ')
            print()

    def compute_utility(self, board, move, player):
        if (self.k_in_a_row(board, move, player, (0, 1)) or
            self.k_in_a_row(board, move, player, (1, 0)) or
            self.k_in_a_row(board, move, player, (1, -1)) or
                self.k_in_a_row(board, move, player, (1, 1))):
            return +1 if player == 'X' else -1
        else:
            return 0

    def k_in_a_row(self, board, move, player, temp_x_y):
        len = 0
        if self.num_moves >= (2 * self.k - 1):
            (temp_x, temp_y) = temp_x_y
            x, y = move
            while board.get((x, y)) == player:
                len += 1
                x, y = x + temp_x, y + temp_y
            x, y = move
            while board.get((x, y)) == player:
                len += 1
                x, y = x - temp_x, y - temp_y
            len -= 1
        return len >= self.k

    def play_game(self, game, *players):
        state = game.state
        while True:
            for player in players:
                move = player(self, state)
                state = self.result(state, move)
                if self.terminal_test(state):
                    self.display(state)
                    return self.utility(state, self.to_move(self.initial))


def alpha_beta_player(state, game):
    return alpha_beta_pruning(state, game)


def minimax_player(state, game):
    return basic_minimax(state, game)


def alpha_beta_cutoff_player(state, game):
    return alpha_beta_cutoff(state, game)


def query_player(game, state):
    """Make a move by querying standard input."""
    print("current state:")
    game.display(state)
    print("available moves: {}".format(game.actions(state)))
    print("")
    move = None
    if game.actions(state):
        move_string = input('Your move? ')
        try:
            move = eval(move_string)
        except NameError:
            move = move_string
    else:
        print('no legal moves: passing turn to next player')
    return move
