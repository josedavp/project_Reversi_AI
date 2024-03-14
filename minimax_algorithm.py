from reversi import reversi

class MiniMax:
    """ Contains the method and helper functions used for MiniMax Algorithm. """
    def minimax_Algorithm(self, game, turn, depth): 
        """ 
            Handles the MiniMax Algorithm used for Reversi AI Game

            Parameters:
                game (object): Game State; Representing Reversi/game state
                turn (int): Whos turn it is in game (-1 black or 1 for white)
                depth (int): Depth of search 
                
            Returns:
            x (): Coordinate for next move
            y (): Coordinate for next move
        """ 
        best_score = float('-inf')
        best_move = None #(returns x, y) coordinates of best move
    
        for x in range(0, len(game.board)):
            for y in range(0, len(game.board[x])):
                #if depth > 0 and game.step(i, j, turn, False) != -3: # or later on switch -3 to a 0
                if game.step(x, y, turn, False) >0:  #!= -3:  # Check if move is legal; -3 for now; change for depth maybe
                # if game.legal_move(x,y, turn):  
                #     game.make_move(x,y, turn)
                    score = self.min_value(game, depth -1, -turn)
                #     game.undo_move()
                    # score = self.min_value(game, depth - 1, -turn) # THIS IS THE TARGETED AREA FOR ISSUE
                    if score > best_score:
                        best_score = score
                        best_move = (x, y)
        if best_move == None:
            best_move = (-1, -1)
            return -1, -1
        #game.step(best_move[0], best_move[1], turn, True)
        return best_move

    def max_value(self, game, depth, turn): #add alpha, beta in parameters for pruning
        """
            Max-value operation in MiniMax algorithm.

            Parameters:
                game (object): Current game state
                depth (int): Depth of search
                turn (int): Player's turn (1 or -1)

            Returns:
                max_score (int): Maximum value achievable by the current player
        """        
        if depth <= 0: 
            return self.evaluate(game, turn)

        max_score = float('-inf')
    
        for x in range(0, len(game.board)):
            for y in range(0, len(game.board[x])):
                if game.step(x, y, turn, False) >0: #!= -3:  # Check if move is legal; -3 for now; change for depth maybe
                    score = self.min_value(game, depth - 1, -turn)
                    max_score = max(max_score, score) #correct?
                        
        return max_score


    def min_value(self, game, depth, turn): #add alpha, beta in parameters for pruning
        """
            Min-value operation in MiniMax algorithm.

            Parameters:
                game (object): Current game state
                depth (int): Depth of search
                turn (int): Player's turn (1 or -1)

            Returns:
                min_score (int): Minimum value achievable by the opponent player
        """
        
        if depth <= 0: 
            return self.evaluate(game, turn)
    
        minimum_score = float('inf') #verify
       
        for x in range(0, len(game.board)):
            for y in range(0, len(game.board[x])):
                if game.step(x, y, turn, False) >0: # != -3:  
                    score = self.max_value(game, depth - 1, -turn)
                    minimum_score = min(minimum_score, score) #score 
                        
        return minimum_score
   
    
    def evaluate(self, game, turn):
        """Check if the game is inline with player score.

        Parameters:
            game (_type_): Current state
            turn (_type_): The turn in the game

        Return:
            int:The difference in player score/count.
        """
        if turn == 1:
            return game.white_count - game.black_count
        
        return game.black_count - game.white_count 