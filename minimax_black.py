import socket
import pickle
import numpy as np
from copy import deepcopy
from reversi import reversi

class ReversiAI:
    def __init__(self, color):
        self.color = color
        self.opponent_color = -color
        self.max_depth = 3

    def evaluate_board(self, board):
        # Simple evaluation function: the difference between the number of pieces
        return np.sum(board == self.color) - np.sum(board == self.opponent_color)

    def minimax(self, board, depth, alpha, beta, maximizing_player):
        if depth == 0:
            return self.evaluate_board(board), None
        
        legal_moves = self.get_legal_moves(board, self.color if maximizing_player else self.opponent_color)
        
        if maximizing_player:
            max_eval = float('-inf')
            best_move = None
            for move in legal_moves:
                new_board = deepcopy(board)
                self.make_move(new_board, move[0], move[1], self.color)
                eval, _ = self.minimax(new_board, depth - 1, alpha, beta, False)
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval, best_move
        else:
            min_eval = float('inf')
            for move in legal_moves:
                new_board = deepcopy(board)
                self.make_move(new_board, move[0], move[1], self.opponent_color)
                eval, _ = self.minimax(new_board, depth - 1, alpha, beta, True)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval, None

    def make_move(self, board, x, y, color):
        game = reversi()
        game.board = board
        game.step(x, y, color)

    def get_legal_moves(self, board, color):
        game = reversi()
        game.board = board
        legal_moves = []
        for i in range(8):
            for j in range(8):
                if game.step(i, j, color, False) > 0:
                    legal_moves.append((i, j))
        return legal_moves

def main():
    game_socket = socket.socket()
    game_socket.connect(('127.0.0.1', 33333))
    ai = ReversiAI(-1)  # Assuming AI is playing as black
    while True:
        data = game_socket.recv(4096)
        turn, board = pickle.loads(data)
        if turn == 0:
            game_socket.close()
            return

        if turn == ai.color:
            _, move = ai.minimax(board, ai.max_depth, float('-inf'), float('inf'), True)
            if move is None:
                x, y = -1, -1  # No move possible
            else:
                x, y = move
            game_socket.send(pickle.dumps([x, y]))
        else:
            print("Opponent's turn.")

if __name__ == '__main__':
    main()