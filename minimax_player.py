#Zijie Zhang, Sep.24/2023

import pygame
import numpy as np
import socket, pickle
from reversi import reversi
from minimax_algorithm import MiniMax

def main():
    game_socket = socket.socket()
    game_socket.connect(('127.0.0.1', 33333))
    game = reversi()
    minimax = MiniMax()
    
    #############
    depth = 4 #figure out correct depth or if needs to be adjusted dynamically
    ###############

    while True:

        #Receive play request from the server
        #turn : 1 --> you are playing as white | -1 --> you are playing as black
        #board : 8*8 numpy array
        data = game_socket.recv(4096)
        turn, board = pickle.loads(data)

        #Turn = 0 indicates game ended
        if turn == 0:
            game_socket.close()
            return
        
        #Debug info
        print(turn)
        print(game.board)
        print(board)
        
        #MiniMax Algorithm  - Replace with your algorithm
        x,y = minimax.minimax_Algorithm(game, turn, depth)
        # Print the chosen move
        print("Selected move:", (x, y))
        
        
        ####
        # board = local board we have; not updated by server
        # game.board = is the updated version of the board game from server
        # if (x,y, turn, False)   <----- the false does not commit the new pieces. it just checks them
        #
        # we need to verify if the update is being passed properly  (x,y) coordinates
        # we need to make sure that the board being read is the correct board (game.board)
        # we still the entire contents of game since thats whats being used to step and read board
        ##########
        
        
        
        
        
        ###############################
        
        #Send your move to the server. Send (x,y) = (-1,-1) to tell the server you have no hand to play
        game_socket.send(pickle.dumps([x,y]))
        
if __name__ == '__main__':
    main()