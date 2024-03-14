from reversi import reversi

class MiniMax:
    def minimax_Algorithm(self, game, turn, depth, alpha=float('-inf'), beta=float('inf')): 
        best_score = float('-inf')
        best_move = None
    
        for x in range(0, len(game.board)):
            for y in range(0, len(game.board[x])):
                if game.step(x, y, turn, False) > 0:
                    score = self.min_value(game, depth - 1, -turn, alpha, beta)
                    if score > best_score:
                        best_score = score
                        best_move = (x, y)
                    alpha = max(alpha, best_score)
                    if alpha >= beta:
                        break
        if best_move is None:
            best_move = (-1, -1)
        return best_move

    def max_value(self, game, depth, turn, alpha, beta):
        if depth <= 0: 
            return self.evaluate(game, turn)

        max_score = float('-inf')
        for x in range(0, len(game.board)):
            for y in range(0, len(game.board[x])):
                if game.step(x, y, turn, False) > 0:
                    score = self.min_value(game, depth - 1, -turn, alpha, beta)
                    max_score = max(max_score, score)
                    alpha = max(alpha, max_score)
                    if alpha >= beta:
                        return max_score
        return max_score

    def min_value(self, game, depth, turn, alpha, beta):
        if depth <= 0: 
            return self.evaluate(game, turn)
    
        min_score = float('inf')
        for x in range(0, len(game.board)):
            for y in range(0, len(game.board[x])):
                if game.step(x, y, turn, False) > 0:
                    score = self.max_value(game, depth - 1, -turn, alpha, beta)
                    min_score = min(min_score, score)
                    beta = min(beta, min_score)
                    if alpha >= beta:
                        return min_score
        return min_score

    def evaluate(self, game, turn):
        if turn == 1:
            return game.white_count - game.black_count
        return game.black_count - game.white_count